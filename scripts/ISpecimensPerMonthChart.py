import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from io import StringIO
from common import parse_args

# ------------------------------------------------------------------
# CONFIG – paths come from the command line (see --help)
# ------------------------------------------------------------------
args     = parse_args("Occurrence records collected per month.", "Table3-specimens_collected_per_month.csv")
CSV_PATH = args.input
PNG_OUT  = args.out_dir / "specimen_records_per_month_chart.png"
TIFF_OUT = args.out_dir / "specimen_records_per_month_chart.tiff"

# ------------------------------------------------------------------
# 1. READ RAW LINES & KEEP ONLY VALID CSV LINES
# ------------------------------------------------------------------
print("\n--- 1. Raw file content (first 15 lines) ---")
valid_lines = []
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if i <= 15:
            print(f"{i:02d}: {line}")
        if line.count(',') >= 2 and line.replace(',', '').strip():
            valid_lines.append(line)

print(f"\nKept {len(valid_lines)} valid CSV lines (including header)")

# ------------------------------------------------------------------
# 2. LOAD CLEANED TEXT INTO pandas
# ------------------------------------------------------------------
csv_text = '\n'.join(valid_lines)
df = pd.read_csv(StringIO(csv_text))
df.columns = df.columns.str.strip()

print("\n--- 2. DataFrame right after reading ---")
print(df)

# ------------------------------------------------------------------
# 3. CONVERT & CLEAN (HANDLE THOUSANDS SEPARATORS)
# ------------------------------------------------------------------
required = {'Ctrl_month', 'specimens_all-duplicates', 'specimens_useable'}
if not required.issubset(df.columns):
    raise ValueError(f"Missing columns. Need: {required}")

# Remove commas (thousands separators) from string columns
for col in required:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '')

# Now convert to numeric
df['Ctrl_month'] = pd.to_numeric(df['Ctrl_month'], errors='coerce')
df['specimens_all-duplicates'] = pd.to_numeric(df['specimens_all-duplicates'], errors='coerce')
df['specimens_useable'] = pd.to_numeric(df['specimens_useable'], errors='coerce')

# Drop rows with ANY NaN in required columns

# ------------------------------------------------------------------
# 4. BAR CHART - Ctrl_month 0/No month as LAST bar + enough space for labels
# ------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7))   # increased height a bit too

df['month_code'] = df['Ctrl_month'].fillna(13).replace(0, 13).astype(int)
df = df.sort_values('month_code').reset_index(drop=True)

months = df['month_code'].to_numpy()
unique = df['specimens_all-duplicates'].to_numpy()
usable = df['specimens_useable'].to_numpy()

bar_width = 0.35
x_pos = np.arange(len(months))

bars_unique = ax.bar(x_pos - bar_width/2, unique, width=bar_width,
                     label='Unique occurrence records', color='#1f77b4', edgecolor='none', linewidth=0.6)

bars_usable = ax.bar(x_pos + bar_width/2, usable, width=bar_width,
                     label='Useable occurrence records', color='orange', edgecolor='none', linewidth=0.6)

month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec', 'No month']

ax.set_xticks(x_pos)
ax.set_xticklabels([month_names[m-1] for m in months])

plt.xticks(rotation=45, ha='right')

ax.set_xlabel('Month')
ax.set_ylabel('Number of occurrence records')
ax.set_title('Occurrence records per month')
ax.legend()
ax.grid(True, axis='y', alpha=0.3)

# ------------------------------------------------------------
# 5. Add value labels
# ------------------------------------------------------------
def add_vertical_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., 
                    height * 1.05, 
                    f'{int(height):,}', 
                    ha='center', va='bottom', 
                    fontsize=9, fontweight='bold', rotation=90)

add_vertical_labels(bars_unique)
add_vertical_labels(bars_usable)

# ------------------------------------------------------------
# 6. Extend Y-axis so labels fit nicely
# ------------------------------------------------------------
max_value = max(unique.max(), usable.max())
ax.set_ylim(0, max_value * 1.22)          # ← This is the key line

# Optional: nicer y-tick formatting
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.tight_layout()

# Save with tight bounding box
fig.savefig(PNG_OUT,  dpi=300, format='png',  facecolor='white', bbox_inches='tight')
fig.savefig(TIFF_OUT, dpi=300, format='tiff', facecolor='white', bbox_inches='tight')
print(f"\nCharts saved to:\n{PNG_OUT}\n{TIFF_OUT}")
if args.show:
    plt.show()
