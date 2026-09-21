from __future__ import annotations
import argparse
import subprocess
import sys
import time
from pathlib import Path
import yaml

def run_workflow(item: dict):
    if not item.get("enabled", True):
        return item["name"], "SKIPPED", 0.0

    cmd = [
        sys.executable,
        item["script"],
        "--input", item["input"],
        "--output", item["output"]
    ]

    start = time.perf_counter()
    proc = subprocess.run(cmd, check=False)
    elapsed = time.perf_counter() - start
    return item["name"], "OK" if proc.returncode == 0 else "FAILED", elapsed

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    for workflow in config.get("workflows", []):
        name, status, elapsed = run_workflow(workflow)
        print(f"{name}: {status} | {elapsed:.2f}s")

if __name__ == "__main__":
    main()
