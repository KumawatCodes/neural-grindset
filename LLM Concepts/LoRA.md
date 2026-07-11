# neural-grindset / LLM Concepts / LoRA.md

## Edit

# LoRA (Low‑Rank Adaptation)

LoRA (Low‑Rank Adaptation) is a parameter‑efficient fine‑tuning (PEFT) technique that freezes the pre‑trained model's weights and injects trainable low‑rank matrices into each layer of the Transformer architecture. It dramatically reduces the number of trainable parameters – from billions to mere millions – while achieving performance comparable to full fine‑tuning.

## Core Intuition (The "Low‑Rank" Assumption)

The key insight behind LoRA is that **the weight updates during fine‑tuning also have a low "intrinsic rank"** – meaning the changes to the weights can be represented using far fewer dimensions than the full weight matrix.

During full fine‑tuning, a pre‑trained weight matrix `W₀` (size `d × k`) is updated to `W₀ + ΔW`. In LoRA, we constrain `ΔW` to be a low‑rank decomposition:

ΔW = A × B


Where:

- `A` is `d × r` (trainable)
- `B` is `r × k` (trainable)
- `r` (rank) is very small: `r << min(d, k)`, typically 4, 8, 16, or 32

The forward pass becomes:

Pre‑trained weight W₀ (d×k) LoRA update ΔW = A·B (d×k)
┌──────────────────────┐ ┌────────┐ ┌────────┐
│ │ │ A (d×r)│ │ B (r×k)│
│ W₀ │ + │ (train)│ │ (train)│
│ (frozen) │ └────────┘ └────────┘
└──────────────────────┘ └──────────┬──────────┘
ΔW

Forward pass: h = x · W₀ + x · (A·B)
↑ ↑
frozen base trainable adapter


## Why LoRA Works (The Math)

For a linear layer with weight `W ∈ ℝ^{d × k}`, the forward pass is:
