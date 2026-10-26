ARG CUDA_IMAGE=nvidia/cuda:13.4.3-base-ubuntu24.04
FROM ${CUDA_IMAGE}
RUN apt-get update && apt-get install -y --no-install-recommends python3 && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY src/ src/
ENTRYPOINT ["python3", "src/gpu_diagnostics.py"]
