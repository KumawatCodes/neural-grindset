---
title: "Transformer Architecture"
phase: "Phase-1 — Core AI Foundations"
group: "02_LLM-Fundamentals"
tags: [ai-engineering, phase-1, study-notes]
status: empty
created: 2026-06-07
---
# Transformer Architecture

## 1. Executive Summary

The Transformer is the engine inside every model you call through an API — GPT, Claude, Gemini, Llama. It is a neural network design built around one trick: every token looks at every other token directly, instead of passing information step-by-step like older models did. That one trick is why these models can be trained on thousands of GPUs in parallel, and it's also the reason long context is expensive (cost grows quadratically with sequence length).

You'll hit this topic the moment you ask "why is my 50K-token prompt 4x slower than my 25K-token prompt" or "why does this model need so much GPU memory just sitting idle." Everything downstream in this knowledge base — KV-cache, context windows, pricing — is a direct consequence of how the Transformer is built.

### 30-Second Interview Answer

"A Transformer processes a sequence using self-attention: every token computes a relevance score against every other token, and uses that to build a context-aware representation. This replaced RNNs because it can be parallelized across GPUs and captures long-range dependencies more effectively. The catch is that attention costs grow quadratically with sequence length, which is why production systems now layer on tricks like FlashAttention, KV-caching, and Mixture-of-Experts on top of the base design."

### 2-Minute Interview Answer

"Before Transformers, sequence models (RNNs/LSTMs) processed tokens one at a time, so training couldn't be parallelized and long-range dependencies decayed. The 2017 'Attention Is All You Need' paper replaced recurrence with self-attention: for each token, compute Query, Key, and Value vectors, then score every token against every other token using QK^T, scale it, softmax it, and use that to weight the Value vectors. Stack this with feed-forward layers, residual connections, and layer normalization, and you get a block you can stack N times.

What changed since 2017: positional encoding moved from fixed sine waves to RoPE (rotary embeddings), which lets models extrapolate to much longer contexts. The feed-forward activation moved from GELU to SwiGLU for better training stability. Normalization moved before the sub-layer (Pre-LN) instead of after, for stability at scale. And at the system level, nobody runs a single dense Transformer anymore — production models use Mixture-of-Experts (only 2 of 16 experts active per token), FlashAttention kernels to make the O(n²) attention cheaper in practice, and KV-caching so you don't recompute attention for tokens you've already processed. The core math hasn't changed; the engineering around it has."

---

## 2. The Real Engineering Problem

Picture trying to train a translation model in 2016 using an RNN. To process word 50 in a sentence, the model first has to process words 1 through 49, in order, one at a time. You cannot parallelize this across GPUs the way you parallelize matrix multiplications — the computation for token 50 literally depends on the output for token 49.

This creates two pains for engineers: training is slow because GPUs sit underutilized waiting for sequential steps, and long sentences lose information because signal from early tokens fades by the time it reaches token 50 (the "vanishing gradient" problem in long sequences). Attempts to patch this (LSTMs, GRUs, attention bolted onto RNNs) helped but didn't remove the sequential bottleneck.

Google needed a model that could be trained on machine translation at a scale where GPU parallelism was the only way to make the economics work. They needed every token to be computable independently, with the relationships between tokens captured through math rather than through sequential passing.

---

## 3. Why This Exists

Self-attention exists to solve the parallelization problem and the long-range dependency problem at the same time. If every token computes its relationship to every other token through a matrix multiplication (instead of a sequential loop), you can compute the entire layer in one parallel operation on a GPU. And because every token has a direct path to every other token (not a 50-step relay), long-range dependencies don't decay.

If self-attention disappeared tomorrow, the field would partially regress to recurrent or convolutional architectures, which scale worse on modern GPU hardware. That's also exactly why State Space Models (Mamba) and other alternatives are now being explored — not because attention is "wrong," but because its O(n²) cost is becoming the new bottleneck once you've solved the parallelization problem.

---

## 4. Mental Model

