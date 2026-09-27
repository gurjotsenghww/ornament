"""
Command-Line Interface for the Ornàment Training Data System (Sections 1, 23, 26).
Provides collect, validate, build, status, and stats commands.
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from ornament.training_data.pipeline import TrainingDataPipeline
from ornament.training_data.config import TrainingDataConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        prog="ornament-data",
        description="Ornàment Autonomous Web Training Data Engine"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # collect
    collect_parser = subparsers.add_parser("collect", help="Collect/generate training examples")
    collect_parser.add_argument("--type", choices=["html", "css", "debugging", "paired"], required=True, help="Data type to collect")
    collect_parser.add_argument("--count", type=int, default=100, help="Number of examples to collect")
    collect_parser.add_argument("--categories", type=str, help="Comma-separated category filters")

    # build
    build_parser = subparsers.add_parser("build", help="Build JSONL dataset splits and manifests")
    build_parser.add_argument("--output", default="dataset-v0.1", help="Dataset version identifier")

    # status
    subparsers.add_parser("status", help="Display pipeline status, validated counts, and storage metrics")

    # stats
    subparsers.add_parser("stats", help="Display detailed category distribution and quality statistics")

    args = parser.parse_args()
    pipeline = TrainingDataPipeline()

    if args.command == "collect":
        cats = [c.strip() for c in args.categories.split(",")] if args.categories else None
        res = pipeline.collect(data_type=args.type, count=args.count, categories=cats)
        print("\n" + "=" * 50)
        print(f"[*] Collection Complete for '{args.type}'")
        print(f"    Requested:        {res['requested']}")
        print(f"    Saved (New):      {res['saved']}")
        print(f"    Duplicates (Skip):{res['duplicates']}")
        print(f"    Rejected:         {res['rejected']}")
        print(f"    Total Validated:  {res['total_validated']}")
        print("=" * 50 + "\n")

    elif args.command == "build":
        res = pipeline.build_datasets(version=args.output)
        print("\n" + "=" * 50)
        print(f"[*] Dataset Compilation Complete: {res['version']}")
        print(f"    HTML splits:      {res['datasets']['datasets_created'].get('html')}")
        print(f"    CSS splits:       {res['datasets']['datasets_created'].get('css')}")
        print(f"    Debugging splits: {res['datasets']['datasets_created'].get('debugging')}")
        print(f"    Portfolio count:  {res['datasets']['datasets_created'].get('portfolio')}")
        print("=" * 50 + "\n")

    elif args.command == "status":
        stats = pipeline.get_status()
        counts = stats["counts"]
        print("\n" + "=" * 50)
        print("Ornàment Training Data Store Status")
        print("=" * 50)
        print(f"  HTML Examples:      {counts.get('html', 0):,}")
        print(f"  CSS Examples:       {counts.get('css', 0):,}")
        print(f"  Debugging Cases:    {counts.get('debugging', 0):,}")
        print(f"  Paired Examples:    {counts.get('paired', 0):,}")
        print("-" * 50)
        print(f"  Total Validated:    {counts.get('validated', 0):,}")
        print(f"  Rejected Samples:   {counts.get('rejected', 0):,}")
        print(f"  Duplicate Skips:    {counts.get('duplicates', 0):,}")
        print(f"  Unique Hash Index:  {stats.get('dedup_registered_hashes', 0):,}")
        print("=" * 50 + "\n")

    elif args.command == "stats":
        stats = pipeline.get_status()
        print("\n" + "=" * 50)
        print("Detailed Category Distribution")
        print("=" * 50)
        for lang, cats in stats.get("category_counts", {}).items():
            print(f"\n[{lang.upper()}] Total: {sum(cats.values())}")
            for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
                print(f"  - {cat:20s}: {count:5d}")
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
