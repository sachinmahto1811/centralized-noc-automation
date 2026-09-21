import argparse
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    open_df = df[df["status"].eq("OPEN")].copy()

    summary = (
        open_df.groupby(["circle", "alarm_type"], as_index=False)
        .agg(site_count=("site_id", "nunique"),
             alarm_count=("site_id", "size"))
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
