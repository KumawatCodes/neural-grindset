
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
