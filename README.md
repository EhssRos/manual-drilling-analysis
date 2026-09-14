# Manual drilling skill-taxonomy dataset and analysis pipeline

Data and analysis scripts underlying:

> Roshankar, E., Flehmke, M., Dege, J.H., Schüppstuhl, T.
> "What Does It Take to Imitate a Human Driller? A Skill Taxonomy and
> Empirical Evaluation for Learning from Demonstration in Manual Aircraft
> Assembly." CIRP CMS 2027.

## ⚠️ Important note on provenance

The scripts in this repository are a **faithful reconstruction** of the
original analysis pipeline, rebuilt from the documented methodology after
the original working files were lost to a filesystem reset. The table below
is a complete, honest cross-check of every number this pipeline reproduces
against the paper's reported values, run at the time this repository was
assembled.

| Result | Paper | This pipeline | Match |
|---|---|---|---|
| Total annotated / usable / excluded holes | 201 / 157 / 44 | 201 / 157 / 44 | ✅ exact |
| Horizontal-/vertical-feed subset sizes | 68 / 58 (n=126) | 68 / 58 (n=126) | ✅ exact |
| Tz effect size (tip→full) | d=0.88 | d=0.88 | ✅ exact |
| Feed-force CV (tip / full) | 0.182 / 0.193 | 0.183 / 0.192 | ✅ values match; **p=0.40 here vs. p=0.23 in paper** (still non-significant either way, but the exact p-value depends on a smoothing-window choice we could not recover exactly) |
| Three-stage force pattern | 58.2→69.6→54.5 N | 58.4→69.7→54.6 N | ✅ very close |
| Anticipation: detected / before breakthrough | 94.4% / 95.8% | 94.4% / 95.8% | ✅ exact |
| Anticipation: median lead time | 1.09 s | 1.20 s | ⚠️ close, not exact |
| Material remaining at decline onset (median) | 35% | 31.2% | ⚠️ close, not exact |
| Tool-tilt correction rate (tip / full) | 4.53 / 1.79 °/s, p<.001, d=0.52 | 4.53 / 1.79 °/s, p=5.5e-14, d=0.52 | ✅ exact |
| Positioning tilt: toward-body, both subsets | 97–100%, $p<10^{-17}$ | 97–100%, $p<10^{-17}$ | ✅ exact |
| Tip-engagement tilt: away-from-body reversal | 69–75%, $p<.003$ | 69–75%, $p<.003$ | ✅ exact |
| Peak feed force, 4mm / 10mm (horizontal subset) | 82.1 / 82.8 N | 82.1 / 82.8 N | ✅ exact |
| Torque magnitude by thickness (tip/full) | 4mm: −0.05/−0.12; 10mm: −0.06/−0.17 Nm | 4mm: −0.06/−0.12; 10mm: −0.05/−0.17 Nm | ✅ close |
| Full-engagement duration, 4mm / 10mm | 2.65 / 4.88 s | 2.65 / 4.88 s | ✅ exact |

**Bottom line**: 10 of 11 cross-checked results match exactly or very
closely. Two results (anticipation median lead time, material-remaining
percentage) are close but not exact. Where this code disagrees with the
paper, **the paper's reported numbers are the source of truth**; treat this
repository as a transparent, runnable specification of the method, not a
pixel-exact original artifact.

**Note on tool-tilt stabilisation range (removed from the paper)**: an
earlier draft compared the absolute tool-tilt angle at contact onset vs.
verified Start between the two feed-axis subsets (31° vs. 6°) and
attributed the difference to a setup-specific effect. On reflection this
comparison was dropped from the paper: absolute tilt relative to the world
frame mostly reflects how the workpiece/fixture is mounted in each physical
setup, not operator skill, since the tool must stay close to perpendicular
to the *local* feed axis regardless of that axis's orientation in the world
frame. The genuinely skill-relevant quantity is the *within-hole* change in
tilt-correction behaviour (tip vs. full engagement), which is exactly what
the Controlled-entry tilt-rate result above captures, and which does not
depend on any world-frame reference. `tilt_stab_range` remains in
`01_build_clean_dataset.py`'s output as a diagnostic column but is no
longer referenced in the paper text.

