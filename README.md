# Chart scripts for: Mind the gaps: Analysing South African herbarium data with ParseGBIF reveals opportunities for biodiversity research

Python scripts used to produce the figures in the article

## Repository layout

```
data/      input CSV tables (see "Data" below)
figures/   generated PNG/TIFF figures (created automatically)
scripts/   one script per figure; scripts/common.py holds shared path handling
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Put the input CSVs in `data/`, then run any script from anywhere:

```bash
python scripts/ISpeciesPerYearChart.py
```

Figures are written to `figures/` as PNG (300 dpi) and TIFF.

Every script accepts the same options:

| Option | Meaning | Default |
|---|---|---|
| `--data-dir DIR` | folder containing the input CSV | `data/` |
| `--input FILE` | use this CSV file directly (overrides `--data-dir`) | see table below |
| `--out-dir DIR` | where to write figures | `figures/` |
| `--no-show` | save only; don't open a plot window | window opens |

Run all scripts without opening windows:

```bash
for f in scripts/[A-Za-z]*Chart*.py scripts/*Map*.py; do python "$f" --no-show; done
```

## Scripts, inputs and outputs

| Script | Input CSV (in `data/`) | Output (in `figures/`) | Figure in article |
|---|---|---|---|
| `ISpecimensPerYearChart.py` | `Table1-specimens_collectedPerYear.csv` | `occurrence_records_per_year_chart_b.{png,tiff}` | Fig. ? |
| `ISpecimensPerYearChartUnusable.py` | `Table1-specimens_collectedPerYear_percentageUnuseable.csv` | `unuseable_records_per_year_chart.{png,tiff}` | Fig. ? |
| `ISpeciesPerYearChart.py` | `Table2-species_collected_per_year.csv` | `species_records_per_year_chart.{png,tiff}` | Fig. ? |
| `ISpecimensPerMonthChart.py` | `Table3-specimens_collected_per_month.csv` | `specimen_records_per_month_chart.{png,tiff}` | Fig. ? |
| `ISpeciesPerMonthChart.py` | `Table4-species_collected_per_month.csv` | `species_records_per_month_chart.{png,tiff}` | Fig. ? |
| `ISAHerbariaSpecimensSpeciesChart.py` | `Table5_Herbarium_JoinedSA.csv` | `SA_herbarium_records_occurrence_records.{png,tiff}` | Fig. ? |
| `INonSAHerbariaSpecimensSpeciesChart.py` | `Table5_Herbarium_JoinedNonSA.csv` | `non_SA_herbarium_records_occurrence_records.{png,tiff}` | Fig. ? |
| `herbariaMap.py` | `Table5-HerbariumOR.csv` | `herbaria_world_map.png`, `herbaria_world_map_600dpi.tiff` | Fig. ? |
| `ISpecimensPerFamilyChart.py` | `Table8-families_specimens_total.csv` | `Occurrence_records_PerFamily_Top20_NoFamily.png`, `..._600dpi.tiff` | Fig. ? |
| `IMapsForFamilies.py` | `parseGBIF_top12_families_records_no_duplicates.csv` | `Map_01_<family>.png` … `Map_12_<family>.png` | Fig. ? |
| `SpecimensTaxaPerTopCollectorsChart.py` | `collectors_unique_taxa.csv` | `collectors_records_vs_pct_taxa.{png,tiff}` | Fig. ? |

Note: the map scripts use Cartopy, which downloads Natural Earth coastline/border
data on first run (internet connection required once).

## Data

DOI (https://doi.org/10.15468/dl.68eusb)
Data parsing and organisation: http://github.com/ianengelbrecht/parseGBIF

## Citation

If you use this code, please cite the article above.

## Licence

MIT, Copyright Hester Steyn 2026
