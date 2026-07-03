# neural-grindset / LLM Concepts / Prompting.md

## Edit

# Prompting & Decoding Parameters (Temperature, Top‑k, Top‑p)

This guide covers two essential aspects of working with LLMs:
1. **Prompting** – How to structure inputs to get the desired output.
2. **Decoding Parameters** – How to control randomness, diversity, and coherence during generation.

---

## Part 1: Prompting

Prompting is the art and science of crafting input text to guide a language model toward a specific output. The model doesn't "understand" intent – it predicts the most probable continuation based on the prompt.

### Basic Prompt Structure

[System] → [User] → [Assistant] → (generation)

System: Sets the behaviour, tone, and persona.
User: The actual question or instruction.
Assistant: The model's response (or start of it).


### Types of Prompting

| Technique               | Description                                                                 | Example                                                           |
|-------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------|
| **Zero‑shot**           | No examples; just instruction.                                             | *"Classify this text as positive or negative: 'I love this!'"*    |
| **Few‑shot**            | Provide 1–5 examples before the actual query.                              | *"Positive: 'Great!'\nNegative: 'Terrible.'\nClassify: 'Okay.'"*   |
| **Chain‑of‑Thought (CoT)** | Force the model to reason step‑by‑step before answering.                 | *"Let's think step by step. First, ... Therefore, the answer is..."* |
| **Role‑based**          | Assign a persona / role to the model.                                     | *"You are a senior Python developer. Review this code..."*        |
| **System Prompt**       | Permanent instructions that override user behaviour (API, e.g., OpenAI).  | *"You are a helpful assistant that only speaks in haikus."*      |
| **Instruction (ChatML)** | Clear, imperative statements. Very effective with instruction‑tuned models. | *"Summarise the following text in two sentences:"*              |

### Prompt Engineering Best Practices

- **Be specific** – Vague prompts yield vague outputs.
- **Use delimiters** – `---`, `###`, or triple backticks to separate instructions from data.
- **Assign a role** – "You are an expert historian..." improves factual grounding.
- **Ask for citations** – "Cite the relevant paragraph" reduces hallucination.
- **Specify output format** – JSON, Markdown, bullet points, etc.

---

## Part 2: Decoding / Sampling Parameters

After the model computes logits (raw scores) for each token in the vocabulary, **decoding** converts these logits into a selected token. The parameters below control this conversion.

### The Generation Pipeline (ASCII)

┌─────────────────┐
│ Model Logits │
│ (raw scores) │
└────────┬────────┘
│
▼
┌───────────────────────────┐
│ Temperature Scaling │
│ logits = logits / T │
└────────────┬──────────────┘
│
▼
┌────────────────────────────┐
│ Softmax │
│ probs = softmax(logits) │
└────────────┬───────────────┘
│
▼
┌────────────────────────────┐
│ Top‑k Filter │
│ (keep only top k tokens) │
└────────────┬───────────────┘
│
▼
┌────────────────────────────┐
│ Top‑p (nucleus) Filter │
│ (keep cumulative prob ≥ p)│
└────────────┬───────────────┘
│
▼
┌────────────────────────────┐
│ Sample (or Argmax) │
│ Select final token │
└────────────────────────────┘

text

> **Note:** Order matters. Most implementations apply **Temperature → Softmax → Top‑k → Top‑p → Sample**.

---

## Temperature (T)

Temperature scales the logits **before** the softmax. It controls the "sharpness" of the probability distribution.

### Formula
softmax(logits / T) = exp(logitᵢ / T) / Σⱼ exp(logitⱼ / T)

text

### Visual Effect (ASCII distribution)
Raw logits: [3.0, 2.0, 1.0, 0.5, 0.1]
Softmax (T=1): [0.45, 0.25, 0.15, 0.10, 0.05] (default, balanced)

T = 0.3 (Low): [0.80, 0.15, 0.03, 0.01, 0.01] (sharp → greedy)
T = 0.0 (Argmax): [1.00, 0.00, 0.00, 0.00, 0.00] (deterministic)

T = 1.5 (High): [0.30, 0.22, 0.18, 0.14, 0.12] (flat → random)
T = ∞ (uniform): [0.20, 0.20, 0.20, 0.20, 0.20] (pure randomness)

text

### Practical Values

| Temperature | Effect                                       | Best Use Case                        |
|-------------|----------------------------------------------|--------------------------------------|
| 0.0 – 0.3   | Very low randomness (near‑greedy)            | Code generation, exact Q&A, parsing  |
| 0.5 – 0.7   | Balanced (some diversity, still factual)     | General chat, summarisation          |
| 0.8 – 1.0   | Creative but coherent                        | Storytelling, brainstorming          |
| 1.2 – 2.0   | High randomness (may become incoherent)      | Idea generation, poetry (experimental)|

> **Warning:** Setting `temperature = 0` is often approximated by `do_sample=False` (greedy decoding). In Hugging Face, set `do_sample=False` or `temperature=0.0` + `do_sample=True`.

---

## Top‑k Sampling

Top‑k restricts the vocabulary to the `k` most probable tokens and re‑normalises the probabilities among them. All other tokens get probability `0`.

### How It Works
Sorted tokens: A(0.4), B(0.3), C(0.15), D(0.08), E(0.04), F(0.02), ...
Top‑k = 3: Keep only A, B, C → renormalise → [0.47, 0.35, 0.18]
Tokens D, E, F... are discarded.

