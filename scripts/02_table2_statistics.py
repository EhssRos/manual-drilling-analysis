"""
02_table2_statistics.py -- Print the Table 2 / Section 5-6 summary statistics
from the cleaned dataset built by 01_build_clean_dataset.py.

Run after 01_build_clean_dataset.py, from the scripts/ directory:
    python 02_table2_statistics.py
"""

import numpy as np
import pandas as pd
from scipy import stats


def cohens_d_paired(x, y):
    diff = x - y
    return diff.mean() / diff.std(ddof=1)


def main():
    h = pd.read_csv("../output/clean_horizontal.csv")
    v = pd.read_csv("../output/clean_vertical.csv")
    allp = pd.concat([h, v], ignore_index=True)
    print(f"Combined n = {len(allp)} (horizontal n={len(h)}, vertical n={len(v)})\n")

    print("--- Controlled force dosage ---")
    sub = allp.dropna(subset=["Tz_tip", "Tz_full"])
    d = cohens_d_paired(sub.Tz_tip, sub.Tz_full)
    print(f"Tz tip={sub.Tz_tip.mean():.3f} full={sub.Tz_full.mean():.3f} Nm, d={d:.2f}")

    sub = allp.dropna(subset=["tip_cv", "full_cv"])
    t, p = stats.wilcoxon(sub.tip_cv, sub.full_cv)
    d = cohens_d_paired(sub.tip_cv, sub.full_cv)
    print(f"Feed-force CV tip={sub.tip_cv.mean():.3f} full={sub.full_cv.mean():.3f}, "
          f"Wilcoxon p={p:.3f}, d={d:.2f}")

    sub = allp.dropna(subset=["tip_f", "rest_full_f", "pre_bt_f"])
    t1, p1 = stats.wilcoxon(sub.tip_f, sub.rest_full_f)
    t2, p2 = stats.wilcoxon(sub.rest_full_f, sub.pre_bt_f)
    d1 = cohens_d_paired(sub.tip_f, sub.rest_full_f)
    d2 = cohens_d_paired(sub.rest_full_f, sub.pre_bt_f)
    print(f"Three-stage force: {sub.tip_f.mean():.1f} -> {sub.rest_full_f.mean():.1f} "
          f"-> {sub.pre_bt_f.mean():.1f} N; transitions p={p1:.1e}/{p2:.1e}, d={d1:.2f}/{d2:.2f}")

    print("\n--- Anticipation of breakthrough ---")
    sub = allp.dropna(subset=["anticipation_s"])
    pct_detect = len(sub) / len(allp) * 100
    before = sub[sub.anticipation_s > 0]
    pct_before = len(before) / len(sub) * 100
    print(f"Detected: {len(sub)}/{len(allp)} ({pct_detect:.1f}%); "
          f"before breakthrough: {pct_before:.1f}%; median lead = {before.anticipation_s.median():.2f}s")

    sub = allp.dropna(subset=["frac_remaining"])
    print(f"Material remaining at decline onset: median={sub.frac_remaining.median():.1f}%, "
          f"IQR=[{sub.frac_remaining.quantile(.25):.1f}, {sub.frac_remaining.quantile(.75):.1f}]")

    print("\n--- Controlled entry (tool-tilt correction rate) ---")
    sub = allp.dropna(subset=["tip_tilt_rate", "full_tilt_rate"])
    t, p = stats.wilcoxon(sub.tip_tilt_rate, sub.full_tilt_rate)
    d = cohens_d_paired(sub.tip_tilt_rate, sub.full_tilt_rate)
    print(f"Tilt-correction rate tip={sub.tip_tilt_rate.median():.2f} "
          f"full={sub.full_tilt_rate.median():.2f} deg/s, Wilcoxon p={p:.2e}, d={d:.2f}")

    print("\n--- Cross-condition checks (Section 5, 'beyond taxonomy entries') ---")
    for label, df in [("horizontal", h), ("vertical", v)]:
        sub = df.dropna(subset=["tip_dur", "full_dur"])
        print(f"{label}: median tip_dur={sub.tip_dur.median():.2f}s, "
              f"full_dur={sub.full_dur.median():.2f}s")


if __name__ == "__main__":
    main()