Think of a Transformer layer as a room full of people at a conference, where everyone needs to update their understanding of the conversation by listening to everyone else, simultaneously, in one round.

- Each person (token) has three things: a **Query** ("what am I looking for?"), a **Key** ("what do I represent so others can find me?"), and a **Value** ("what information do I actually carry?").
- Every person compares their Query against everyone else's Key to get a relevance score. High relevance means "I should pay attention to you."
- Those scores get turned into weights (via softmax) and used to blend everyone's Values into a new, context-aware representation for each person.

This entire exchange happens in one parallel "round," not a chain. Stack 32-96 of these rounds (layers), and each round refines everyone's understanding a bit further.

### How To Visualize It

```
Input tokens:      [The]  [cat]  [sat]  [on]  [mat]
                      |      |      |      |     |
              Each token computes Q, K, V vectors
                      |      |      |      |     |
        Attention:  every token's Q is compared to every token's K
                      (this is the n × n matrix — the O(n²) cost)
                      |      |      |      |     |
              Weighted blend of all Values → new representation
                      |      |      |      |     |
                  Feed-forward layer (per-token, independent)
                      |      |      |      |     |
                 Output: context-aware token representations
```

Stack this block N times. Each stack lets information travel further and combine in more complex ways — by the last layer, "sat" knows it relates to "cat" (subject) and "mat" (location), without ever having been told that explicitly.

---

## 5. Engineering Evolution

```
Problem: Sequential models (RNN/LSTM) can't parallelize, decay over long sequences
↓
Old Solution: RNN + attention bolted on (Bahdanau attention, 2014)
↓
Limitation: Still sequential at its core, attention helped but didn't remove the bottleneck
↓
New Solution: Pure self-attention, no recurrence (Transformer, 2017)
↓
Current Best Practice: Transformer + RoPE + SwiGLU + Pre-LN + FlashAttention + MoE + KV-cache + quantization
↓
Current Limitation: Attention is O(n²) — cost and memory explode past ~1M tokens
↓
Future Direction: Sparse attention, hybrid attention+recurrence, State Space Models (Mamba) for linear-time scaling
```

---

## 6. Vocabulary Map

|Term|Meaning|Why It Exists|Where Used|Aliases|
|---|---|---|---|---|
|Self-Attention|Each token scores relevance against every other token|Removes sequential bottleneck, captures long-range deps|Every Transformer layer|Scaled dot-product attention|
|Query/Key/Value (Q/K/V)|Three learned projections of each token|Splits "what I want" from "what I offer" from "what I carry"|Inside attention computation|QKV|
|Multi-Head Attention|Run attention several times in parallel with different learned projections|One attention pattern can't capture all relationship types (syntax, semantics, position)|Every attention layer|MHA|
|Positional Encoding|Injects token order info, since attention itself is order-blind|Without it, "cat sat on mat" = "mat on sat cat" to the model|Input embeddings or inside attention|RoPE, ALiBi|
|RoPE|Rotary Positional Embedding — encodes position as a rotation in vector space|Lets models extrapolate to far longer contexts than they were trained on|Llama, most modern open models|Rotary embeddings|
|FFN (Feed-Forward Network)|Per-token MLP applied after attention|Attention mixes information between tokens; FFN processes it per-token|Every Transformer block|MLP block|
|SwiGLU|Activation function used in modern FFNs|More stable training than GELU at scale|GPT, Llama, most 2024+ models|Swish-Gated Linear Unit|
|LayerNorm / Pre-LN|Normalization applied before each sub-layer|Keeps training stable as models get deeper|Every Transformer block|Pre-normalization|
|FlashAttention|GPU kernel that computes attention without materializing the full n×n matrix in memory|Standard attention is memory-bound; this makes it I/O-efficient|All production inference engines|FA, FA-2, FA-3|
|KV-Cache|Stored Key/Value vectors from previous tokens|Avoids recomputing attention for tokens already processed|Every autoregressive generation step|(see KV-cache note)|
|MoE (Mixture of Experts)|Multiple FFN "experts" per layer; a router activates only a few per token|Lets you scale parameter count without scaling compute per token|GPT-4, Mixtral, Claude (reportedly)|Sparse MoE|
|Sparse Attention|Each token attends to a subset of tokens, not all|Reduces O(n²) cost for long sequences|Long-context models|Sliding window attention|
|SSM (State Space Model)|Alternative to attention; processes sequence with linear-time recurrence|Avoids O(n²) cost entirely|Mamba, hybrid models|Mamba|