text

### Pros & Cons

| Pros ✅                                     | Cons ❌                                         |
|--------------------------------------------|------------------------------------------------|
| Prevents very low‑probability "garbage" tokens | Hard‑coded `k` may be too large/small for different contexts |
| Simple and fast                            | May still include bad tokens if `k` is too high |
| Works well with moderate `k` (e.g., 40–100) | If `k=1`, it's just greedy decoding           |

### Common Values

| k      | Effect                                                   |
|--------|----------------------------------------------------------|
| 1      | Greedy (fully deterministic).                            |
| 10–20  | Very strict; mostly top candidates.                      |
| 40–50  | Balanced (common default in many models).                |
| 100+   | Very lenient; almost no filtering.                       |

---

## Top‑p (Nucleus Sampling)

Top‑p (nucleus sampling) dynamically selects the **smallest set of tokens** whose cumulative probability exceeds a threshold `p`. It adapts to the shape of the distribution.

### How It Works
Sorted probs: A(0.5), B(0.3), C(0.15), D(0.03), E(0.02)
Cumulative: 0.5, 0.8, 0.95, 0.98, 1.00

Top‑p = 0.9: Keep A, B, C (cum = 0.95 ≥ 0.9) → renormalise.
Tokens D & E are discarded.

text

### Visual Comparison: Top‑k vs. Top‑p
Distribution A (steep): [0.6, 0.3, 0.05, 0.03, 0.02]
Top‑k=3 → keeps 3 tokens. Top‑p=0.9 → keeps 3 tokens (similar).

Distribution B (flat): [0.2, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08]
Top‑k=3 → keeps 3 (too strict). Top‑p=0.9 → keeps 6 tokens (adapts!).

text

### Pros & Cons

| Pros ✅                                     | Cons ❌                                         |
|--------------------------------------------|------------------------------------------------|
| Adaptive – works for both sharp & flat distributions | Slightly more compute (needs sorting/cumulative sum) |
| Better than Top‑k for diverse generation   | If `p` is too low, output becomes repetitive.   |
| State‑of‑the‑art default (0.9–0.95)        | May occasionally include awkward tokens if the distribution is very flat. |

### Common Values

| p      | Effect                                                   |
|--------|----------------------------------------------------------|
| 0.0    | Greedy (only top token).                                 |
| 0.5    | Strict; only very high‑confidence tokens.                |
| 0.9    | Balanced (most common default).                          |
| 0.95   | Slightly more diverse than 0.9.                          |
| 1.0    | No filtering (full vocabulary).                          |

---

## Combining Temperature, Top‑k, and Top‑p

Most modern LLM APIs allow you to set all three simultaneously. The pipeline is:

1. **Scale logits by Temperature** (make sharp or flat).
2. **Apply Softmax** to get probabilities.
3. **Apply Top‑k** (keep top k).
4. **Apply Top‑p** (keep cumulative mass p).
5. **Sample** from the remaining distribution.

### Recommended Combinations

| Use Case                     | Temperature | Top‑k | Top‑p | do_sample |
|------------------------------|-------------|-------|-------|-----------|
| **Deterministic (Q&A, code)**| 0.0         | –     | –     | False     |
| **Balanced (chat)**          | 0.7         | 50    | 0.95  | True      |
| **Creative (storytelling)**  | 0.9         | 40    | 0.90  | True      |
| **Brainstorming**            | 1.2         | 100   | 0.95  | True      |
| **Factual (RAG)**            | 0.3         | 40    | 0.90  | True      |

### Code Example (Hugging Face)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

prompt = "The future of artificial intelligence is"

inputs = tokenizer(prompt, return_tensors="pt")

# Greedy (deterministic)
outputs_greedy = model.generate(**inputs, max_new_tokens=50, do_sample=False)

# Sampling with parameters
outputs_sample = model.generate(
    **inputs,
    max_new_tokens=50,
    do_sample=True,           # Must be True for sampling
    temperature=0.7,
    top_k=50,
    top_p=0.95,
    repetition_penalty=1.1    # Bonus: penalises repeated tokens
)

print(tokenizer.decode(outputs_sample[0], skip_special_tokens=True))
```
Code Example (OpenAI API)
```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "Write a haiku about code."}],
    temperature=0.8,
    top_p=0.9,
    max_tokens=100
)

print(response.choices[0].message.content)
```

Greedy Decoding vs. Sampling
Strategy	How It Works	Pros	Cons
Greedy (argmax)	Always picks the highest‑probability token.	Deterministic, fast	Repetitive, lacks creativity
Beam Search	Keeps k most probable sequences, picks best.	Higher quality for MT	Expensive, still repetitive
Sampling (with T/Top)	Randomly picks from the probability distribution.	Creative, diverse	Can hallucinate / drift
Repetition Penalty (Bonus)
Though not part of T/Top‑k/Top‑p, repetition penalty is essential to avoid loops.

How it works: Decreases the logits of tokens that have already appeared.

Value range: 1.0 (no penalty) to 1.2–2.0 (aggressive).

Common default: 1.05 or 1.1.

```python
# Hugging Face
outputs = model.generate(..., repetition_penalty=1.1)

# OpenAI (uses frequency_penalty and presence_penalty)
# frequency_penalty: reduces repetition based on token frequency.
# presence_penalty: penalises tokens that have already appeared at least once.
```
