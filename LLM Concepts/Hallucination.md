
# Hallucination (in Generative AI)

Hallucination refers to the phenomenon where a generative model produces content that is **factually incorrect, contradictory, or entirely fabricated** – yet presents it with high confidence and fluency. Unlike a simple mistake, hallucinations are often *plausible-sounding* nonsense, making them particularly dangerous in high‑stakes applications (medicine, law, finance).

## Why Hallucinations Are Dangerous

- **Trust erosion** – Users lose confidence when models confidently state falsehoods.
- **Misinformation spread** – Generated content can be mistaken for ground truth.
- **Legal & compliance risks** – Incorrect legal citations or medical advice can have real consequences.
- **Hidden cost of verification** – Humans must fact‑check every output, negating productivity gains.

## Types of Hallucinations

| Type                  | Description                                                          | Example                                                               |
|-----------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|
| **Factual**           | Contradicts established world knowledge.                             | *"The capital of Australia is Sydney."* (actually Canberra)           |
| **Faithfulness**      | Contradicts the user's provided context (RAG, summarisation).        | *Given a document about cats, the model says "Dogs are mentioned."*   |
| **Logical**           | Reasoning error leading to an absurd or contradictory conclusion.    | *"If A > B and B > C, then C > A."*                                  |
| **Extrinsic**         | Introduces new information not in the prompt or source, unverifiable. | *Inventing a study that doesn't exist to support a claim.*            |
| **Intrinsic**         | Contradicts the provided source or prompt (direct violation).        | *Prompt: "The sky is blue." → Output: "The sky is green."*            |

## Why Hallucinations Happen

### 1. Training Data Issues
- **Incomplete coverage** – Model lacks knowledge about niche topics.
- **Contradictions** – Conflicting facts in training data (e.g., outdated information).
- **Sycophancy** – Model learns to agree with false user premises.

### 2. Training Objective (Teacher Forcing)
Autoregressive models are trained to minimise cross‑entropy loss on **next‑token prediction**. This encourages:
- **Short‑term coherence** over long‑term factual accuracy.
- **Maximum likelihood** – The model learns the *most probable* continuation, not necessarily the *correct* one.

### 3. Exposure Bias (Train‑Inference Mismatch)
During training, the model sees the true previous tokens (teacher forcing). During inference, it sees its **own predictions** – errors accumulate and amplify.

```text
Training:  [The] [capital] [of] [France] → [is] [Paris] (true)
Inference: [The] [capital] [of] [France] → [is] [London?] (drifts)

```

4. Softmax Temperature
Higher temperature → more random sampling → higher chance of hallucination. Lower temperature → more deterministic but still can hallucinate if the top‑1 is wrong.

5. "Lost in the Middle"
In long contexts, the model forgets information in the middle of the context window, leading to hallucinated answers that ignore critical facts.

How Hallucination Propagates (ASCII Diagram)

```
User Prompt
    │
    ▼
┌─────────────────────────────────────┐
│  Model receives query               │
│  "What is the tallest mountain?"    │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Retrieves/attends to relevant      │
│  patterns (but misses Mount Everest │
│  due to weak signal / bad attention)│
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Softmax over vocabulary:           │
│  "K2" = 0.48, "Everest" = 0.45,     │
│  "Denali" = 0.07                    │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Sampling (e.g., temperature=1.0)   │
│  picks "K2" (wrong!)                │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Fluently generates:                │
│  "The tallest mountain is K2."      │
│  (Confident, articulate, wrong!)    │
└─────────────────────────────────────┘
```
Code Example: Detecting Hallucinations with SelfCheckGPT
SelfCheckGPT uses stochastic consistency – if the model gives different answers when sampled multiple times, the original is likely a hallucination.

```
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def generate_samples(prompt, n=5):
    samples = []
    for _ in range(n):
        inputs = tokenizer(prompt, return_tensors='pt')
        outputs = model.generate(**inputs, max_new_tokens=50, do_sample=True, temperature=0.8)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        samples.append(text)
    return samples

# Example
prompt = "The tallest mountain in the world is"
samples = generate_samples(prompt, n=5)

for i, s in enumerate(samples):
    print(f"Sample {i+1}: {s}")

# Check consistency: if answers vary wildly, hallucination risk is high.
```
