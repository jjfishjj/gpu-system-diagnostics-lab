"""Collect and evaluate NVIDIA GPU health data from nvidia-smi CSV output."""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

FIELDS = ["index", "name", "temperature.gpu", "utilization.gpu", "memory.used", "memory.total", "power.draw", "power.limit", "clocks_throttle_reasons.active"]


@dataclass(frozen=True)
class GPUHealth:
    index: int
    name: str
    temperature_c: float
    utilization_pct: float
    memory_pct: float
    power_pct: float
    throttle_active: bool
    status: str


def parse_nvidia_smi(text: str) -> list[GPUHealth]:
    results = []
    for row in csv.reader(io.StringIO(text.strip())):
        if not row:
            continue
        values = [cell.strip() for cell in row]
        if len(values) != len(FIELDS):
            raise ValueError(f"expected {len(FIELDS)} columns, got {len(values)}")
        index, name, temp, util, used, total, power, limit, throttle = values
        memory_pct = float(used) / float(total) * 100 if float(total) else 0
        power_pct = float(power) / float(limit) * 100 if float(limit) else 0
        throttled = throttle not in {"0x0000000000000000", "0", "Not Active", "N/A"}
        status = "critical" if float(temp) >= 90 or throttled else "warning" if float(temp) >= 80 or memory_pct >= 95 else "healthy"
        results.append(GPUHealth(int(index), name, float(temp), float(util), memory_pct, power_pct, throttled, status))
    return results


def collect() -> str:
    command = ["nvidia-smi", f"--query-gpu={','.join(FIELDS)}", "--format=csv,noheader,nounits"]
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="parse a saved nvidia-smi CSV instead of querying hardware")
    args = parser.parse_args()
    raw = args.input.read_text(encoding="utf-8") if args.input else collect()
    print(json.dumps([asdict(item) for item in parse_nvidia_smi(raw)], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
