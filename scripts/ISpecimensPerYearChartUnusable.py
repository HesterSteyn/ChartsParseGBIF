import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# -------------------------------------------------
from common import parse_args

args = parse_args("Percentage of unusable occurrence records per year.", "Table1-specimens_collectedPerYear_percentageUnuseable.csv")
file_path = args.input

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()
df = df.sort_values('Ctrl_year')

# Clean data
df = df.dropna(subset=['Ctrl_year', 'percentageUnuseable'])

print("=== DEBUG INFO ===")
print(f"Rows after cleaning: {len(df)}")
print(df.head())
print(df[['Ctrl_year', 'percentageUnuseable']].describe())
print("==================")

if len(df) == 0:
    print("ERROR: No data left after cleaning. Check your CSV.")
else:
    # Create the plot
    plt.figure(figsize=(12, 6))

    # Actual data
    plt.plot(df['Ctrl_year'], df['percentageUnuseable'],
             marker='o', linewidth=2, label='Unuseable records (%)')

    # Trendline
    z = np.polyfit(df['Ctrl_year'], df['percentageUnuseable'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df['Ctrl_year'].min(), df['Ctrl_year'].max(), 100)
    plt.plot(x_trend, p(x_trend),
             color='red', linestyle='--', linewidth=2,
             label=f'Trendline (slope = {z[0]:.4f})')

    # X-axis ticks every 25 years
    years = df['Ctrl_year'].unique()
    start_year = int(years.min() // 25 * 25)
    end_year = int(years.max() // 25 * 25) + 25
    plt.xticks(list(range(start_year, end_year + 1, 25)), rotation=45)

    # ... (all your previous code remains the same)

# Formatting
plt.xlabel('Year')
plt.ylabel('Unuseable occurrence records (%)')
plt.title('Percentage unuseable occurrence records per year')

plt.ylim(0, 105)                          # ← gives ~5% breathing room above 100
plt.yticks([0, 20, 40, 60, 80, 100])       # ← only labels up to 100 (no label above)

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ---------- SAVE ----------
charts_dir = args.out_dir

base_name = 'unuseable_records_per_year_chart'
tiff_path = os.path.join(charts_dir, f'{base_name}.tiff')
png_path  = os.path.join(charts_dir, f'{base_name}.png')

plt.savefig(tiff_path, format='tiff', dpi=300, bbox_inches='tight')
plt.savefig(png_path,  format='png',  dpi=300, bbox_inches='tight')

print(f"\nChart saved as:")
print(f"  TIFF → {tiff_path}")
print(f"  PNG  → {png_path}")

# Show the graph (force it)
if args.show:
    plt.show()
