#!/usr/bin/env python3
"""
Plot herbarium locations and save as PNG + 600 DPI TIFF.
"""

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from common import parse_args

args = parse_args(__doc__, "Table5-HerbariumOR.csv")

# ------------------------------------------------------------
# 1. Load CSV
# ------------------------------------------------------------
csv_path = args.input
df = pd.read_csv(csv_path)

# Filter valid coordinates
df = df.dropna(subset=["location.lat", "location.lon"])
df = df[(df["location.lat"] != 0) | (df["location.lon"] != 0)]

print(f"Plotting {len(df)} herbaria with valid coordinates.")

# ------------------------------------------------------------
# 2. Create map
# ------------------------------------------------------------
fig = plt.figure(figsize=(16, 9), dpi=150)  # High-quality preview
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_global()

# Background
ax.add_feature(cfeature.LAND, facecolor="#f0f0f0")
ax.add_feature(cfeature.OCEAN, facecolor="#d0e8ff")
ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor="gray")
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, edgecolor="gray")

# Plot points
ax.scatter(
    df["location.lon"], df["location.lat"],
    color="#ff7f0e", s=15, edgecolor="#ff7f0e", linewidth=0.5,
    transform=ccrs.PlateCarree(), zorder=5
)

# Title & grid
ax.set_title(f"Herbaria housing SA specimens", fontsize=12, pad=20)
ax.gridlines(draw_labels=True, linewidth=0.5, color="gray", alpha=0.5, linestyle="--")

# ------------------------------------------------------------
# 3. Save as PNG (standard)
# ------------------------------------------------------------

png_path = args.out_dir / "herbaria_world_map.png"
fig.savefig(png_path, bbox_inches="tight", dpi=300)  # 300 DPI is excellent for PNG
print(f"PNG saved: {png_path.resolve()}")

# ------------------------------------------------------------
# 4. Save as 600 DPI TIFF
# ------------------------------------------------------------
tiff_path = args.out_dir / "herbaria_world_map_600dpi.tiff"
fig.savefig(
    tiff_path,
    format="tiff",
    bbox_inches="tight",
    dpi=600,                    # 600 DPI
    pil_kwargs={"compression": "tiff_lzw"}  # Lossless compression
)
print(f"600 DPI TIFF saved: {tiff_path.resolve()}")

# ------------------------------------------------------------
# 5. Show plot (optional)
# ------------------------------------------------------------
if args.show:
    plt.show()