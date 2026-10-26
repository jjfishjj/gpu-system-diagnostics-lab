#!/usr/bin/env bash
set -euo pipefail
output_dir="${1:-gpu-report}"
mkdir -p "$output_dir"
nvidia-smi -q > "$output_dir/nvidia-smi-q.txt"
nvidia-smi topo -m > "$output_dir/topology.txt"
nvidia-smi --query-gpu=index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw,power.limit,clocks_throttle_reasons.active --format=csv,noheader,nounits > "$output_dir/metrics.csv"
if command -v dcgmi >/dev/null 2>&1; then dcgmi diag -r 2 > "$output_dir/dcgm-diag.txt"; fi
python3 src/gpu_diagnostics.py --input "$output_dir/metrics.csv" > "$output_dir/health.json"
echo "report written to $output_dir"
