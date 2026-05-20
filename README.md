# Climate Risk & Homelessness in New Jersey
### A Public Data Analysis | Phase 1 of 2

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Data: HUD](https://img.shields.io/badge/Data-HUD%20Exchange-blue)](https://www.hudexchange.info/)
[![Data: NASA SEDAC](https://img.shields.io/badge/Data-NASA%20SEDAC-lightgrey)](https://sedac.ciesin.columbia.edu/)
[![Status: In Progress](https://img.shields.io/badge/Status-In%20Progress-yellow)]()

---

## Overview

This project investigates whether climate change measurably worsens the structural
conditions that produce and sustain homelessness across New Jersey's Continuums of
Care (CoCs). It is built entirely on publicly available data and designed to be fully
reproducible by any researcher, policy analyst, or CoC partner.

**This is Phase 1.** Phase 2 — currently in proposal — integrates operational HMIS
aggregate data and By-Name List (BNL) exports to move from structural risk analysis
to real-time individual-level vulnerability mapping. See [Phase 2 Roadmap](#phase-2-roadmap).

> **Status:** Phase 1 — Data acquisition and EDA (Summer 2026)

---

## The Question

> After controlling for poverty and housing cost burden, do climate variables —
> extreme heat days, flood events, annual temperature anomaly — predict worse
> homelessness outcomes across NJ CoCs year over year?

---

## Why This Matters

New Jersey's CoCs shelter and serve thousands of people experiencing homelessness
annually. Climate change is not an abstract future risk for this population — it is
a current operational pressure:

- **Extreme heat** drives unsheltered individuals into emergency cooling centers,
  overwhelming shelter systems not designed for weather surges
- **Flooding** (a chronic risk in coastal and riverine NJ) displaces housed people
  into homelessness and destroys transitional housing stock
- **Urban heat islands** concentrate both climate exposure and housing instability
  in the same zip codes

This analysis maps where those pressures are highest, which CoCs are most exposed,
and what the structural data already signals — before any individual-level data is
needed to see the pattern.

---

## Project Architecture

This project runs across two environments with distinct roles:

| Layer | Label | Purpose |
|-------|-------|---------|
| **PKM / Documentation** | PKM (M3) | Notes, project planning, writing |
| **Execution / Code** | Execution (P52s) | Data pipeline, notebooks, model training, git repo |

### Repository Structure (Execution — P52s)

```
nj-climate-homelessness/
│
├── README.md
├── LICENSE
├── requirements.txt
├── environment.yml
│
├── data/
│   ├── raw/                    # Downloaded source files (not committed — see data/raw/README.md)
│   ├── interim/                # Mid-pipeline intermediates, safe to regenerate
│   ├── processed/              # Cleaned, model-ready panel dataset
│   ├── external/               # Reference shapefiles, crosswalks, lookup tables
│   └── README.md               # Data sources, download instructions, licenses
│
├── notebooks/
│   ├── 01_pit_baseline.ipynb           # HUD PIT trend analysis (2013–2024)
│   ├── 02_climate_exposure_map.ipynb   # SEDAC + NOAA + FEMA geographic analysis
│   ├── 03_regression_climate_pit.ipynb # Panel regression: climate → PIT delta
│   ├── 04_county_risk_classification.ipynb  # K-means county risk tiering
│   └── 05_final_report_figures.ipynb   # Publication-ready visualizations
│
├── src/
│   ├── data_loaders.py         # Functions for loading HUD, NOAA, SEDAC data
│   ├── make_dataset.py         # End-to-end pipeline entry point
│   ├── build_features.py       # Feature engineering: county-level matrix assembly
│   ├── crosswalk.py            # County ↔ CoC boundary crosswalk utility
│   ├── train.py                # Model training and cross-validation
│   ├── evaluate.py             # Metrics, feature importance, residual analysis
│   └── viz.py                  # Reusable visualization and map functions
│
├── models/                     # Serialized model artifacts (.pkl, .joblib)
│
├── reports/
│   ├── NJ_Climate_Homelessness_Phase1.md   # Full written report
│   ├── figures/                            # Exported charts and maps
│   └── tables/                             # Summary statistics tables
│
├── docs/
│   └── data_sources.md         # Detailed per-source download and license notes
│
├── tests/                      # Unit tests for src/ modules
├── .env.example                # API key template (never commit .env)
└── .gitignore
```

---

## Data Sources

All data used in this project is publicly available and free to access.

| Source | Contents | URL |
|--------|----------|-----|
| HUD PIT Count (2013–2024) | Annual sheltered + unsheltered counts by CoC | [HUD Exchange](https://www.hudexchange.info/programs/coc/coc-homeless-populations-and-subpopulations-reports/) |
| HUD Housing Inventory Count | Annual shelter bed capacity by CoC | [HUD Exchange](https://www.hudexchange.info/programs/coc/coc-homeless-populations-and-subpopulations-reports/) |
| HUD System Performance Measures | Length of homelessness, exits to housing, returns by CoC | [HUD Exchange](https://www.hudexchange.info/programs/coc/coc-performance-measures/) |
| NASA SEDAC — SVI | Social vulnerability index by county | [SEDAC](https://sedac.ciesin.columbia.edu/) |
| NASA SEDAC — Urban Heat Island | Surface temperature differentials, urban cores | [SEDAC](https://sedac.ciesin.columbia.edu/) |
| NOAA Storm Events | Extreme heat events, floods, hurricanes by county | [NCDC](https://www.ncdc.noaa.gov/stormevents/) |
| NOAA Climate at a Glance | Annual temperature anomaly, NJ statewide | [NCEI](https://www.ncei.noaa.gov/cag/) |
| FEMA Flood Map | 100/500-year floodplain boundaries | [MSC](https://msc.fema.gov/) |
| CDC Social Vulnerability Index | County-level composite vulnerability score | [ATSDR](https://www.atsdr.cdc.gov/placeandhealth/svi/) |
| U.S. Census ACS 5-Year | Poverty rate, rent burden, vacancy by county | [Census Bureau](https://data.census.gov/) |
| NJ County / CoC Boundaries | Shapefiles for spatial joins | [HUD EGIS](https://hudgis-hud.opendata.arcgis.com/) / [NJ OIT](https://njogis-newjersey.opendata.arcgis.com/) |

> **Downloading data:** See [`data/README.md`](data/README.md) for step-by-step
> download instructions. No API keys required for Phase 1 except NASA Earthdata
> (free account). See [`.env.example`](.env.example) for credential setup.

**Raw data is not committed to this repo.** All files in `data/raw/` are
documented by source, URL, and pull date so the dataset can be fully reproduced.

---

## Methods

### Panel Dataset Structure

The core analytical dataset is a panel structured as one observation per CoC per
year. Variables include:

- **Outcome:** Year-over-year change in unsheltered PIT count per CoC
- **Climate features:** Annual extreme heat days, flood events, average temperature
  anomaly (county-level, crosswalked to CoC)
- **Housing features:** HIC beds per capita, rent burden, vacancy rate
- **Socioeconomic controls:** Poverty rate, CDC SVI composite score

### Analysis Pipeline

1. **Baseline (Notebook 01):** Time series of PIT and HIC trends across all NJ CoCs, 2013–2024
2. **Geographic exposure (Notebook 02):** Choropleth mapping of climate and social vulnerability across NJ counties with CoC boundary overlay
3. **Regression (Notebook 03):** Multivariate panel regression with cross-validation, testing whether climate variables explain PIT variance beyond socioeconomic controls
4. **Classification (Notebook 04):** K-means clustering of NJ counties into HIGH / MEDIUM / LOW climate-homelessness risk tiers
5. **Reporting (Notebook 05):** Final figures and maps for the written report

### Modeling Approach

- **Baseline:** Linear regression, Ridge/Lasso regularization
- **Primary:** Random Forest (scikit-learn)
- **Validation:** Time-series cross-validation — no data leakage across years

### Key Methodological Constraints

- Annual PIT data limits temporal resolution — month-to-month dynamics during heat
  events are not visible at this scale
- County ↔ CoC boundary crosswalk introduces spatial measurement error, documented
  in `src/crosswalk.py`
- PIT Count systematically undercounts unsheltered individuals during adverse weather
  — the population most exposed to climate events is hardest to enumerate on the
  coldest or hottest nights
- ~99 panel observations (9 CoCs × 11 years) support exploratory association
  analysis; findings are framed as association evidence, not causal claims

---

## 10-Week Timeline (Summer 2026)

| Week | Phase | Milestone |
|------|-------|-----------|
| 1–2 | Data acquisition | All sources downloaded, `data/raw/` fully documented |
| 3–4 | EDA | Notebooks 01–02 complete; distributions and missingness understood |
| 5 | Feature engineering | County-level feature matrix assembled, CoC crosswalk validated |
| 6–7 | Baseline modeling | Regression and Random Forest benchmarks with cross-validation |
| 8 | Evaluation | Feature importance, residual analysis, county-level error map |
| 9 | Visualization | Choropleth maps, trend charts, summary tables |
| 10 | Write-up | Phase 1 report draft + README finalized |

---

## Key Findings (Phase 1 — Preliminary)

> *Updated as analysis progresses through Summer 2026*

- [ ] NJ CoC PIT trend analysis complete
- [ ] County climate exposure map complete
- [ ] Panel regression results
- [ ] County risk tier classification
- [ ] Final report published

---

## Setup and Reproduction

### Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/nj-climate-homelessness.git
cd nj-climate-homelessness
```

### Option A — Miniforge / Mamba

```bash
mamba env create -f environment.yml
conda activate nasa_sds
nbstripout --install            # strips notebook outputs before commits
```

### Option B — pip

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nbstripout --install
```

### Configure credentials

```bash
cp .env.example .env
# Add your NASA Earthdata username and password
```

### Download raw data

Follow [`data/README.md`](data/README.md) for per-source instructions.
Place all files in `data/raw/` exactly as specified.

### Run the pipeline

```bash
python src/make_dataset.py   # cleans and merges all sources → data/processed/
jupyter lab notebooks/       # run notebooks in order (01 → 05)
```

---

## Dependencies

```yaml
# environment.yml
name: nasa_sds
channels:
  - conda-forge
dependencies:
  - python=3.11
  - numpy
  - pandas>=2.2
  - scipy
  - matplotlib
  - seaborn
  - scikit-learn>=1.4
  - geopandas>=0.14
  - shapely>=2.0
  - pyproj
  - rasterio          # GeoTIFF / gridded climate data
  - xarray            # NOAA NetCDF (.nc) files
  - netcdf4
  - folium            # Interactive NJ CoC maps
  - jupyter
  - nbstripout        # Strip notebook outputs before git commit
  - python-dotenv
  - tqdm
  - requests
```

Full pip list: [`requirements.txt`](requirements.txt)

---

## Phase 2 Roadmap

Phase 1 demonstrates what is visible in public structural data. Phase 2 moves from
structural risk to operational integration by incorporating:

| Data Source | What It Adds |
|-------------|-------------|
| HMIS aggregate monthly reports | Monthly inflow/outflow — makes seasonal climate-surge dynamics visible |
| By-Name List (BNL) aggregate exports | Individual-level vulnerability flags — identifies who in the active homeless population is in flood zones, lacks cooling access, or has prior weather-related shelter entries |
| Real-time shelter utilization | Actual vs. capacity ratios during extreme heat and flood events |

**Phase 2 research questions:**
- Do monthly HMIS inflows spike during and after extreme heat events and flooding in high-risk CoCs?
- Can a climate vulnerability flag on the BNL be operationalized to prioritize outreach *before* weather events rather than during them?
- What is the lag between a major climate event and a detectable inflow spike in HMIS data?

> Phase 2 requires data sharing agreements with participating New Jersey Continuums
> of Care and HMIS leads. If you work in NJ homelessness services and are interested
> in collaboration, see [Contact](#contact).

---

## About the Author

**Robert Houston** is a homelessness prevention professional in New Jersey with
domain expertise in By-Name Lists, Point-in-Time Counts, Coordinated Entry, and
the Built for Zero methodology. This project bridges professional practice with
quantitative analysis at the intersection of public data, applied mathematics, and
social systems modeling.

---

## License

This project is licensed under the MIT License. All source data retains its original
licensing terms — see [`data/README.md`](data/README.md) for details.

---

## Contact

**Robert Houston**
📧 [your email]
🔗 [your LinkedIn]

> *If you are an HMIS lead, CoC coordinator, or data manager interested in
> Phase 2 collaboration, please reach out.*

---

## Acknowledgments

Public data provided by the HUD Office of Community Planning and Development,
NASA Socioeconomic Data and Applications Center (SEDAC), NOAA National Centers
for Environmental Information, FEMA, the CDC Agency for Toxic Substances and
Disease Registry, and the U.S. Census Bureau.
