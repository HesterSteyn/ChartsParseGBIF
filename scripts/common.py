"""
Shared command-line handling for the chart scripts.

By default every script reads its input CSV from ``<repo>/data`` and writes
figures to ``<repo>/figures``. Both can be overridden on the command line:

    python scripts/ISpeciesPerYearChart.py --data-dir /path/to/csvs
    python scripts/ISpeciesPerYearChart.py --input my_table.csv --out-dir out
    python scripts/ISpeciesPerYearChart.py --no-show     # don't open a window
"""

import argparse
from pathlib import Path

import matplotlib

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = REPO_ROOT / "data"
DEFAULT_OUT_DIR = REPO_ROOT / "figures"


def parse_args(description, default_input):
    """Parse the common CLI options and return them.

    Returns an ``argparse.Namespace`` with:
      * ``input``   - Path to the input CSV
      * ``out_dir`` - Path to the output folder (created if missing)
      * ``show``    - whether to display the figure interactively
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--data-dir", type=Path, default=DEFAULT_DATA_DIR,
        help=f"folder containing the input CSV (default: {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--input", type=Path, default=None,
        help=f"input CSV file; overrides --data-dir (default: <data-dir>/{default_input})",
    )
    parser.add_argument(
        "--out-dir", type=Path, default=DEFAULT_OUT_DIR,
        help=f"folder to write figures to (default: {DEFAULT_OUT_DIR})",
    )
    parser.add_argument(
        "--no-show", dest="show", action="store_false",
        help="save figures without opening an interactive window",
    )
    args = parser.parse_args()

    args.input = args.input if args.input is not None else args.data_dir / default_input
    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    if not args.show:
        matplotlib.use("Agg")  # no display needed (e.g. on a server)

    return args
