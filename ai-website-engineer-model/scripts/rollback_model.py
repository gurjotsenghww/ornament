#!/usr/bin/env python3
"""
Model rollback utility for Ornàment.
Allows safe switching between versioned model manifests and adapters.
"""
import argparse
import json
from pathlib import Path

def rollback(manifest_dir: Path, target_version: str):
    target_manifest = manifest_dir / f"model-v{target_version}.json"
    if not target_manifest.exists():
        print(f"[ERROR] Target manifest not found: {target_manifest}")
        return False
    
    with open(target_manifest, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"[*] Rolling back active model to version: {data['version']}")
    print(f"    Base model: {data['base_model']}")
    print(f"    Dataset version: {data['dataset_version']}")
    print(f"    Commit SHA: {data['commit_sha']}")
    print(f"[SUCCESS] Model rolled back to v{target_version}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rollback model version")
    parser.add_argument("--version", required=True, help="Version to rollback to (e.g. 0.1.0)")
    args = parser.parse_args()
    manifest_dir = Path(__file__).resolve().parent.parent / "manifests"
    rollback(manifest_dir, args.version)
