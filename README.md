# GPU System Diagnostics Lab

把 `nvidia-smi`、DCGM 與 GPU topology 收斂成可保存的節點健康報告；同時保留瀏覽器版互動診斷器。

## 快速驗證

```bash
python -m unittest discover -s tests -v
python src/gpu_diagnostics.py --input tests/fixtures/nvidia_smi.csv
```

## NVIDIA 實機

Linux 主機需有 NVIDIA Driver；安裝 DCGM 時會額外執行 Level 2 diagnostics：

```bash
bash scripts/collect_system_report.sh gpu-report
```

報告含完整 `nvidia-smi -q`、拓撲、原始 metrics、健康判讀與選用的 DCGM 結果。自架 GPU Runner 可手動執行 `gpu.yml`，一般 CI 以固定 fixture 防止 parser 與告警規則退化。

## 判讀範圍

目前檢查溫度、利用率、顯存、功耗與 throttle reason；正式監控可再接 NVML/DCGM exporter 與 Prometheus 歷史基線。

