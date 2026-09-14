"""
common.py -- Shared utilities for the drilling-data analysis pipeline.

Used by all numbered scripts in this repository. Implements:
  - loading and time-aligning the Force/Torque and OptiTrack CSV pairs for one hole
  - the boustrophedon-corrected file lookup (see README for background)
  - the four-phase model boundary detection (positioning / tip engagement /
    full engagement / breakthrough), anchored on the human-verified Start/End
    annotations
  - tool-tilt computation from the OptiTrack quaternion stream
"""

import glob
import os

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data_raw", "Bo_holes_copied")

# Six holes whose annotated axis did not match the dominant displacement
# direction on inspection (see paper Section 4.2); excluded from both
# feed-axis subsets throughout.
EXCLUDE_FILES = {
    "Bo4_P2_Force_20251205_B3.3.csv",
    "Bo1_P2_Force_20251205_B5.csv",
    "Bo18_P4_Force_20251205_B5.csv",
    "Bo13_P7_Force_20251205_B3.3.csv",
    "Bo2_P8_Force_20251205_B3.3.csv",
    "Bo12_P7_Force_20251205_B3.3.csv",
}


def rolling_median(x, win):
    """Centered rolling median, used throughout to denoise force/tilt traces
    without the phase lag of a rolling mean."""
    return pd.Series(x).rolling(win, center=True, min_periods=1).median().values


def find_hole_paths(row):
    """Resolve the Force and Opti CSV paths for one annotations.csv row."""
    pattern = os.path.join(
        DATA_DIR, f"P{row.plate}_V{row.versuch}_{row.thickness}mm", row.hole, row.file
    )
    matches = glob.glob(pattern)
    if not matches:
        return None, None
    return matches[0], matches[0].replace("Force", "Opti")


def load_hole(row):
    """Load and time-align one hole's Force and Opti streams onto a shared
    zero at the earlier of the two recordings' start times. Returns
    (force_df, opti_df) or (None, None) if the files are missing."""
    fp, op = find_hole_paths(row)
    if fp is None or not os.path.exists(op):
        return None, None
    f = pd.read_csv(fp).sort_values("timestamp").reset_index(drop=True)
    o = pd.read_csv(op).sort_values("timestamp").reset_index(drop=True)
    t0 = min(f.timestamp.min(), o.timestamp.min())
    f["t"] = f.timestamp - t0
    o["t"] = o.timestamp - t0
    return f, o


def quat_to_tilt(qx, qy, qz, qw):
    """Angle (deg) between the tool's body-frame z-axis and the world
    z-axis, i.e. the tool-tilt series used throughout the paper (Fig. 1's
    bottom panel, and the Controlled-entry tilt-rate test)."""
    zz = 1 - 2 * (qx**2 + qy**2)
    return np.degrees(np.arccos(np.clip(np.abs(zz), -1, 1)))


def signed_feed_force(f):
    """Fz sign varies by recording; the paper always reports the feed force
    as a positive magnitude (reaction force resisting tool advance)."""
    fz = f.Fz.values
    return -fz if np.nanmean(fz) < 0 else fz


def tip_full_boundary(f_t, fz_smooth, start_time, end_time):
    """The force-based sub-boundary separating tip engagement from full
    engagement (Section 4.3): the first point within [Start, End] at which
    smoothed feed force reaches 85% of its in-window maximum. Constrained to
    lie inside the human-verified window, so it is not affected by
    contact-detection uncertainty."""
    mask = (f_t >= start_time) & (f_t <= end_time)
    if mask.sum() == 0:
        return None, np.nan
    plateau = np.nanmax(fz_smooth[mask])
    thresh = 0.85 * plateau
    idxs = np.where(mask)[0]
    for i in idxs:
        if fz_smooth[i] >= thresh:
            return f_t[i], plateau
    return f_t[idxs[0]], plateau


def load_annotations(exclude_unusable=True):
    """Load annotations.csv from the repository root."""
    path = os.path.join(os.path.dirname(__file__), "..", "annotations.csv")
    ann = pd.read_csv(path)
    if exclude_unusable:
        ann = ann[
            (ann.usable == True)
            & ann.start_time.notna()
            & ann.end_time.notna()
        ].copy()
    return ann


def horizontal_feed_subset(ann):
    """P1/P3/P4, feed along the tracked pos_z axis (physically the
    horizontal-drilling setup; see Section 4.2 for the naming history)."""
    return ann[
        (ann.axis == "pos_z")
        & (~ann.plate.isin([5, 6]))
        & (~ann.file.isin(EXCLUDE_FILES))
    ].copy()


def vertical_feed_subset(ann):
    """P7/P8, feed along pos_x/pos_y (the vertical-drilling setup), 3.3mm
    bit only."""
    return ann[
        (ann.axis.isin(["pos_x", "pos_y"]))
        & (~ann.plate.isin([5, 6]))
        & (ann.diameter == 3.3)
        & (~ann.file.isin(EXCLUDE_FILES))
    ].copy()