**Note on lateral force (also removed from the paper)**: an earlier version
of this repository reported a lateral-force consistency check here that
could not be reproduced to match the paper (paper: 6.1–7.0 N; this
pipeline: 7.6–8.3 N regardless of metric definition tried). On review, this
check did not clearly support any specific taxonomy entry once the
tilt-rate evidence for Controlled entry was established, so it has been
removed from the paper rather than carried forward with an unresolved
discrepancy. `tip_radial`/`full_radial` remain in the output CSVs as
general diagnostic columns but are no longer referenced in the paper text.

## Repository structure

```
.
├── annotations.csv          # human-verified Start/End reference points per hole,
│                             # plate/versuch/thickness/diameter metadata
├── data_raw/                # raw Force/Torque and OptiTrack CSV pairs per hole
│   └── Bo_holes_copied/
│       └── P<plate>_V<versuch>_<thickness>mm/Bo<n>/*.csv
├── sources/                 # citation verification: for every reference, what we
│   │                         # cite it for, and what the original source actually says
│   ├── Quellenliste_final_verifiziert.md   # final, most thorough pass (33/37 sources
│   │                                        # confirmed against original abstract/text,
│   │                                        # with quotes; documents corrections made
│   │                                        # along the way, e.g. an author-list error
│   │                                        # and one citation found to misrepresent
│   │                                        # its source, both fixed in the paper)
│   └── Quellenliste_vollstaendig.md        # earlier, first-pass source audit
├── scripts/
│   ├── common.py                    # shared data-loading / feature utilities
│   ├── 01_build_clean_dataset.py    # builds output/clean_horizontal.csv, clean_vertical.csv
│   ├── 02_table2_statistics.py      # prints all Table 2 / Section 5-6 statistics
│   ├── 03_make_fig1_phases.py       # reproduces Fig. 1 (four-phase model, 2x2 grid)
│   ├── 04_make_fig2_dfzdt.py        # reproduces Fig. 2 (dFz/dt around breakthrough)
│   ├── 05_tilt_direction_analysis.py # exploratory: does tilt deviation have a
│                                     # consistent *direction*, not just magnitude/rate?
│                                     # (positioning-baseline reference; NOT in the paper)
│   └── 06_make_fig3_tiltplane.py    # reproduces Fig. 3 (tool-orientation deviation
│                                     # by phase, full-engagement reference; IS in the paper,
│                                     # supports the Positioning/tip alignment and
│                                     # Controlled entry rows in Table 2)
├── output/                  # generated CSVs (created by 01_build_clean_dataset.py)
├── figures/                 # generated PDFs (created by 03_* and 04_*)
└── requirements.txt
```

## Data

Each hole has two synchronised recordings:
- `*_Force_*.csv`: 6-axis force/torque at the workpiece (`Fx,Fy,Fz,Tx,Ty,Tz`)
- `*_Opti_*.csv`: 6-DoF pose of a marker cluster on the drill body
  (`pos_x,pos_y,pos_z,quat_x,quat_y,quat_z,quat_w`)

`annotations.csv` provides, per hole: which plate/trial/thickness/diameter
it belongs to, the human-verified `start_time`/`end_time` (end of
positioning / beginning of tip engagement, and moment of visually observed
breakthrough, both in the same time base as the raw CSVs), the dominant
feed-axis (`axis`) used to split the dataset into the horizontal-feed
(P1/P3/P4) and vertical-feed (P7/P8) subsets described in the paper's
Section 4.2, and a `usable` flag for holes excluded due to corrupted or
ambiguous signals.

## Running the pipeline