---

## 7. System Placement

```
User prompt
   ↓
Tokenizer (text → token IDs)
   ↓
Embedding layer (token IDs → vectors)
   ↓
Transformer stack (N layers of: Self-Attention → FFN, with residuals + norm)
   ↓
Final LayerNorm + output projection (vector → vocabulary logits)
   ↓
Sampling/decoding (logits → next token)
   ↓
Detokenizer (token IDs → text)
   ↓
Response to user
```

The Transformer block sits at the heart of this pipeline. Everything before it (tokenization, embeddings) prepares input; everything after it (sampling, decoding) decides what to do with its output.

---

## 8. Internal Working

Trace one token, "cat," through a single Transformer layer:

1. **Embedding**: "cat" is converted to a vector, e.g. `[0.2, -0.4, 0.1, ...]`, of size `d_model` (e.g. 4096 for a mid-size model).
2. **Positional info added**: RoPE rotates this vector based on "cat"'s position in the sequence (position 2 of 5).
3. **Q/K/V projection**: Three separate learned weight matrices transform this vector into a Query vector, a Key vector, and a Value vector.
4. **Attention scores**: "cat"'s Query is dot-producted against every other token's Key (including its own), producing one raw score per token. These scores are scaled by `1/√d_k` to keep gradients stable.
5. **Softmax**: Scores are turned into a probability distribution — e.g., "cat" might end up attending 60% to itself, 25% to "sat," 10% to "The," 5% to others.
6. **Weighted sum**: "cat"'s new representation is the weighted sum of all tokens' Value vectors, using those attention weights.
7. **Multi-head repeat**: Steps 3-6 happen in parallel across 8-128 "heads," each with its own learned Q/K/V projections, capturing different relationship types. Results are concatenated.
8. **Residual + Norm**: The original "cat" vector is added back (residual connection) and normalized.
9. **FFN**: The result passes through a per-token feed-forward network (expand → SwiGLU activation → contract).
10. **Residual + Norm again**: Add and normalize.
11. **Repeat for N layers**: This entire process repeats 32-96+ times, each layer refining "cat"'s representation further using increasingly abstract relationships.
12. **Output**: After the final layer, "cat"'s vector is projected onto the vocabulary to produce logits — a score for every possible next token, if "cat" happens to be the last token being decoded.

---

## 9. Core Components

**Self-Attention**

- Purpose: build context-aware representations by mixing information across tokens.
- Input: Q, K, V vectors for all tokens.
- Output: new vector per token, blended from all tokens' Values.
- Internal logic: scaled dot-product + softmax weighting.
- Failure case: if sequence is too long, attention either truncates (losing info) or costs explode (O(n²) compute and memory).

**Multi-Head Attention**

- Purpose: capture multiple types of relationships simultaneously (e.g., syntactic vs. semantic).
- Input: same as self-attention, split across heads.
- Output: concatenated per-head outputs, projected back to `d_model`.
- Internal logic: parallel independent attention computations.
- Failure case: too few heads can't capture relationship diversity; too many heads add overhead without benefit past a point.

**Feed-Forward Network (FFN)**

- Purpose: per-token non-linear transformation, independent of other tokens.
- Input: attention output for one token.
- Output: transformed vector, same dimensionality.
- Internal logic: expand to a larger hidden dimension, apply SwiGLU, contract back down.
- Failure case: this is where most of a dense model's parameters live — undersized FFNs limit model capacity; this is also the part MoE replaces with multiple sparse "experts."

**Positional Encoding (RoPE)**

