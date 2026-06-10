# Autoregressive Models

Autoregressive (AR) models generate sequences **one element at a time**, conditioning each new element on the previously generated ones. They are the foundation of modern large language models (LLMs) like GPT‑4, Llama, and Gemini.

## Core Idea

Given a sequence `x₁, x₂, ..., xₜ`, an autoregressive model learns the conditional probability distribution:
P(x₁, x₂, ..., xₜ) = Πᵢ P(xᵢ | x₁, ..., xᵢ₋₁)


During generation (inference), the model predicts the **next token** given all previous tokens, then appends that token and repeats.

## How It Works (Step by Step)

1. **Input** – A prompt or start token: `["The", "cat", "sat"]`
2. **Predict next** – Model outputs probability over vocabulary for token 4.
3. **Sample** – Choose a token (e.g., `"on"`) using argmax, top‑k, or temperature sampling.
4. **Append** – New sequence: `["The", "cat", "sat", "on"]`
5. **Repeat** – Predict token 5, and so on, until an end token or max length.

### ASCII Diagram of Autoregressive Generation

```text
Step 1:   [The]  →  model  →  P(cat | The)     →  choose "cat"
Step 2:   [The, cat] → model → P(sat | The, cat) → choose "sat"
Step 3:   [The, cat, sat] → model → P(on | The, cat, sat) → choose "on"
Step 4:   ... continues
```

Training: Teacher Forcing
During training, the model sees the full ground truth sequence and learns to predict each next token given the true previous tokens (not its own predictions). This is called teacher forcing.

```
Input:    [The,  cat,  sat,  on,  the]
Target:   [cat,  sat,  on,   the, mat]

Loss = cross_entropy(predicted, target) averaged over all positions
```
Causal (Masked) Attention
In transformer‑based AR models, attention is causal – each token can only attend to previous (and itself) tokens, not future ones.

```
Tokens:   t1    t2    t3    t4
t1:       ✔     ✘     ✘     ✘
t2:       ✔     ✔     ✘     ✘
t3:       ✔     ✔     ✔     ✘
t4:       ✔     ✔     ✔     ✔
```
This is implemented via a mask that sets future positions to -inf before softmax.

Simple Code Example (PyTorch, causal mask)
```python
import torch
import torch.nn.functional as F

def causal_mask(size):
    mask = torch.triu(torch.ones(1, size, size), diagonal=1).bool()
    return mask  # True = positions to mask

# Example sequence of 4 tokens
seq_len = 4
mask = causal_mask(seq_len)
print(mask.squeeze())
# Output:
# [[False,  True,  True,  True],
#  [False, False,  True,  True],
#  [False, False, False,  True],
#  [False, False, False, False]]
```
Generating Text (Inference)
```python
def generate(model, prompt_tokens, max_new_tokens=20, temperature=1.0):
    for _ in range(max_new_tokens):
        logits = model(prompt_tokens)          # shape: (seq_len, vocab_size)
        next_token_logits = logits[-1, :]      # last position
        if temperature > 0:
            probs = F.softmax(next_token_logits / temperature, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
        else:
            next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
        prompt_tokens = torch.cat([prompt_tokens, next_token], dim=-1)
    return prompt_tokens
```
Popular Autoregressive Models
Model Family	Architecture	Key Features
GPT‑4 / GPT‑3	Transformer (decoder‑only)	Causal attention, large scale
Llama 2/3	Transformer (decoder‑only)	RoPE, RMSNorm, grouped‑query attention
Gemini	Transformer (decoder‑only)	Multi‑modal (text, image, audio)
CodeLlama	Fine‑tuned Llama	Specialised for code generation
LLaMA‑GRPO	Transformer	Reinforcement learning from preferences
Pros and Cons
Pros ✅	Cons ❌
Simple, stable training (teacher forcing)	Sequential generation is slow (O(seq_len) passes)
State‑of‑the‑art for text, code, music	No bidirectional context (unlike BERT)
Can generate arbitrarily long sequences	Prone to error accumulation (drift)
Easy to condition on prompts	Less control over global structure
