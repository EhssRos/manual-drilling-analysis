"""
01_build_clean_dataset.py -- Build the per-hole feature table used by every
downstream script and reported in the paper's Table 2 / Section 5-6.

For every usable, annotated hole in both feed-axis subsets, computes:
  - tip/full-engagement mean feed force, torque about the feed axis (Tz),
    and feed-force coefficient of variation
  - the three-stage force pattern values (tip / early-full / pre-breakthrough)
  - breakthrough-anticipation timing (force-decline onset relative to the
    verified End point) and the remaining-material-thickness check used to
    rule out a purely mechanical explanation (Section 6.1)
  - tool-tilt correction rate during tip vs. full engagement (the
    Controlled-entry evidence in Table 2)
  - lateral (radial) force during tip/full engagement
  - phase durations

Run from the scripts/ directory:  python 01_build_clean_dataset.py
Writes: output/clean_horizontal.csv, output/clean_vertical.csv
"""

import numpy as np
import pandas as pd

from common import (
    load_annotations,
    load_hole,
    horizontal_feed_subset,
    vertical_feed_subset,
    rolling_median,
    signed_feed_force,
    tip_full_boundary,
    quat_to_tilt,
)


def process_hole(row):
    f, o = load_hole(row)
    if f is None:
        return None

    fz = signed_feed_force(f)
    fz_s = rolling_median(fz, max(3, int(len(fz) * 0.06)))

    t_sub, plateau = tip_full_boundary(f.t.values, fz_s, row.start_time, row.end_time)
    if t_sub is None or np.isnan(plateau):
        return None

    def mean_in(t0, t1, series_t, series_v):
        m = (series_t >= t0) & (series_t <= t1)
        return np.nanmean(series_v[m]) if m.sum() > 0 else np.nan

    def cv_in(t0, t1):
        # CV auf ungeglaettetem Signal (starke Glaettung reduziert die
        # Standardabweichung kuenstlich und verzerrt CV nach unten)
        m = (f.t.values >= t0) & (f.t.values <= t1)
        seg = fz[m]
        if len(seg) < 3 or np.nanmean(seg) == 0:
            return np.nan
        return np.nanstd(seg) / np.nanmean(seg)

    tip_f = mean_in(row.start_time, t_sub, f.t.values, fz_s)
    full_f = mean_in(t_sub, row.end_time, f.t.values, fz_s)
    tip_cv = cv_in(row.start_time, t_sub)
    full_cv = cv_in(t_sub, row.end_time)

    # Vorschubkraft im letzten 0.5s-Fenster vor Ende (dritte Stufe des
    # Drei-Stufen-Musters)
    pre_bt_mask = (f.t.values >= row.end_time - 0.5) & (f.t.values <= row.end_time)
    pre_bt_f = np.nanmean(fz_s[pre_bt_mask]) if pre_bt_mask.sum() > 0 else np.nan
    # "rest_full" = full engagement, ohne das letzte 0.5s-Fenster
    rest_full_mask = (f.t.values >= t_sub) & (f.t.values <= row.end_time - 0.5)
    rest_full_f = np.nanmean(fz_s[rest_full_mask]) if rest_full_mask.sum() > 0 else np.nan

    Tz_tip = mean_in(row.start_time, t_sub, f.t.values, rolling_median(f.Tz.values, 5))
    Tz_full = mean_in(t_sub, row.end_time, f.t.values, rolling_median(f.Tz.values, 5))

    # Spitzenkraft im gesamten Start-Ende-Fenster
    win_mask = (f.t.values >= row.start_time) & (f.t.values <= row.end_time)
    peak_f = np.nanmax(fz_s[win_mask]) if win_mask.sum() > 0 else np.nan

    # Kontaktbeginn: letzter Punkt vor Start, an dem Kraft < 5% Plateau war
    # (gleiche Definition wie in 03_make_fig1_phases.py)
    pre_mask = f.t.values <= row.start_time
    pre_idx = np.where(pre_mask)[0]
    contact_t = row.start_time - 1.0
    contact_thresh = 0.05 * plateau
    for i in reversed(pre_idx):
        if fz_s[i] < contact_thresh:
            contact_t = f.t.values[i]
            break

    # Verkippung (fuer Stabilisierungsbereich UND Aenderungsrate gemeinsam
    # berechnet)
    tilt = quat_to_tilt(o.quat_x.values, o.quat_y.values, o.quat_z.values, o.quat_w.values)
    tilt_s = rolling_median(tilt, 5)

    # Tool-Tilt-Stabilisierungsbereich: Differenz zwischen dem Wert am
    # Kontaktbeginn (vor Start) und dem Wert bei Start selbst -- Grundlage
    # fuer den Cross-Condition-Check in Section 5 ("beyond taxonomy entries")
    tilt_stab_range = abs(np.interp(contact_t, o.t.values, tilt_s) - np.interp(row.start_time, o.t.values, tilt_s))

    radial = np.sqrt(f.Fx.values ** 2 + f.Fy.values ** 2)
    radial_s = rolling_median(radial, 5)
    tip_radial = mean_in(row.start_time, t_sub, f.t.values, radial_s)
    full_radial = mean_in(t_sub, row.end_time, f.t.values, radial_s)

    # Verkippungs-Aenderungsrate (Controlled-entry-Evidenz, Tabelle 2)
    dt = np.diff(o.t.values)
    dtilt = np.abs(np.diff(tilt_s)) / np.clip(dt, 1e-6, None)
    t_mid = o.t.values[1:]

    def rate_in(t0, t1):
        m = (t_mid >= t0) & (t_mid <= t1)
        return np.nanmedian(dtilt[m]) if m.sum() >= 3 else np.nan

    tip_tilt_rate = rate_in(row.start_time, t_sub)
    full_tilt_rate = rate_in(t_sub, row.end_time)

    # Kraftabfall-Beginn relativ zum verifizierten Ende (Anticipation) + wie
    # viel Restmaterial zu diesem Zeitpunkt noch uebrig ist (Section 6.1)
    decline_t = find_force_decline_onset(f.t.values, fz_s, row.start_time, plateau)
    anticipation = row.end_time - decline_t if decline_t is not None else np.nan

    frac_remaining = np.nan
    depth_end = np.nan
    if decline_t is not None:
        pz = rolling_median(o.pos_z.values, 7) if "pos_z" in o.columns else None
        if pz is not None:
            pz_start = np.interp(row.start_time, o.t.values, pz)
            pz_end = np.interp(row.end_time, o.t.values, pz)
            pz_decline = np.interp(decline_t, o.t.values, pz)
            sign = 1 if (pz_end - pz_start) > 0 else -1
            depth_end = (pz_end - pz_start) * sign * 1000
            depth_decline = (pz_decline - pz_start) * sign * 1000
            if depth_end > 0:
                frac_remaining = 100 * (depth_end - depth_decline) / depth_end

    return dict(
        file=row.file, plate=row.plate, thickness=row.thickness, diameter=row.diameter,
        tip_f=tip_f, rest_full_f=rest_full_f, pre_bt_f=pre_bt_f, plateau=plateau,
        peak_f=peak_f, tilt_stab_range=tilt_stab_range,
        tip_cv=tip_cv, full_cv=full_cv,
        Tz_tip=Tz_tip, Tz_full=Tz_full,
        tip_radial=tip_radial, full_radial=full_radial,
        tip_tilt_rate=tip_tilt_rate, full_tilt_rate=full_tilt_rate,
        anticipation_s=anticipation, frac_remaining=frac_remaining,
        depth_end_mm=depth_end,
        tip_dur=t_sub - row.start_time, full_dur=row.end_time - t_sub,
    )


