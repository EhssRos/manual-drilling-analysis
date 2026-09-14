"""
03_make_fig1_phases.py -- Reproduce Fig. 1 (four-phase model, 2x2 grid:
feed force, torque about the feed axis, feed-axis acceleration, tool tilt),
4mm plates, horizontal-feed subset, as used in the paper.

Run after 01_build_clean_dataset.py, from the scripts/ directory:
    python 03_make_fig1_phases.py
Writes: figures/fig_phases_4mm_2x2.pdf
"""

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import (
    load_annotations, horizontal_feed_subset, load_hole, rolling_median,
    signed_feed_force, tip_full_boundary, quat_to_tilt,
)

T_GRID = np.linspace(-1.05, 1.8, 500)


def resample_hole(row):
    f, o = load_hole(row)
    if f is None:
        return None
    fz = signed_feed_force(f)
    fz_s = rolling_median(fz, max(3, int(len(fz) * 0.06)))
    t_sub, plateau = tip_full_boundary(f.t.values, fz_s, row.start_time, row.end_time)
    if t_sub is None:
        return None

    # Contact onset: first point, searching backward from Start, at which
    # smoothed force has been continuously below 5% of the in-window
    # plateau (i.e. the last "at rest" sample before force starts rising).
    pre_mask = f.t.values <= row.start_time
    pre_idx = np.where(pre_mask)[0]
    contact_t = row.start_time - 1.0  # fallback
    thresh = 0.05 * plateau
    for i in reversed(pre_idx):
        if fz_s[i] < thresh:
            contact_t = f.t.values[i]
            break

    dur_contact_start = max(row.start_time - contact_t, 1e-6)
    dur_tip = t_sub - row.start_time
    dur_full = row.end_time - t_sub

    def to_norm(t):
        if t < contact_t:
            return -1.2  # will fall outside the plotted range, clipped by T_GRID
        elif t < row.start_time:
            return -1 + (t - contact_t) / dur_contact_start
        elif t < t_sub:
            return (t - row.start_time) / max(dur_tip, 1e-6) * 0.25
        elif t < row.end_time:
            return 0.25 + (t - t_sub) / max(dur_full, 1e-6) * 0.75
        else:
            return 1 + (t - row.end_time) / max(dur_full, 1e-6)

    t_norm_f = np.array([to_norm(t) for t in f.t.values])
    tz_s = rolling_median(f.Tz.values, 5)

    vel = np.gradient(rolling_median(o.pos_z.values, 7), o.t.values) if "pos_z" in o.columns else None
    accel = np.gradient(vel, o.t.values) if vel is not None else None
    t_norm_o = np.array([to_norm(t) for t in o.t.values])

    tilt = quat_to_tilt(o.quat_x.values, o.quat_y.values, o.quat_z.values, o.quat_w.values)

    fz_r = np.interp(T_GRID, t_norm_f, fz_s, left=np.nan, right=np.nan)
    tz_r = np.interp(T_GRID, t_norm_f, tz_s, left=np.nan, right=np.nan)
    tilt_r = np.interp(T_GRID, t_norm_o, rolling_median(tilt, 5), left=np.nan, right=np.nan)
    accel_r = np.interp(T_GRID, t_norm_o, accel, left=np.nan, right=np.nan) if accel is not None else np.full_like(T_GRID, np.nan)

    return fz_r, tz_r, accel_r, tilt_r, 0.25  # 0.25 = normalised tip/full boundary


def main():
    ann = load_annotations()
    subset = horizontal_feed_subset(ann)
    subset4 = subset[subset.thickness == 4]

    fz_all, tz_all, ac_all, tilt_all = [], [], [], []
    for _, row in subset4.iterrows():
        result = resample_hole(row)
        if result is not None:
            fz_r, tz_r, accel_r, tilt_r, _ = result
            fz_all.append(fz_r); tz_all.append(tz_r); ac_all.append(accel_r); tilt_all.append(tilt_r)

    n = len(fz_all)
    fz_all, tz_all, ac_all, tilt_all = map(np.array, (fz_all, tz_all, ac_all, tilt_all))

    PHASE_COLORS = ["#ececec", "#d6e9f7", "#c8e6c9", "#ffe0b2"]
    PHASE_LABELS = ["Positioning", "Tip engagement", "Full engagement", "Breakthrough"]
    bounds = [(-1.05, 0), (0, 0.25), (0.25, 1), (1, 1.6)]

    plt.rcParams.update({"font.size": 9, "font.family": "serif"})
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.6), sharex=True)

    panels = [
        (fz_all, "Feed force $F_z$ (N)", "#1f77b4", "mean_std"),
        (tz_all, "Torque about feed axis $T_z$ (Nm)", "#8B008B", "mean_std"),
        (ac_all, "Feed-axis acceleration (m/s$^2$)", "#B8860B", "median_iqr"),
        (tilt_all, "Tool tilt (deg)", "#2ca02c", "mean_std"),
    ]
    for ax, (data, ylabel, color, kind) in zip(axes.flat, panels):
        for (x0, x1), pc in zip(bounds, PHASE_COLORS):
            ax.axvspan(x0, x1, color=pc, zorder=0)
        ax.axvline(0, color="k", lw=0.7); ax.axvline(1, color="k", lw=0.7)
        ax.set_xlim(-1.05, 1.6)
        if kind == "mean_std":
            m = np.nanmean(data, axis=0); s = np.nanstd(data, axis=0)
        else:
            m = np.nanmedian(data, axis=0)
            s = None
        valid = ~np.isnan(m)
        ax.plot(T_GRID[valid], m[valid], color=color, lw=1.4, zorder=3)
        if kind == "mean_std":
            ax.fill_between(T_GRID[valid], (m - s)[valid], (m + s)[valid], color=color, alpha=0.18, lw=0)
        else:
            q25 = np.nanpercentile(data, 25, axis=0); q75 = np.nanpercentile(data, 75, axis=0)
            ax.fill_between(T_GRID[valid], q25[valid], q75[valid], color=color, alpha=0.2, lw=0)
        ax.set_ylabel(ylabel, fontsize=8); ax.tick_params(labelsize=7); ax.grid(alpha=0.25, lw=0.4)

    axes[1, 0].set_xlabel("Normalised time", fontsize=8)
    axes[1, 1].set_xlabel("Normalised time", fontsize=8)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in PHASE_COLORS]
    fig.legend(handles, PHASE_LABELS, loc="lower center", ncol=4, fontsize=7.5, bbox_to_anchor=(0.5, -0.02), frameon=False)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig("../figures/fig_phases_4mm_2x2.pdf", bbox_inches="tight")
    print(f"n={n}; wrote figures/fig_phases_4mm_2x2.pdf")


if __name__ == "__main__":
    main()
