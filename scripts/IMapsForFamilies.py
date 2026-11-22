# --------------------------------------------------------------
#  INDIVIDUAL MAPS – ONE PER TOP-12 families (12 MAPS TOTAL)
# --------------------------------------------------------------

import os
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from common import parse_args

# ------------------------------------------------------------------
# 1. PATHS (see `python IMapsForFamilies.py --help`)
# ------------------------------------------------------------------
args = parse_args("One distribution map per top-12 family.",
                  "parseGBIF_top12_families_records_no_duplicates.csv")
csv_path = args.input
output_folder = args.out_dir

# ------------------------------------------------------------------
# 2. LOAD & RENAME COLUMNS
# ------------------------------------------------------------------
df = pd.read_csv(csv_path)

# Strip whitespace from column names (in case of hidden spaces)
df.columns = df.columns.str.strip()

# Clean data
df['parseGBIF_decimalLatitude']  = pd.to_numeric(df['parseGBIF_decimalLatitude'],  errors='coerce')
df['parseGBIF_decimalLongitude'] = pd.to_numeric(df['parseGBIF_decimalLongitude'], errors='coerce')
df = df.dropna(subset=['parseGBIF_decimalLatitude', 'parseGBIF_decimalLongitude'])
df['parseGBIF_wcvp_family'] = df['parseGBIF_wcvp_family'].astype(str).str.strip()

# Get exactly 12 unique families (in order of most records)
families = df['parseGBIF_wcvp_family'].value_counts().head(12).index.tolist()

# ------------------------------------------------------------------
# 3. CREATE ONE MAP PER FAMILY (12 maps)
# ------------------------------------------------------------------
for idx, family in enumerate(families, 1):
    data = df[df['parseGBIF_wcvp_family'] == family]
    n = len(data)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([15, 34, -35, -22], crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.8)

    ax.scatter(data['parseGBIF_decimalLongitude'], data['parseGBIF_decimalLatitude'],
               color='red', marker='o', s=20, alpha=0.7,
               transform=ccrs.PlateCarree(), edgecolors='darkred', linewidth=0.3)

    ax.set_title(f'{family}\n{n:,} Useable occurrence records', fontsize=14, pad=15)

    # Safe filename
    safe_name = "".join(c for c in family if c.isalnum() or c in " _-")[:80]
    png_name = f"Map_{idx:02d}_{safe_name}.png"
    png_path = os.path.join(output_folder, png_name)

    plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    print(f"[{idx}/12] Saved: {png_name}")

# ------------------------------------------------------------------
# 4. DONE
# ------------------------------------------------------------------
print(f"\nAll 12 maps saved in:\n   {output_folder}")
