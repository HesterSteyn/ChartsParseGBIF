import pandas as pd
import matplotlib.pyplot as plt  # Ensure this import is included
import os  

from common import parse_args

args = parse_args("Taxa collected per year.", "Table2-species_collected_per_year.csv")
file_path = args.input

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Strip any leading/trailing whitespace from column names (common CSV issue causing KeyError)
df.columns = df.columns.str.strip()

# Now sort by Ctrl_year (should work after stripping)
df = df.sort_values('Ctrl_year')

# Create the line chart
plt.figure(figsize=(12, 6))  # Adjust size as needed
plt.plot(df['Ctrl_year'], df['species_all'], marker='o', label='Unique taxa', linewidth=2)
plt.plot(df['Ctrl_year'], df['species_useable'], marker='s', label='Useable taxa', linewidth=2)

# Set exact years as x-axis ticks (display all years)
# plt.xticks(df['Ctrl_year'], rotation=45)  # Rotate labels for readability if many years

# Label x-axis every 25 years
years = df['Ctrl_year'].dropna().unique()
if len(years) > 0:
    start_year = int(years.min() // 25 * 25)
    end_year = int(years.max() // 25 * 25) + 25
    x_ticks = list(range(start_year, end_year + 1, 25))
    plt.xticks(x_ticks, rotation=45)
else:
    plt.xticks(rotation=45)

# Customize the chart
plt.xlabel('Year')
plt.ylabel('Number of taxa')
plt.title('Taxa per year')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()  # Adjust layout to prevent label cutoff

# save the charts
charts_dir = args.out_dir

# Define filenames
base_name = 'species_records_per_year_chart'
tiff_path = os.path.join(charts_dir, f'{base_name}.tiff')
png_path = os.path.join(charts_dir, f'{base_name}.png')

# Save as TIFF (your original format)
plt.savefig(tiff_path, format='tiff', dpi=300, bbox_inches='tight')
print(f"Chart saved as TIFF: {tiff_path}")

# Save as PNG
plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
print(f"Chart saved as PNG: {png_path}")

# Display the chart
if args.show:
    plt.show()
