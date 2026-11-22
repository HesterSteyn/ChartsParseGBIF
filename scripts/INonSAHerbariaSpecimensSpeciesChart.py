import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from common import parse_args

# --------------------------- CONFIG ---------------------------
args     = parse_args("Records and taxa for non-SA herbaria with > 6000 records.", "Table5_Herbarium_JoinedNonSA.csv")
CSV_PATH = args.input
PNG_OUT  = args.out_dir / "non_SA_herbarium_records_occurrence_records.png"
TIFF_OUT = args.out_dir / "non_SA_herbarium_records_occurrence_records.tiff"

# --------------------------- LOAD & CLEAN DATA ---------------------------
df = pd.read_csv(CSV_PATH)

for col in ['records', 'species']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Filter: herbaria with > 6000 records
df_filtered = df[df['records'] > 6000].copy().reset_index(drop=True)

print(f"Found {len(df_filtered)} herbaria with > 6000 records")
print(df_filtered[['Herbarium_Code', 'records', 'species']])

# Sort by records (descending)
df_filtered = df_filtered.sort_values('records', ascending=False).reset_index(drop=True)

# --------------------------- BAR CHART ---------------------------
fig, ax = plt.subplots(figsize=(15, 9))   # Slightly larger for log scale

x_pos = np.arange(len(df_filtered))
bar_width = 0.35

bars_records = ax.bar(x_pos - bar_width/2, df_filtered['records'], 
                      width=bar_width, label='All occurrence records', color='#1f77b4', edgecolor='none', linewidth=0.6)

bars_species = ax.bar(x_pos + bar_width/2, df_filtered['species'], 
                      width=bar_width, label='All taxa', color='#ff7f0e', edgecolor='none', linewidth=0.6)

# Labels
ax.set_xlabel('Institution Code', fontsize=12)
ax.set_ylabel('Count (Log Scale)', fontsize=12)
ax.set_title('Non-SA herbaria with more than 6 000 occurrence records', fontsize=14, pad=20)

ax.set_xticks(x_pos)
ax.set_xticklabels(df_filtered['Herbarium_Code'], 
                   rotation=45, ha='right', fontsize=10)

ax.legend()
ax.grid(True, axis='y', alpha=0.3)

# --------------------------- LOG SCALE ---------------------------
ax.set_yscale('log')

# Set reasonable log limits
max_val = max(df_filtered['records'].max(), df_filtered['species'].max())
ax.set_ylim(bottom=100, top=max_val * 2.5)   # Start from 100 to avoid log(0) issues

# --------------------------- VALUE LABELS (Log-friendly) ---------------------------
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            # Place label slightly above the bar on log scale
            ax.text(bar.get_x() + bar.get_width()/2., 
                    height * 1.08, 
                    f'{int(height):,}', 
                    ha='center', va='bottom',
                    fontsize=8.5, fontweight='bold', rotation=90)

add_labels(bars_records)
add_labels(bars_species)

plt.tight_layout()

# --------------------------- SAVE ---------------------------
fig.savefig(PNG_OUT, dpi=300, bbox_inches='tight', facecolor='white')
fig.savefig(TIFF_OUT, dpi=300, bbox_inches='tight', facecolor='white')

print(f"\nCharts saved to:\n{PNG_OUT}\n{TIFF_OUT}")
if args.show:
    plt.show()
