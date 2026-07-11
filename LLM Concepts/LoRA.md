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

 h = W · x

text

Full fine‑tuning updates `W` to `W'`:
h = (W + ΔW) · x

text

LoRA approximates `ΔW` as `A · B` where:

- `A ∈ ℝ^{d × r}`, initialised with random Gaussian (Kaiming/He initialisation)
- `B ∈ ℝ^{r × k}`, initialised with zeros

**Initialisation trick:** At the start of training, `B = 0`, so `ΔW = 0`. The model starts from exactly the base model (no initial quality loss), and `A` and `B` are trained to learn the necessary updates.

The gradient flows through `A` and `B` only – the original weights `W₀` receive no gradients.

## Key Hyperparameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| **`r` (rank)** | The rank of the low‑rank matrices. Higher `r` = more capacity, more trainable params. | 4, 8, 16, 32, 64 |
| **`alpha`** | Scaling factor: `ΔW = (alpha / r) · (A · B)`. Controls the strength of LoRA relative to the base model. | 8, 16, 32 |
| **`lora_dropout`** | Dropout probability applied to the LoRA outputs. Regularisation to prevent overfitting. | 0.0 – 0.1 |
| **`target_modules`** | Which weight matrices to apply LoRA to (e.g., `q_proj`, `v_proj`, `k_proj`, `o_proj`). | All attention layers, sometimes MLP layers |
| **`bias`** | Whether to train bias terms. Usually `"none"` to save memory. | `"none"`, `"all"`, `"lora_only"` |
| **`task_type`** | Task type for PEFT (e.g., `"CAUSAL_LM"`, `"SEQ_CLS"`). | `"CAUSAL_LM"` |

## Memory Savings (7B Model Example)

| Fine‑tuning Method | Trainable Params | Memory (FP16) | GPU Required |
|-------------------|------------------|---------------|---------------|
| Full Fine‑tuning | 7,000,000,000 (100%) | 14 GB (weights) + 14 GB (gradients) + 14 GB (optimiser) ≈ **42 GB** | A100‑80GB |
| LoRA (`r=16`) | ~4,000,000 (0.06%) | 14 GB (weights, frozen) + 8 MB (LoRA) + 16 MB (gradients) ≈ **14 GB** | RTX 3090 / 4090 |
| QLoRA (`r=16` + 4‑bit) | ~4,000,000 (0.06%) | 3.5 GB (4‑bit weights) + 8 MB (LoRA) ≈ **3.5 GB** | RTX 3060 (6GB) |

> **Key Insight:** LoRA enables fine‑tuning a 7B model on a single consumer GPU (24GB) without any model sharding or offloading.

## Code Example: Training with LoRA + PEFT

```python
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
import torch

# 1. Load base model (FP16 or BF16)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
tokenizer.pad_token = tokenizer.eos_token

# 2. Configure LoRA
lora_config = LoraConfig(
    r=16,                                    # Rank
    lora_alpha=32,                           # Scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Attention layers
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 3. Wrap model with LoRA
model = get_peft_model(model, lora_config)

# 4. Print trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 6,738,415,616 || trainable%: 0.0622

# 5. Prepare dataset
dataset = load_dataset("json", data_files="my_data.json")
def tokenize_func(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=512
    )
tokenized_dataset = dataset.map(tokenize_func, batched=True)

# 6. Training arguments
training_args = TrainingArguments(
    output_dir="./lora-llama2",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,              # Higher lr than full fine‑tuning
    fp16=True,
    logging_steps=10,
    save_steps=100,
    optim="adamw_torch"
)

# 7. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"]
)

trainer.train()

# 8. Save adapter weights (small file)
model.save_pretrained("./lora-llama2-adapter")

# 9. Optional: merge and save full model
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./llama2-finetuned-full")
```
# Code Example: Inference with LoRA Adapter
```
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "./lora-llama2-adapter")
model.eval()

# Generate
prompt = "Explain LoRA in simple terms."
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```
# QLoRA (4‑bit + LoRA) – The Most Popular Hybrid

