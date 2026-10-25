"""Locate and load the prepared dataset written by notebook 01.

Notebook 01 writes one folder per run, `DATA_ROOT/<run_id>/`, and creates `manifest.json` in it as its
last step. A run without a manifest is incomplete. Later notebooks read the data only through `load_run`.
"""
import json
import os
from pathlib import Path

DATA_ROOT = Path(os.environ.get("HW2_DATA_ROOT", Path.home() / ".cache" / "hw2_prepared"))


def load_run(run_id=None, data_root=DATA_ROOT):
    """Return the manifest of a prepared run (default: the latest one) with `root` and absolute `paths` added."""
    data_root = Path(data_root)
    if run_id is None:
        latest = data_root / "latest.txt"
        if not latest.exists():
            raise FileNotFoundError(f"No prepared data in {data_root}. Run notebook 01 first (or set HW2_DATA_ROOT).")
        run_id = latest.read_text().strip()

    root = data_root / run_id
    manifest_path = root / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"{root} has no manifest.json: notebook 01 did not finish for this run.")

    manifest = json.loads(manifest_path.read_text())
    manifest["root"] = root
    manifest["paths"] = {name: root / rel for name, rel in manifest["files"].items()}
    return manifest
