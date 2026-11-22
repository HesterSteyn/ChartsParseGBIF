import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from common import parse_args

args = parse_args("Top 20 families: unique vs. usable occurrence records.", "Table8-families_specimens_total.csv")

# Load the data
total_path = args.input
df_total = pd.read_csv(total_path)

# Use the same file for usable specimens (adjust column names if needed)
df_useable = pd.read_csv(total_path)   # ← same file in your original code

# ====================== SELECT FAMILIES ======================
# Top 20 families excluding 'No family'
top_20 = (df_total[df_total['parseGBIF_wcvp_family'] != 'No family']
          .nlargest(20, 'total_specimens')['parseGBIF_wcvp_family']
          .tolist())

# Add 'No family' as the 21st entry
families_to_plot = top_20 + ['No family']

# Filter both datasets
total_top = df_total[df_total['parseGBIF_wcvp_family'].isin(families_to_plot)].copy()
useable_top = df_useable[df_useable['parseGBIF_wcvp_family'].isin(families_to_plot)].copy()

# Sort: top 20 by total specimens, then 'No family' last
total_top['sort_order'] = total_top['parseGBIF_wcvp_family'].apply(
    lambda x: families_to_plot.index(x)
)
total_top = total_top.sort_values('sort_order')

useable_top = useable_top.set_index('parseGBIF_wcvp_family').loc[families_to_plot].reset_index()

# Merge
df = pd.merge(
    total_top[['parseGBIF_wcvp_family', 'total_specimens']],
    useable_top[['parseGBIF_wcvp_family', 'specimens_useable']],   # change column name if different
    on='parseGBIF_wcvp_family',
    how='left'
).fillna(0)

# ====================== PLOTTING ======================
labels = df['parseGBIF_wcvp_family'].astype(str)
x = np.arange(len(labels))
width = 0.35

max_spec = max(df['total_specimens'].max(), df['specimens_useable'].max())

fig, ax = plt.subplots(figsize=(12, 9))

# Bars
bars1 = ax.bar(x - width/2, df['total_specimens'], width, 
               label='Unique occurrence records', color='#1f77b4', alpha=0.85, edgecolor='none')
bars2 = ax.bar(x + width/2, df['specimens_useable'], width, 
               label='Useable occurrence records', color='#ff7f0e', alpha=0.85)

ax.set_xlabel('Plant families')
ax.set_ylabel('Number of occurrence records')
ax.set_title('Top 20 families — unique vs useable occurrence records')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend(loc='upper right')

# Y-axis padding
padding = max_spec * 0.22
ax.set_ylim(0, max_spec + padding)

# Value labels on bars
offset = max_spec * 0.015
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + offset,
            f'{int(height):,}', ha='center', va='bottom', fontsize=9, rotation=90)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + offset,
            f'{int(height):,}', ha='center', va='bottom', fontsize=9, rotation=90)

plt.tight_layout()

# ====================== SAVE ======================
output_folder = args.out_dir

png_path = output_folder / "Occurrence_records_PerFamily_Top20_NoFamily.png"
plt.savefig(png_path, bbox_inches="tight", dpi=300)
print(f"PNG saved: {png_path}")

tiff_path = output_folder / "Occurrence_records_PerFamily_Top20_NoFamily_600dpi.tiff"
plt.savefig(tiff_path, format="tiff", bbox_inches="tight", dpi=600,
            pil_kwargs={"compression": "tiff_lzw"})
print(f"TIFF saved: {tiff_path}")

if args.show:
    plt.show()