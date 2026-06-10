
# Autoregressive Models

Autoregressive (AR) models generate sequences **one element at a time**, conditioning each new element on the previously generated ones. They are the foundation of modern large language models (LLMs) like GPT‑4, Llama, and Gemini.

## Core Idea

Given a sequence `x₁, x₂, ..., xₜ`, an autoregressive model learns the conditional probability distribution:

P(x₁, x₂, ..., xₜ) = Πᵢ P(xᵢ | x₁, ..., xᵢ₋₁)

text

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