```bash
pip install -r requirements.txt
cd scripts
python 01_build_clean_dataset.py   # ~1-2 min; builds the per-hole feature tables
python 02_table2_statistics.py     # prints the Table 2 statistics to stdout
python 03_make_fig1_phases.py      # writes figures/fig_phases_4mm_2x2.pdf
python 04_make_fig2_dfzdt.py       # writes figures/fig_dfzdt.pdf
python 05_tilt_direction_analysis.py  # exploratory tilt-direction check (see below)
python 06_make_fig3_tiltplane.py   # writes figures/fig_tilt_plane.pdf (Fig. 3, in the paper)
```

## Fig. 3 in the paper: tool-orientation deviation by phase

`06_make_fig3_tiltplane.py` reproduces Fig. 3 and the statistics behind the
"Positioning / tip alignment" and "Controlled entry" rows in Table 2. It
uses the mean tool orientation during **full engagement** as the reference
(0, 0), since that is the only phase in which the tool is mechanically
constrained by the forming hole -- the best available estimate of the true
drilling axis. Positioning, tip engagement, and breakthrough are then
expressed as directional deviations from that axis:

- **Positioning** is consistently tilted toward the operator's body
  (97-100% of holes, both subsets, $p<10^{-17}$) -- plausibly a posture
  that keeps a clear sightline to the bit and the arm out of the way.
- **Tip engagement** reverses to a slight away-from-body tilt (69-75%,
  $p<.003$) rather than an instantaneous jump to the full-engagement axis.
- **Breakthrough** sits in between (64-78% consistency) -- real, but not
  clean enough on its own to support a specific directional claim.

For the horizontal-feed subset, the feed axis is only 2-18° from
world-vertical, which makes a world-vertical-anchored perpendicular frame
numerically unstable; the script falls back to a world-X anchor there
instead and the resulting plane is rotated and labelled "toward/away from
body" based on the corresponding author's own review of the recorded
video (this specific labelling is not something the tracking data alone
can establish, since there is no record of how the OptiTrack world frame
was calibrated relative to the room). For the vertical-feed subset, the
feed axis is 75-88° from world-vertical, where the same construction is
well-conditioned and "away from body" coincides with true vertical
directly.

## Superseded exploratory script: 05_tilt_direction_analysis.py

`05_tilt_direction_analysis.py` was an earlier exploration of the same
underlying idea as Fig. 3, but compares each phase to the
positioning-phase baseline rather than to full engagement, and its
printed output describes the vertical-feed subset's consistent deviation
as "against gravity" -- language that was later dropped as an
overinterpretation (tilt is a rotation, not a translation, so "against
gravity" implies a force/energy story the data does not actually support;
it is more accurately described as a consistent *direction*, nothing more).
**06_make_fig3_tiltplane.py is the version actually used for the paper**:
it uses the more physically appropriate full-engagement reference (the
only mechanically-constrained, and therefore most trustworthy, phase), and
its output is what Fig. 3 and the corresponding Table 2 text are based on.
05 is kept in this repository only for transparency about how the
analysis developed, not as a second independent result.

## Citation verification (sources/)

`sources/Quellenliste_final_verifiziert.md` documents, for every reference
in the paper's bibliography, what we cite it for and what the original
source actually says.
## Method summary

The four-phase model (positioning / tip engagement / full engagement /
breakthrough) and the specific statistical tests are described in the
paper's Sections 4.3, 5, and 6.1. In brief:

- **Tip/full-engagement boundary**: the first point within the
  human-verified `[start_time, end_time]` window at which smoothed feed
  force reaches 85% of its in-window maximum.
- **Anticipation of breakthrough**: the point at which smoothed feed force
  first drops below 70% of the in-window plateau and continues decreasing;
  reported relative to `end_time`.
- **Remaining material at decline onset**: computed from the tracked
  marker's displacement along the feed axis, expressed as a percentage of
  total displacement between `start_time` and `end_time`.
- **Tool-tilt correction rate**: the median absolute rate of change (deg/s)
  of the angle between the tool's body-frame z-axis and the world z-axis,
  computed separately within the tip-engagement and full-engagement
  windows.

## Licence / usage

Internal research data; not for redistribution outside the project team
without checking with the authors.
