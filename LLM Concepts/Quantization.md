
# Quantization

Quantization is the process of reducing the numerical precision of a model's weights and activations – typically from 32‑bit floating point (FP32) to lower‑bit formats like 16‑bit, 8‑bit, or even 4‑bit integers. It dramatically reduces memory usage, speeds up inference, and enables large language models to run on consumer hardware with minimal loss in quality.

## Why Quantization Matters

- **Memory reduction** – A 7B parameter model at FP32 = 28GB; at INT4 = 3.5GB (8× smaller).
- **Faster inference** – Lower precision operations are computationally cheaper (especially on GPUs with INT8/INT4 tensor cores).
- **Deployment** – Enables running models on edge devices, mobile phones, and consumer GPUs (e.g., RTX 3090/4090 with 24GB VRAM).
- **Cost savings** – Less VRAM = smaller cloud instances, lower hosting costs.

## Precision Formats (Common)

| Format   | Bits | Type         | Range / Precision                    | Typical Use Case                     |
|----------|------|--------------|--------------------------------------|--------------------------------------|
| **FP32** | 32   | Floating     | ~1e‑38 to 3e38, high precision       | Original training (full precision)   |
| **FP16** | 16   | Floating     | ~5.9e‑8 to 65504                     | Faster training, OK quality          |
| **BF16** | 16   | Floating     | Same range as FP32, less precision   | Stable training (popular)            |
| **INT8** | 8    | Integer      | -128 to 127 (signed)                 | Inference (smooth, low loss)         |
| **INT4** | 4    | Integer      | -8 to 7 or 0 to 15                   | Extreme compression (small loss)     |
| **NF4**  | 4    | Float (non‑uniform) | 4‑bit normal‑float (bitsandbytes) | QLoRA fine‑tuning, better than INT4 |

## Types of Quantization

### 1. Post‑Training Quantization (PTQ)

**Process:** Quantize a pre‑trained model **without** retraining. Uses a small calibration dataset to determine optimal scale factors.

Pre‑trained FP16 model → Calibrate on sample data → Quantize weights → INT8/INT4 model

text

| Pros ✅                                     | Cons ❌                                         |
|--------------------------------------------|------------------------------------------------|
| Fast (hours, not days)                     | Quality loss is more noticeable at low bits    |
| No training infrastructure needed          | Struggles with outliers (activation spikes)    |
| Works for most open‑source models          | May need GPTQ/AWQ for 4‑bit quality            |

### 2. Quantization‑Aware Training (QAT)

**Process:** Simulate quantization during training (or fine‑tuning). The model learns to adapt to low‑precision constraints.
Train / Fine‑tune with simulated quantization (fake quantization) → Final quantized model

text

| Pros ✅                                     | Cons ❌                                         |
|--------------------------------------------|------------------------------------------------|
| Higher quality at low bits (4‑bit)         | Requires training infrastructure               |
| Model learns to be robust to rounding      | Slower (takes days)                            |
| Best for production models                 | Often overkill for most use cases              |

### Quantization Pipeline (ASCII)
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Full‑precision │ ──→ │ Calibration │ ──→ │ Quantized │
│ Model (FP32) │ │ (scale/zero) │ │ Model (INT4) │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│ │ │
│ │ │
▼ ▼ ▼
Memory: 28GB Computes min/max Memory: 3.5GB
(7B params) per channel / tensor (~8× smaller)

text

## Popular Quantization Methods

| Method        | Bit Width | How It Works                                | Best For                     |
|---------------|-----------|---------------------------------------------|------------------------------|
| **GPTQ**      | 4, 3, 2   | Layer‑wise quantization with optimal rounding | NVIDIA GPUs, high quality 4‑bit |
| **AWQ**       | 4         | Protects 1% of salient weights (per‑channel scaling) | Faster than GPTQ, similar quality |
| **GGUF**      | 2–8       | CPU‑first format with block quantisation    | llama.cpp, CPU/Apple Silicon |
| **bitsandbytes (NF4)** | 4 | Non‑uniform 4‑bit (normal‑float)            | QLoRA fine‑tuning (HF ecosystem) |
| **SqueezeLLM**| 4         | Dense vs. sparse separation (outliers kept high‑precision) | Very low bits (3‑bit) |

### GPTQ vs. AWQ vs. GGUF – Quick Reference

| Feature        | GPTQ                         | AWQ                         | GGUF                       |
|----------------|------------------------------|-----------------------------|----------------------------|
| **Target hardware** | NVIDIA GPU (CUDA)          | NVIDIA GPU                  | CPU / Apple Silicon / GPU  |
| **Quality**        | Excellent at 4‑bit          | Slightly better than GPTQ 4‑bit | Good, but typically slightly lower than GPTQ/AWQ |
| **Speed**          | Fast on GPUs                | Very fast on GPUs           | Optimised for CPU/ARM      |
| **File format**    | `.safetensors` (HF)         | `.safetensors`              | `.gguf`                    |
| **Common tool**    | `auto_gptq` / `ExLlama`     | `llm-awq`                   | `llama.cpp` / `ollama`     |

## How Quantization Works (The Math)

For **symmetric quantization** (no zero‑point):
q = round(x / scale)
x_quant = q * scale

where scale = max(|x|) / (2^(bits-1) - 1)
