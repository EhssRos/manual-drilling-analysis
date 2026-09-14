"""
06_make_fig3_tiltplane.py -- Reproduces Fig. 3 (tool-orientation deviation
from the true drilling axis, by phase), as used in the paper's Table 2
rows "Positioning / tip alignment" and "Controlled entry".

Unlike 05_tilt_direction_analysis.py (an earlier, exploratory script that
compares each phase to the *positioning*-phase baseline), this script uses
the mean orientation during *full engagement* as the reference (0, 0):
full engagement is the only phase in which the tool is mechanically
constrained by the forming hole, so it is the best available estimate of
the "true" drilling axis. Positioning, tip engagement, and breakthrough are
then expressed as deviations from that true axis.

For the horizontal-feed subset specifically, the feed axis sits only
2-18 deg from world-vertical, which makes a world-vertical-anchored
perpendicular frame numerically unstable (see `local_frame`); the fallback
anchor (world-X) is used there instead, and the resulting plane is
rotated and relabelled "toward body" / "away from body" based on the
corresponding author's own review of the recorded video, since this
cannot be established from the tracking data alone (there is no recorded
information on how the OptiTrack world frame was calibrated relative to
the room, or on the operator's exact body position during recording). For
the vertical-feed subset, the feed axis sits 75-88 deg from world-vertical,
where the same frame construction is well-conditioned and the "away from
body" axis coincides with the true vertical.

Run after 01_build_clean_dataset.py, from the scripts/ directory:
    python 06_make_fig3_tiltplane.py
Writes: figures/fig_tilt_plane.pdf, output/tiltplane_horizontal.csv,
        output/tiltplane_vertical.csv
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from common import (
    load_annotations, horizontal_feed_subset, vertical_feed_subset,
    load_hole, rolling_median, signed_feed_force, tip_full_boundary,
)

WORLD_UP = np.array([0, 0, 1.0])
NEAR_PARALLEL_DEG = 25

PHASE_COLORS = {"pos": "#888888", "tip": "#4a90d9", "full": "#4caf50", "bt": "#ff9800"}
PHASE_LABELS = {"pos": "Positioning", "tip": "Tip engagement", "bt": "Breakthrough"}


def tool_z_axis(qx, qy, qz, qw):
    zx = 2 * (qx * qz + qw * qy)
    zy = 2 * (qy * qz - qw * qx)
    zz = 1 - 2 * (qx**2 + qy**2)
    return np.stack([zx, zy, zz], axis=-1)


def local_frame(feed_axis):
    """See 05_tilt_direction_analysis.py's local_frame for the full
    rationale; identical construction, reused here for consistency."""
    f = feed_axis / np.linalg.norm(feed_axis)
    angle_to_world_up = np.degrees(np.arccos(np.clip(abs(np.dot(f, WORLD_UP)), -1, 1)))
    anchor = np.array([1.0, 0, 0]) if angle_to_world_up < NEAR_PARALLEL_DEG else WORLD_UP
    up_ref = anchor - np.dot(anchor, f) * f
    up_ref /= np.linalg.norm(up_ref)
    side_ref = np.cross(f, up_ref)
    return up_ref, side_ref


def hole_phase_points(row):
    """Returns each phase's mean (up, side) tool orientation, expressed as
    a deviation from the full-engagement mean (the true drilling axis)."""
    f, o = load_hole(row)
    if f is None:
        return None
    fz = signed_feed_force(f)
    fz_s = rolling_median(fz, max(3, int(len(fz) * 0.06)))
    t_sub, plateau = tip_full_boundary(f.t.values, fz_s, row.start_time, row.end_time)
    if t_sub is None:
        return None

    pos_cols = ["pos_x", "pos_y", "pos_z"]
    p_start = np.array([np.interp(row.start_time, o.t.values, o[c].values) for c in pos_cols])
    p_end = np.array([np.interp(row.end_time, o.t.values, o[c].values) for c in pos_cols])
    feed_axis = p_end - p_start
    if np.linalg.norm(feed_axis) < 1e-6:
        return None
    up_ref, side_ref = local_frame(feed_axis)

    toolz = tool_z_axis(o.quat_x.values, o.quat_y.values, o.quat_z.values, o.quat_w.values)
    proj_up = rolling_median(toolz @ up_ref, 5)
    proj_side = rolling_median(toolz @ side_ref, 5)

    def mean_in(mask):
        return (np.nanmean(proj_up[mask]), np.nanmean(proj_side[mask])) if mask.sum() > 1 else (np.nan, np.nan)

    pos_mask = o.t.values < row.start_time - 0.3
    tip_mask = (o.t.values >= row.start_time) & (o.t.values <= t_sub)
    full_mask = (o.t.values >= t_sub) & (o.t.values <= row.end_time)
    bt_mask = (o.t.values > row.end_time) & (o.t.values <= row.end_time + 0.4)

    pu, ps = mean_in(pos_mask)
    tu, ts = mean_in(tip_mask)
    fu, fs = mean_in(full_mask)  # reference
    bu, bs = mean_in(bt_mask)
    return dict(
        pos_up=pu - fu, pos_side=ps - fs,
        tip_up=tu - fu, tip_side=ts - fs,
        full_up=0.0, full_side=0.0,
        bt_up=bu - fu, bt_side=bs - fs,
    )


def collect(fn):
    ann = load_annotations()
    rows = fn(ann)
    recs = [r for r in (hole_phase_points(row) for _, row in rows.iterrows()) if r is not None]
    return pd.DataFrame(recs)


def print_stats(df, label, body_axis_col, sign):
    """Prints, for each phase, the mean deviation along the body-relevant
    axis and a binomial test of directional consistency against chance."""
    print(f"\n=== {label} (n={len(df)}) ===")
    for phase in ["pos", "tip", "bt"]:
        vals = sign * df[f"{phase}_{body_axis_col}"].dropna()
        n_majority = (np.sign(vals) == np.sign(vals.mean())).sum()
        n_total = len(vals)
        p_binom = stats.binomtest(n_majority, n_total, 0.5, alternative="greater").pvalue
        direction = "away from body" if vals.mean() > 0 else "toward body"
        print(f"{phase}: mean={vals.mean():+.3f} ({direction}), "
              f"{n_majority}/{n_total}={n_majority/n_total*100:.0f}% consistent, p={p_binom:.2e}")


def main():
    df_h = collect(horizontal_feed_subset)
    df_v = collect(vertical_feed_subset)
    df_h.to_csv("../output/tiltplane_horizontal.csv", index=False)
    df_v.to_csv("../output/tiltplane_vertical.csv", index=False)

    # Horizontal-feed: "away from body" = -side (see module docstring for why)
    print_stats(df_h, "horizontal-feed", "side", sign=-1)
    # Vertical-feed: "away from body"/true-vertical = +up
    print_stats(df_v, "vertical-feed", "up", sign=1)

    plt.rcParams.update({"font.size": 9, "font.family": "serif"})
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.6))

    def rot_h(u, s):
        return u, -s  # rotate horizontal-feed frame 90 deg: plotted (x,y) = (up, -side)

    ax = axes[0]
    for phase in ["pos", "tip", "bt"]:
        x, y = rot_h(df_h[f"{phase}_up"], df_h[f"{phase}_side"])
        ax.scatter(x, y, alpha=0.25, s=12, color=PHASE_COLORS[phase])
    ax.scatter([0], [0], s=55, color=PHASE_COLORS["full"], marker="s", zorder=5, label="Full engagement (ref.)")
    path_x, path_y = [], []
    for phase in ["pos", "tip"]:
        x, y = rot_h(df_h[f"{phase}_up"].mean(), df_h[f"{phase}_side"].mean())
        path_x.append(x)
        path_y.append(y)
    path_x.append(0)
    path_y.append(0)
    x, y = rot_h(df_h["bt_up"].mean(), df_h["bt_side"].mean())
    path_x.append(x)
    path_y.append(y)
    ax.plot(path_x, path_y, color="black", lw=1.0, ls="--", zorder=4)
    for phase, x, y in zip(["pos", "tip", "bt"], [path_x[0], path_x[1], path_x[3]], [path_y[0], path_y[1], path_y[3]]):
        ax.scatter([x], [y], s=60, color=PHASE_COLORS[phase], edgecolor="black", lw=0.6, zorder=6, label=PHASE_LABELS[phase])
    ax.set_title(f"Horizontal-feed (n={len(df_h)})", fontsize=9)
    ax.set_xlabel("Lateral deviation", fontsize=8)
    ax.set_ylabel("Away from body (+) / toward body ($-$)", fontsize=8)
    ax.axhline(0, color="gray", lw=0.4)
    ax.axvline(0, color="gray", lw=0.4)
    lim = 0.42
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.2, lw=0.4)

    ax = axes[1]
    for phase in ["pos", "tip", "bt"]:
        ax.scatter(df_v[f"{phase}_side"], df_v[f"{phase}_up"], alpha=0.25, s=12, color=PHASE_COLORS[phase])
    ax.scatter([0], [0], s=55, color=PHASE_COLORS["full"], marker="s", zorder=5)
    path_x = [df_v.pos_side.mean(), df_v.tip_side.mean(), 0, df_v.bt_side.mean()]
    path_y = [df_v.pos_up.mean(), df_v.tip_up.mean(), 0, df_v.bt_up.mean()]
    ax.plot(path_x, path_y, color="black", lw=1.0, ls="--", zorder=4)
    for phase, x, y in zip(["pos", "tip", "bt"], [path_x[0], path_x[1], path_x[3]], [path_y[0], path_y[1], path_y[3]]):
        ax.scatter([x], [y], s=60, color=PHASE_COLORS[phase], edgecolor="black", lw=0.6, zorder=6)
    ax.set_title(f"Vertical-feed (n={len(df_v)})", fontsize=9)
    ax.set_xlabel("Lateral deviation", fontsize=8)
    ax.set_ylabel("Away from body (+) / toward body ($-$)", fontsize=8)
    ax.axhline(0, color="gray", lw=0.4)
    ax.axvline(0, color="gray", lw=0.4)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.tick_params(labelsize=7)
    ax.grid(alpha=0.2, lw=0.4)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=7.5, bbox_to_anchor=(0.5, -0.06), frameon=False)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig("../figures/fig_tilt_plane.pdf", bbox_inches="tight")
    print("\nWrote figures/fig_tilt_plane.pdf")


if __name__ == "__main__":
    main()
