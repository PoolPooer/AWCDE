# Reference Environment

## Purpose

This document defines the reference environment used to generate benchmark telemetry throughout the AWCDE research project.

Maintaining a documented reference environment improves reproducibility, simplifies telemetry provider evaluation, and provides provenance for benchmark evidence used during behavioural model validation.

The reference environment is expected to evolve throughout the project and will be updated as new hardware and software platforms are adopted.

---

# Phase 1 Reference Environment

## Host Operating System

Windows 11 Pro

## Linux Environment

Windows Subsystem for Linux (WSL2)

Ubuntu 24.04 LTS

---

## Hardware

### CPU

*TBD*

### GPU

*NVIDIA RTX 5090*

### Memory

*TBD*

### Storage

*TBD*

---

## Software

| Component | Version |
|-----------|---------|
| Python | TBD |
| CUDA | TBD |
| NVIDIA Driver | TBD |
| vLLM | TBD |
| GuideLLM | TBD |
| NVIDIA GenAI-Perf | TBD |

---

## Purpose

This environment is used to:

- Evaluate telemetry providers
- Generate benchmark telemetry
- Validate the behavioural model
- Produce reference Workload Signatures

The environment is intentionally kept stable throughout Phase 1 to minimise external variables during research.

---

# Future Reference Platforms

Future phases may introduce additional reference environments including:

- NVIDIA DGX Spark
- OpenShift AI
- Multi-node GPU environments
- CPU-only inference platforms

Additional platforms will be used to validate the portability of the behavioural model rather than redefine it.