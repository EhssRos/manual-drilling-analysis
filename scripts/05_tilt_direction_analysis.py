"""
05_tilt_direction_analysis.py -- Tests whether tool-tilt deviation from the
positioning-phase baseline has a consistent *direction*, not just a
consistent magnitude/rate (see 01_build_clean_dataset.py's tilt-rate
feature, used for the Controlled-entry result in Table 2).

IMPORTANT METHODOLOGICAL NOTE: tilt direction must be computed relative to
the hole's actual feed axis (Start-to-End displacement), not relative to a
fixed world axis. The horizontal-feed subset's feed axis sits only 2-18 deg
from world-Z, so projecting onto the world XY-plane is close to
numerically degenerate there; the vertical-feed subset's feed axis sits
75-88 deg from world-Z, where the same projection is well-conditioned. This
script builds a per-hole local (up, side) frame perpendicular to that
hole's own feed axis, anchored on world-vertical wherever that anchor is
not close to parallel to the feed axis (see `local_frame`), so that the
"up" component genuinely means "against gravity" specifically for the
vertical-feed subset. For the horizontal-feed subset, the fallback anchor
(world-X) is used instead to keep the frame numerically stable across
holes, but this means "up"/"side" there are only a fixed, arbitrary
reference direction, not a gravity-relative one -- see the printed output
and the paper text for how this caveat is handled.

Run after 01_build_clean_dataset.py, from the scripts/ directory:
    python 05_tilt_direction_analysis.py
Writes: output/tilt_direction_horizontal.csv, output/tilt_direction_vertical.csv
        figures/tilt_direction.png
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import (
    load_annotations, horizontal_feed_subset, vertical_feed_subset,
    load_hole, rolling_median, signed_feed_force, tip_full_boundary,
)

WORLD_UP = np.array([0, 0, 1.0])
NEAR_PARALLEL_DEG = 25  # below this angle to the feed axis, the primary
                        # anchor (world-up) is numerically unstable


def tool_z_axis(qx, qy, qz, qw):
    """Tool body-frame z-axis expressed in world coordinates (full unit
    vector, not just the angle used elsewhere for tilt magnitude/rate)."""
    zx = 2 * (qx * qz + qw * qy)
    zy = 2 * (qy * qz - qw * qx)
    zz = 1 - 2 * (qx**2 + qy**2)
    return np.stack([zx, zy, zz], axis=-1)


def local_frame(feed_axis):
    """Builds a local (up, side) frame perpendicular to the given feed
    axis, consistent across holes. Anchored on world-vertical, falling
    back to world-X when the feed axis is within NEAR_PARALLEL_DEG of
    world-vertical (this is the case for every hole in the
    horizontal-feed subset), to avoid dividing by a near-zero-length
    vector after removing the parallel component."""
    f = feed_axis / np.linalg.norm(feed_axis)
    angle_to_world_up = np.degrees(np.arccos(np.clip(abs(np.dot(f, WORLD_UP)), -1, 1)))
    anchor = np.array([1.0, 0, 0]) if angle_to_world_up < NEAR_PARALLEL_DEG else WORLD_UP
    up_ref = anchor - np.dot(anchor, f) * f
    up_ref /= np.linalg.norm(up_ref)
    side_ref = np.cross(f, up_ref)
    return up_ref, side_ref, angle_to_world_up


def analyze_subset(rows, label):
    results = []
    for _, row in rows.iterrows():
        f, o = load_hole(row)
        if f is None:
            continue
        fz = signed_feed_force(f)
        fz_s = rolling_median(fz, max(3, int(len(fz) * 0.06)))
        t_sub, plateau = tip_full_boundary(f.t.values, fz_s, row.start_time, row.end_time)
        if t_sub is None:
            continue

        # Feed axis from the tracked marker's Start -> End displacement
        pos_cols = ["pos_x", "pos_y", "pos_z"]
        p_start = np.array([np.interp(row.start_time, o.t.values, o[c].values) for c in pos_cols])
        p_end = np.array([np.interp(row.end_time, o.t.values, o[c].values) for c in pos_cols])
        feed_axis = p_end - p_start
        if np.linalg.norm(feed_axis) < 1e-6:
            continue
        up_ref, side_ref, angle_to_world_up = local_frame(feed_axis)

        toolz = tool_z_axis(o.quat_x.values, o.quat_y.values, o.quat_z.values, o.quat_w.values)
        proj_up = rolling_median(toolz @ up_ref, 5)
        proj_side = rolling_median(toolz @ side_ref, 5)

        def mean_in(t0, t1):
            m = (o.t.values >= t0) & (o.t.values <= t1)
            return (np.nanmean(proj_up[m]), np.nanmean(proj_side[m])) if m.sum() > 1 else (np.nan, np.nan)

        pos_mask = o.t.values < row.start_time - 0.3
        base_up, base_side = (
            (np.nanmean(proj_up[pos_mask]), np.nanmean(proj_side[pos_mask])) if pos_mask.sum() > 2 else (np.nan, np.nan)
        )
        full_up, full_side = mean_in(t_sub, row.end_time)

        results.append(dict(
            file=row.file, angle_feed_to_world_up=angle_to_world_up,
            base_up=base_up, base_side=base_side, full_up=full_up, full_side=full_side,
        ))

    df = pd.DataFrame(results)
    df["dev_full_up"] = df.full_up - df.base_up
    df["dev_full_side"] = df.full_side - df.base_side

    du, ds = df.dev_full_up.dropna(), df.dev_full_side.dropna()
    consistency_up = (np.sign(du) == np.sign(du.mean())).mean() * 100
    consistency_side = (np.sign(ds) == np.sign(ds.mean())).mean() * 100
    well_conditioned = df.angle_feed_to_world_up.mean() >= NEAR_PARALLEL_DEG
    print(f"\n=== {label} (n={len(df)}) ===")
    print(f"Mean feed-axis angle to world-vertical: {df.angle_feed_to_world_up.mean():.1f} deg "
          f"({'well-conditioned -- up is gravity-relative' if well_conditioned else 'near-parallel -- up is an arbitrary but stable direction only'})")
    print(f"Deviation (up, side) = ({du.mean():.3f}, {ds.mean():.3f}); "
          f"directional consistency: up={consistency_up:.0f}%, side={consistency_side:.0f}%")
    return df


def main():
    ann = load_annotations()
    df_h = analyze_subset(horizontal_feed_subset(ann), "horizontal-feed")
    df_v = analyze_subset(vertical_feed_subset(ann), "vertical-feed")
    df_h.to_csv("../output/tilt_direction_horizontal.csv", index=False)
    df_v.to_csv("../output/tilt_direction_vertical.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    titles = [
        "Horizontal-feed (n=%d)\n(feed axis near world-vertical: 'up'/'side'\nare a stable but arbitrary direction, not gravity-relative)" % len(df_h),
        "Vertical-feed (n=%d)\n(feed axis far from world-vertical: 'up'\ngenuinely means against gravity)" % len(df_v),
    ]
    for ax, df, title in zip(axes, [df_h, df_v], titles):
        ax.axhline(0, color="gray", lw=0.5)
        ax.axvline(0, color="gray", lw=0.5)
        ax.scatter(df.dev_full_side, df.dev_full_up, alpha=0.5, s=25, color="#1f77b4")
        mu, ms = df.dev_full_up.mean(), df.dev_full_side.mean()
        ax.annotate("", xy=(ms, mu), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="red", lw=2.5))
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("Side deviation")
        if ax is axes[0]:
            ax.set_ylabel("'Up' deviation")
        ax.set_xlim(-0.45, 0.45)
        ax.set_ylim(-0.45, 0.45)
        ax.set_aspect("equal")
        ax.grid(alpha=0.2)
    fig.suptitle("Tool-tilt deviation direction relative to the hole's own feed axis (full engagement)", fontsize=10)
    fig.tight_layout()
    fig.savefig("../figures/tilt_direction.png", dpi=130, bbox_inches="tight")
    print("\nWrote figures/tilt_direction.png")


if __name__ == "__main__":
    main()
