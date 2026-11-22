import pandas as pd
import matplotlib.pyplot as plt
import os
from common import parse_args

args = parse_args("Top collectors: occurrence records vs. % of total taxa.", "collectors_unique_taxa.csv")

# ------------------------------------------------------------------
# Load the table
# ------------------------------------------------------------------
csv_path = args.input
df = pd.read_csv(csv_path)

# Optional: keep only the top N collectors so the chart stays readable
TOP_N = 40          # change this number as you like
df = df.head(TOP_N).copy()

# ------------------------------------------------------------------
# Create the dual-axis chart
# ------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(14, 7))

# --- Bars: number of unique records ---
color_bars = "#4C72B0"
bars = ax1.bar(
    df["Ctrl_nameRecordedBy_Standard"],
    df["unique_records"],
    color=color_bars,
    alpha=0.75,
    label="Unique occurrence records"
)
ax1.set_ylabel("Number of occurrence records", color=color_bars, fontsize=11)
ax1.tick_params(axis="y", labelcolor=color_bars)
ax1.set_ylim(0, df["unique_records"].max() * 1.15)

# --- Line: % taxa ---
ax2 = ax1.twinx()
color_line = "#E36C2C"
line = ax2.plot(
    df["Ctrl_nameRecordedBy_Standard"],
    df["% taxa"],
    color=color_line,
    marker="o",
    markersize=5,
    linewidth=2,
    label="% of total taxa"
)
ax2.set_ylabel("% of total taxa", color=color_line, fontsize=11)
ax2.tick_params(axis="y", labelcolor=color_line)
ax2.set_ylim(0, df["% taxa"].max() * 1.15)

# ------------------------------------------------------------------
# Formatting
# ------------------------------------------------------------------
ax1.set_xlabel("Collector", fontsize=11)
ax1.set_title(f"Top {TOP_N} collectors – unique occurrence records vs. % of total taxa", fontsize=13, pad=15)

# Rotate collector names for readability
plt.setp(ax1.get_xticklabels(), rotation=60, ha="right", fontsize=8)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

plt.tight_layout()

# ------------------------------------------------------------------
# Save
# ------------------------------------------------------------------
output_dir = args.out_dir

png_path  = os.path.join(output_dir, "collectors_records_vs_pct_taxa.png")
tiff_path = os.path.join(output_dir, "collectors_records_vs_pct_taxa.tiff")

plt.savefig(png_path,  dpi=300, bbox_inches="tight")
plt.savefig(tiff_path, dpi=300, bbox_inches="tight")

print(f"Chart saved to:\n  {png_path}\n  {tiff_path}")
if args.show:
    plt.show()