- Purpose: inject order information since attention has no inherent sense of sequence.
- Input: token position index.
- Output: a rotation applied to Q/K vectors.
- Internal logic: rotates vectors by an angle proportional to position, so relative position is encoded in the dot product.
- Failure case: extrapolating far beyond the trained context length degrades quality — this is part of why "advertised" context windows often underperform near their limit.

**Residual Connections + LayerNorm**

- Purpose: keep gradients flowing through very deep networks; stabilize training.
- Input: sub-layer output + the input that went into the sub-layer.
- Output: normalized sum.
- Internal logic: `output = LayerNorm(input + SubLayer(input))`.
- Failure case: without these, deep Transformers (50+ layers) become untrainable — gradients vanish or explode.

---

## 10. Practical Usage

### Installation

```bash
pip install torch transformers --break-system-packages
```

### Imports

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
```

### Basic Example

```python
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

inputs = tokenizer("The cat sat on the", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=5)
print(tokenizer.decode(outputs[0]))
```

This loads a small Transformer (GPT-2), tokenizes a prompt, and generates 5 more tokens autoregressively — internally running the exact attention/FFN steps from Section 8 once per generated token.

### Real Example (inspecting attention)

```python
outputs = model(**inputs, output_attentions=True)
attn = outputs.attentions[0]  # layer 0 attention weights
print(attn.shape)  # [batch, heads, seq_len, seq_len]
```

This pulls out the raw attention weight matrix for layer 0 — the actual n×n scores from step 5 above. Useful for debugging "why did the model focus on the wrong part of my prompt."

### Common Libraries

- `transformers` (HuggingFace) — model loading, tokenization, generation
- `vllm` — production-grade inference serving with PagedAttention/KV-cache management
- `flash-attn` — FlashAttention CUDA kernels
- `deepspeed` / `megatron-lm` — training-scale Transformer infrastructure

### Common APIs

- OpenAI Chat Completions / Responses API
- Anthropic Messages API
- HuggingFace `model.generate()`

### Configuration Options

- `num_attention_heads`, `hidden_size`, `num_hidden_layers` — architecture size
- `rope_theta` — controls RoPE's extrapolation behavior
- `attn_implementation="flash_attention_2"` — use FlashAttention kernel instead of naive attention

### Expected Output

A generated continuation of your prompt, token by token, each one produced by one full forward pass through the entire Transformer stack.

---

## 11. Production Usage

OpenAI's GPT-4o and Anthropic's Claude both run on Mixture-of-Experts Transformer variants — a 1-trillion-parameter model with only ~50B parameters active per token, giving the knowledge capacity of a huge model with the inference cost of a much smaller one. Google's Gemini 1.5 Pro pairs the same core architecture with FlashAttention-3 and RoPE to reach million-token context windows. Meta ships Llama 3 as a dense (non-MoE) Transformer with RoPE, which is part of why it's a popular self-hosting choice — dense models are simpler to deploy and reason about than MoE.

At production scale, nobody runs FP16 weights anymore — INT8 or FP4 quantization is standard, trading a small accuracy hit for major memory and speed wins. Reliability at this scale depends heavily on FlashAttention-class kernels: without them, attention's memory bandwidth requirements alone would make serving million-token contexts uneconomical.

---

## 12. Design Decisions

**Why self-attention over recurrence?** Parallelizability. RNNs are simpler conceptually but can't use GPU parallelism across the sequence dimension. The tradeoff is O(n²) cost vs. RNN's O(n) — Transformers pay more per token at long lengths but gain massively in training throughput at moderate lengths.

**Why Pre-LN over Post-LN?** Pre-LN (normalize before the sub-layer) gives more stable gradients in very deep networks, at a very slight cost to final performance ceiling. Post-LN can outperform at small scale but becomes unstable past ~20 layers without careful learning rate warmup.

**Why RoPE over learned absolute positional embeddings?** RoPE encodes relative position implicitly in the attention dot product, which generalizes to sequence lengths longer than what the model was trained on. Learned absolute embeddings have a hard length cutoff — the model has literally never seen position 50,001 if it was trained at 50,000.

**Why MoE over a bigger dense model?** A dense model with 1T parameters costs 1T-parameters-worth of compute per token. An MoE with 1T total parameters but only 2 of 16 experts active per token costs roughly 1/8th that — you get to store more "knowledge" without paying for it on every single token. The cost is routing complexity and harder, less stable training.

---

## 13. Tradeoff Matrix

|Decision|Speed|Cost|Memory|Complexity|Scalability|Reliability|
|---|---|---|---|---|---|---|
|Dense Transformer|Baseline|Baseline|Baseline|Low|Limited by compute per token|High (well understood)|
|MoE Transformer|Lower latency per token|Lower per-token cost|Higher (stores all experts)|High (routing)|High (scales params cheaply)|Medium (routing instability risk)|
|FlashAttention vs naive attention|2-5x faster|Lower (less GPU time)|Much lower|Medium (custom kernel)|Higher (longer contexts feasible)|High|
|RoPE vs learned absolute PE|Same|Same|Same|Medium|Higher (extrapolates)|High|
|Sparse attention vs full attention|Faster at long context|Lower|Lower|High|Higher|Medium (can miss distant dependencies)|

---

## 14. Cost Impact

- **Compute**: attention cost scales as O(n²) with sequence length — doubling your prompt length quadruples attention compute specifically (though total cost growth is less extreme once you account for the FFN, which scales linearly).
- **Memory**: every layer's Q/K/V intermediate tensors and the KV-cache (Section covered in its own note) consume GPU memory proportional to sequence length × number of layers × hidden size.
- **GPU/Cloud cost**: MoE lets you serve a "smarter" model without proportionally higher GPU cost per request — this is the main lever providers use to keep frontier-model pricing from exploding as model size grows.
- **Engineering complexity**: every optimization in this note (FlashAttention, MoE, quantization) adds real implementation and debugging surface area. A naive from-scratch Transformer is ~200 lines; a production-grade one with all these optimizations is a multi-team effort.

Practical example: if you're building something like your CodeRed or CodeSentinel platforms on top of an API, the architecture choices here are invisible to you — but they directly explain why a 100K-token codebase review costs noticeably more and takes longer than a 2K-token code snippet review, and why that cost doesn't scale linearly.

---

## 15. Failure Modes

**Technical Failure: Attention memory blowup**

- Cause: naive attention materializes the full n×n score matrix.
- Symptoms: CUDA out-of-memory errors at long context lengths.
- Fix: use FlashAttention or a serving engine (vLLM) that implements memory-efficient attention.

**Scaling Failure: Quality degradation near advertised context limit**

- Cause: models are often unreliable well before their advertised max context (a 200K model can degrade noticeably by ~130K).
- Symptoms: model "forgets" details from the middle of a long prompt ("lost in the middle").
- Fix: don't trust the advertised number — test retrieval at your actual expected context length; use RAG to keep prompts shorter when possible.

**Operational Failure: MoE routing collapse**

- Cause: during training, a router can learn to send almost all tokens to the same few experts, wasting the rest.
- Symptoms: model behaves like a much smaller dense model than its parameter count suggests.
- Fix: load-balancing losses during training (not something you control at inference time, but worth knowing why some MoE models underperform their parameter count).

**Production Failure: Position extrapolation breakdown**

- Cause: pushing RoPE-based models far beyond their trained context length without scaling tricks.
- Symptoms: coherence collapses past a certain length even though the model "supports" longer context.
- Fix: use models with explicitly validated long-context training (not just architectural support for long RoPE), and verify with your own long-context tests.

---

## 16. Optimization Techniques

- **FlashAttention**: rewrite attention to avoid materializing the full score matrix, cutting memory bandwidth usage and increasing throughput 2-5x.
- **Quantization (INT8/FP4)**: reduce weight precision to shrink memory footprint and speed up matrix multiplications, at a small accuracy cost.
- **MoE**: scale parameter count (knowledge capacity) without scaling per-token compute.
- **KV-caching**: avoid recomputing attention for already-processed tokens (own note covers this in depth).
- **Sparse/sliding-window attention**: limit each token's attention to a local window or a fixed pattern, cutting O(n²) toward O(n log n) or O(n).
- **Ring Attention**: split a single very-long-sequence attention computation across multiple GPUs, enabling training/inference contexts that don't fit on one device.

---

## 17. Interview Preparation

### Beginner Questions

**Q: What problem does self-attention solve that RNNs couldn't?** A: Parallelization and long-range dependency capture. RNNs process tokens sequentially, so you can't parallelize across the sequence and information decays over long distances. Self-attention lets every token directly attend to every other token in one parallel step. _Reasoning expected_: understanding the sequential bottleneck, not just naming attention.

**Q: What are Q, K, and V?** A: Three learned projections of each token's embedding — Query (what I'm looking for), Key (what I offer for others to match against), Value (what information I actually carry if matched). _Reasoning expected_: not just definitions, but why three separate vectors instead of one.

### Intermediate Questions

**Q: Why is attention O(n²)?** A: Because every token computes a score against every other token — n tokens × n tokens = n² score computations, each one a dot product over the head dimension. _Reasoning expected_: derive it, don't just recite it.

**Q: Why do modern models use RoPE instead of the original sinusoidal positional encoding?** A: RoPE encodes position as a rotation baked into the Q/K dot product itself, which generalizes better to sequence lengths beyond training, whereas absolute positional embeddings have a hard length ceiling. _Reasoning expected_: connect to long-context capability.

### Advanced Questions

**Q: How does MoE reduce inference cost without reducing parameter count?** A: A router selects a small subset of expert FFNs (e.g., 2 of 16) per token. Total parameters stored = sum across all experts, but compute per token = only the active experts' compute. This decouples "knowledge capacity" from "per-token compute cost." _Reasoning expected_: candidate should explain the routing mechanism and the train/inference cost split.

**Q: Why might Mamba/SSMs eventually replace attention for some workloads?** A: SSMs process sequences with linear-time recurrence instead of pairwise attention, giving O(n) instead of O(n²) scaling, which matters most at very long context lengths. The tradeoff is that SSMs are newer, less battle-tested, and not yet used in any frontier production model as of mid-2026. _Reasoning expected_: candidate should not overclaim — SSMs are promising, not proven at frontier scale yet.

---

## 18. Common Mistakes

**Mistake**: thinking attention "understands" language the way RNNs do, token by token. _Why it happens_: people picture attention as a sequential read of the text. _Correct understanding_: attention computes all token relationships in parallel in one matrix operation — there's no "left to right" intrinsic to the math itself (positional encoding is what gives it order awareness).

**Mistake**: assuming bigger context window = model can use all of it equally well. _Why it happens_: providers market context window size as the main spec. _Correct understanding_: "lost in the middle" is real — effective usable context is often well below the advertised max.

**Mistake**: confusing MoE with ensembling multiple full models. _Why it happens_: "multiple experts" sounds like multiple separate models. _Correct understanding_: MoE experts are just multiple FFN blocks within the same layer, sharing the same attention mechanism, with a router picking a few per token — it's one model, not an ensemble.

---

## 19. Current Industry State

As of mid-2026, every frontier model (GPT-4o family, Claude, Gemini, Llama) is built on a Transformer foundation, but the "vanilla" 2017 design is essentially never deployed as-is. The de facto production stack layers RoPE for positions, SwiGLU for activations, Pre-LN for stability, FlashAttention-3 for efficient compute, MoE for scaling parameter count cheaply, and INT8/FP4 quantization for deployment efficiency. OpenAI and Mistral both run MoE variants; Google leans on FlashAttention-3 plus RoPE to push toward million-token contexts; Meta's Llama stays dense, favoring deployment simplicity for the open-weight ecosystem.

What's becoming obsolete: FP16 inference (replaced by lower-precision quantization), and naive full attention without a memory-efficient kernel.

---

## 20. Current Problems & Research

The unresolved core issue is still the O(n²) attention cost — doubling context length quadruples the attention-specific compute, and KV-cache memory grows with it too, which is why long-context serving is so much more expensive and slower than short-context serving. Research is split across three fronts: making attention itself cheaper (sparse attention, FlashAttention-class kernels, Ring Attention for distributed long-context), replacing attention for parts of the stack (State Space Models like Mamba, which scale linearly and reportedly outperform Transformers on certain long-range benchmarks), and hybrid designs that combine attention with recurrence and external memory for better reasoning over very long contexts. None of the SSM or hybrid approaches have displaced attention in a frontier production model yet — they remain promising but unproven at that scale as of this writing.

The foundational papers worth knowing: "Attention Is All You Need" (2017, introduced the architecture), "Mamba: Linear-Time Sequence Modeling" (2023, the leading SSM alternative), and the FlashAttention line of papers (2022-2024, the efficiency breakthrough that made long-context serving practical at all).

---

## 21. Future Evolution

The most likely near-term path is not "Transformers get replaced" but "Transformers get hybridized" — combining attention layers (good at precise retrieval over context) with SSM-style layers (good at cheap long-range summarization) within the same model. Sparse and dynamic attention patterns (where the model learns which tokens matter enough to attend to fully) are likely to become standard rather than exotic. A pure SSM frontier model replacing attention entirely is possible but not yet demonstrated at the scale and quality of current frontier Transformers.

---

## 22. Engineer Checklist

[ ] Explain self-attention and why it replaced RNNs [ ] Explain Q/K/V and the attention formula from memory [ ] Explain why attention is O(n²) and what that costs in production [ ] Explain RoPE, SwiGLU, Pre-LN and why each replaced its predecessor [ ] Explain MoE and how it decouples parameter count from per-token compute [ ] Use HuggingFace `transformers` to load and run a model, inspect attention weights [ ] Discuss FlashAttention's role in production serving [ ] Recognize "lost in the middle" as a real production bottleneck, not a tutorial footnote [ ] Discuss tradeoffs between dense and MoE architectures [ ] Connect this topic to KV-cache, context windows, and inference cost (the rest of this knowledge base)

---

## 23. Knowledge Graph

```
Transformer Architecture
├── Self-Attention
│   ├── Q/K/V projections
│   ├── Multi-Head Attention
│   └── Scaled dot-product formula
├── Positional Encoding
│   ├── Original sinusoidal (historical)
│   └── RoPE (current standard)
├── Feed-Forward Network
│   ├── SwiGLU activation
│   └── MoE (sparse experts)
├── Stabilization
│   ├── Residual connections
│   └── Pre-LN normalization
├── Efficiency Layer (system-level, not architecture-level)
│   ├── FlashAttention
│   ├── KV-Cache
│   └── Quantization (INT8/FP4)
└── Alternatives / Future
    ├── Sparse Attention
    ├── Ring Attention (distributed long-context)
    └── State Space Models (Mamba)
```

---

## 24. If You Remember Only 10 Things

1. Self-attention lets every token directly relate to every other token, in parallel — that's why Transformers train fast on GPUs.
2. Q/K/V: Query asks, Key offers, Value delivers. The dot product of Q and K decides how much of V you get.
3. Attention cost is O(n²) — this single fact explains most long-context pricing and latency behavior in this whole knowledge base.
4. Multi-head attention runs several attention "views" in parallel to capture different relationship types.
5. RoPE encodes position as a rotation, which is why modern models can (somewhat) extrapolate beyond their trained length.
6. SwiGLU and Pre-LN are the modern, more stable replacements for GELU and Post-LN — small tweaks, big stability gains at scale.
7. MoE lets a model store huge knowledge (trillions of parameters) while only paying compute for a small active subset per token.
8. FlashAttention doesn't change the math — it changes how attention is computed on the GPU to avoid memory bottlenecks.
9. "Lost in the middle" is real: advertised context length ≠ effective usable context length.
10. The field's bottleneck has shifted from "can we parallelize training" (solved by attention in 2017) to "can we make O(n²) cheap enough for million-token contexts" (the active research frontier today: sparse attention, SSMs, hybrids).