def find_force_decline_onset(t, fz_smooth, search_from_t, plateau_ref, win=5):
    """First point after search_from_t at which feed force has dropped below
    70% of the in-window plateau and is still decreasing over the next `win`
    samples. This is the force-decline-onset definition used for the
    anticipation result (Table 2, Fig. 2)."""
    idxs = np.where(t >= search_from_t)[0]
    for i in idxs:
        if i + win >= len(fz_smooth):
            break
        window = fz_smooth[i:i + win]
        if window[-1] < 0.7 * plateau_ref and np.mean(np.diff(window)) < 0:
            return t[i]
    return None


def build(subset_rows, label):
    rows = []
    for _, row in subset_rows.iterrows():
        result = process_hole(row)
        if result is not None:
            rows.append(result)
    df = pd.DataFrame(rows)
    print(f"{label}: n={len(df)}")
    return df


if __name__ == "__main__":
    ann = load_annotations()
    horiz = build(horizontal_feed_subset(ann), "horizontal-feed")
    vert = build(vertical_feed_subset(ann), "vertical-feed")
    horiz.to_csv("../output/clean_horizontal.csv", index=False)
    vert.to_csv("../output/clean_vertical.csv", index=False)
    print("Wrote output/clean_horizontal.csv, output/clean_vertical.csv")
