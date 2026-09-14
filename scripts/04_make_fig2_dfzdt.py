"""
04_make_fig2_dfzdt.py -- Reproduce Fig. 2 (median rate of change of feed
force around verified breakthrough, combined across both feed-axis subsets).

Run after 01_build_clean_dataset.py, from the scripts/ directory:
    python 04_make_fig2_dfzdt.py
Writes: figures/fig_dfzdt.pdf
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from common import (
    load_annotations, horizontal_feed_subset, vertical_feed_subset,
    load_hole, rolling_median, signed_feed_force,
)

T_GRID = np.linspace(-1.8, 0.6, 400)


def dfzdt_for_hole(row):
    f, o = load_hole(row)
    if f is None:
        return None
    fz = signed_feed_force(f)
    fz_s = rolling_median(fz, max(3, int(len(fz) * 0.06)))
    t_rel = f.t.values - row.end_time  # 0 = verified breakthrough
    dfzdt = np.gradient(fz_s, f.t.values)
    return np.interp(T_GRID, t_rel, dfzdt, left=np.nan, right=np.nan)


def main():
    ann = load_annotations()
    subsets = [horizontal_feed_subset(ann), vertical_feed_subset(ann)]
    curves = []
    for subset in subsets:
        for _, row in subset.iterrows():
            c = dfzdt_for_hole(row)
            if c is not None:
                curves.append(c)
    curves = np.array(curves)
    med = np.nanmedian(curves, axis=0)
    q25 = np.nanpercentile(curves, 25, axis=0)
    q75 = np.nanpercentile(curves, 75, axis=0)

    plt.rcParams.update({"font.size": 10, "font.family": "serif"})
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    valid = ~np.isnan(med)
    ax.plot(T_GRID[valid], med[valid], color="#1f77b4", lw=1.6)
    ax.fill_between(T_GRID[valid], q25[valid], q75[valid], color="#1f77b4", alpha=0.2, label="IQR")
    ax.axvline(0, color="red", ls="--", lw=1, label="Verified breakthrough")
    ax.axvline(-0.6, color="orange", ls=":", lw=1, label="Pre-breakthrough window (Table 2)")
    ax.set_xlabel("Time relative to verified breakthrough (s)")
    ax.set_ylabel("$dF_z/dt$ (N/s)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig("../figures/fig_dfzdt.pdf", bbox_inches="tight")
    print(f"n={len(curves)}; wrote figures/fig_dfzdt.pdf")


if __name__ == "__main__":
    main()
