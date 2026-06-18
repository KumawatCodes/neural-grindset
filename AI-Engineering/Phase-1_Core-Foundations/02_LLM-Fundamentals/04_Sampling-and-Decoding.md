---
title: "Sampling & Decoding"
phase: "Phase-1 — Core AI Foundations"
group: "02_LLM-Fundamentals"
tags: [ai-engineering, phase-1, study-notes]
status: empty
created: 2026-06-07
---
# Sampling & Decoding

## 1. Executive Summary

Sampling and decoding is the step where the model's raw output — a probability distribution over its entire vocabulary for "what token comes next" — gets turned into an actual chosen token. The model itself never directly outputs text; it outputs scores (logits), and a decoding strategy decides how to pick from them. This is why the exact same model, same prompt, can produce wildly different outputs depending on `temperature`, `top_p`, or `top_k` settings — and it's also where a major chunk of inference speed optimization (speculative decoding) happens.

You'll deal with this directly whenever you tune `temperature` for a chatbot, debug repetitive or incoherent output, or care about inference latency for a real-time application.

### 30-Second Interview Answer

"After the model produces logits (raw scores) for every possible next token, decoding decides how to actually pick one. Greedy decoding always picks the highest-probability token — deterministic but repetitive. Temperature sampling adds controlled randomness; top-k and top-p (nucleus) sampling restrict the random choice to a smaller, more sensible set of candidates so you don't get garbage low-probability tokens. Production systems also use speculative decoding — a small draft model proposes several tokens ahead, and the big model verifies them in one batch — to speed up generation 2-3x without changing the output distribution."

### 2-Minute Interview Answer

"A language model's forward pass ends with logits: one score per vocabulary token, representing how likely it is to be the next token. Softmax turns these into a probability distribution. The simplest decoding strategy, greedy, just picks the single highest-probability token every time — deterministic, but it tends to get stuck in repetitive loops and produces flat, boring text because it never takes a chance on a slightly-lower-probability-but-better token.

Most production chat systems use temperature sampling combined with top-k or top-p. Temperature scales the logits before softmax — lower temperature sharpens the distribution toward the most likely tokens (more focused, less creative), higher temperature flattens it (more random, more creative, more risk of incoherence or hallucination). Top-k restricts sampling to only the k highest-probability tokens; top-p (nucleus sampling) instead takes the smallest set of top tokens whose cumulative probability exceeds p, which adapts the candidate pool size to how confident the model actually is at that step.

Separately from output quality, decoding speed matters a lot for latency-sensitive applications. Speculative decoding uses a small, fast 'draft' model to propose several tokens ahead, then the large model verifies all of them in a single batched pass — if the draft model guessed right, you got several tokens for the cost of one big-model forward pass; if wrong, you fall back gracefully. This gives 2-3x speedup with no change to the output distribution, since the big model still has final say on every token. Newer approaches like Speculative Speculative Decoding push this further by pre-building draft continuations for likely outcomes before verification even starts."

---

## 2. The Real Engineering Problem

Picture an early chatbot using greedy decoding — always picking the most likely next word. Ask it "Tell me about your day" and it might respond "I had a great day. I had a great day. I had a great day." — stuck in a loop, because once "I had a great day" becomes the highest-probability continuation, picking it again becomes the highest-probability choice again, forever. Greedy decoding has no mechanism to break out of locally-optimal repetition.

The opposite extreme — pure random sampling from the full probability distribution — solves the repetition problem but introduces a new one: the vocabulary's "long tail" contains thousands of extremely low-probability, often nonsensical tokens, and even a 0.01% chance of picking garbage compounds badly over a long generation. Engineers needed a way to inject just enough randomness to avoid repetition and add natural variation, without opening the door to incoherent garbage tokens.

---

## 3. Why This Exists

Sampling strategies exist to solve the tension between coherence (favor likely tokens) and diversity/naturalness (avoid robotic repetition). Different applications need different points on that spectrum — code generation wants low temperature (correctness matters more than variety), creative writing wants higher temperature (variety matters more than always picking the safest word).

Speculative decoding exists for a completely different reason: raw autoregressive generation is inherently slow because you must generate one token, wait, generate the next, wait, repeating sequentially — you can't parallelize generation the way you can parallelize the prefill/training step (see Transformer note). Speculative decoding gets around this by guessing ahead and verifying in batches, which is one of the few ways to meaningfully speed up generation without changing the model itself.

---

## 4. Mental Model

Think of decoding like writing a sentence with someone looking over your shoulder, suggesting the next word, but you get to decide how much you trust their top suggestion versus considering a few alternatives.

- **Greedy**: you always take their #1 suggestion, no matter what. Reliable, but boring and prone to loops.
- **Temperature**: you adjust how "confident" their suggestions sound. Low temperature = they only confidently suggest the safest, most obvious word. High temperature = they shrug and suggest something more surprising more often.
- **Top-k**: you only consider their top 20 (or whatever k) suggestions, ignoring anything ranked lower, however small the chance.
- **Top-p (nucleus)**: instead of a fixed number of suggestions, you consider just enough top suggestions to cover, say, 90% of their total confidence — if they're very sure, that might be just 2 words; if they're unsure, that might be 50 words.

### How To Visualize It

```
Logits for next token (raw scores) → Softmax → Probability distribution

Example distribution:
  "happy"   : 0.45
  "great"   : 0.20
  "fine"    : 0.15
  "tired"   : 0.08
  "purple"  : 0.001   ← nonsensical, near-zero probability
  ... (50,000 more tokens, mostly near-zero)

Greedy:        always picks "happy" (highest)
Top-k=3:       only considers {happy, great, fine}, samples among them
Top-p=0.9:     considers {happy, great, fine} (cumulative 0.80) + maybe "tired"
               (cumulative 0.88) — just enough to cross 0.9, excludes "purple"
Temperature:   reshapes the whole distribution before any of the above —
               high temp flattens it (more even odds), low temp sharpens it
               (closer to greedy)
```

---

## 5. Engineering Evolution

```
Problem: Model outputs a probability distribution, not a single answer — something has to choose
↓
Old Solution: Greedy decoding (always pick highest probability)
↓
Limitation: Repetitive loops, low diversity, doesn't reflect real uncertainty
↓
New Solution: Temperature + top-k / top-p (nucleus) sampling
↓
Current Best Practice: Tuned sampling params per use case + speculative decoding for speed
↓
Current Limitation: Sampling params are still mostly hand-tuned per task; sequential generation is inherently slow
↓
Future Direction: Adaptive/auto-tuned sampling per task; Speculative Speculative Decoding (SSD) for maximum throughput overlap
```

---

## 6. Vocabulary Map

|Term|Meaning|Why It Exists|Where Used|Aliases|
|---|---|---|---|---|
|Logits|Raw, unnormalized scores the model outputs for each vocabulary token|The direct output of the model before any probability conversion|Every forward pass's final layer|Raw scores|
|Softmax|Converts logits into a normalized probability distribution|Logits aren't probabilities (they can be negative, don't sum to 1)|Right before sampling|—|
|Temperature|A scaling factor applied to logits before softmax|Controls how sharp or flat the resulting probability distribution is|Every major API (`temperature` param)|—|
|Top-k sampling|Restrict sampling to the k highest-probability tokens|Prevents the long tail of near-zero-probability tokens from ever being picked|Most chat APIs|—|
|Top-p / nucleus sampling|Restrict sampling to the smallest set of top tokens whose cumulative probability exceeds p|Adapts candidate pool size to the model's actual confidence at each step (unlike fixed top-k)|Most chat APIs|Nucleus sampling|
|Greedy decoding|Always pick the single highest-probability token|Simplest possible decoding rule|Deterministic use cases (e.g. classification-style tasks)|Argmax decoding|
|Beam search|Track multiple candidate sequences in parallel, keep the best-scoring ones|Higher quality output for tasks like translation where global sentence quality matters more than per-token diversity|Translation, some structured generation|—|
|Speculative decoding|A small "draft" model proposes several tokens ahead; the large model verifies them in one batched pass|Sequential generation is slow; this parallelizes verification|Production inference serving (latency optimization)|—|
|SSD (Speculative Speculative Decoding)|Pre-builds speculative continuations for all likely verifier outcomes ahead of time|Maximizes overlap between drafting and verification for max throughput|Cutting-edge inference serving (2026 research)|—|

---

## 7. System Placement

```
Transformer forward pass
   ↓
Logits (one score per vocabulary token)
   ↓
Sampling/decoding strategy (temperature, top-k, top-p, or greedy)
   ↓
Chosen next token
   ↓
Token appended to sequence, fed back in (autoregressive loop)
   ↓
Repeat until stop token / max length
   ↓
Detokenizer → final text response
```

Decoding is the bridge between "what the model computed" and "what actually gets generated" — it runs once per output token, every single generation step.

---

## 8. Internal Working

Trace generation of one token, step by step, with temperature=0.7 and top-p=0.9:

1. The Transformer's final layer produces logits — a vector of 50,000+ raw scores, one per vocabulary token.
2. Logits are divided by the temperature value (0.7): this sharpens the distribution slightly compared to temperature=1.0 (no scaling), since dividing by a number less than 1 increases the relative gap between high and low scores.
3. Softmax converts the scaled logits into a probability distribution that sums to 1.
4. Top-p filtering: tokens are sorted by probability descending; the algorithm keeps adding tokens to a candidate set until their cumulative probability crosses 0.9, then discards everything else (the rest of the long tail).
5. The probabilities of the remaining candidate set are renormalized to sum to 1 (since some mass was just discarded).
6. A random sample is drawn from this final, filtered distribution — this is the actual randomness step, typically using the model's pseudo-random number generator (which is why a fixed `seed` can make outputs reproducible).
7. The sampled token is appended to the sequence.
8. The KV-cache (see KV-cache note) is updated with this new token's Key/Value vectors, so the next step doesn't need to recompute attention for everything that came before.
9. This entire process — one full or partial forward pass plus a sampling step — repeats for every single output token until a stop condition (max tokens, stop sequence, or end-of-text token) is hit.

---

## 9. Core Components

**Temperature scaling**

- Purpose: control overall randomness/creativity of output.
- Input: raw logits, a temperature value (commonly 0-2).
- Output: scaled logits.
- Internal logic: `scaled_logit = logit / temperature`.
- Failure case: temperature=0 causes division issues in some implementations (usually handled as a special case equal to greedy decoding); very high temperature (>1.5) often produces incoherent output.

**Top-k filtering**

- Purpose: hard-cap the candidate pool size.
- Input: probability distribution, integer k.
- Output: filtered distribution over only the top k tokens.
- Internal logic: sort, keep top k, zero out the rest, renormalize.
- Failure case: a fixed k can be too small when the model is genuinely uncertain (excludes reasonable options) or too large when the model is very confident (includes irrelevant low-probability tokens).

**Top-p (nucleus) filtering**

- Purpose: adaptive candidate pool size based on actual model confidence.
- Input: probability distribution, threshold p.
- Output: filtered distribution over the smallest set crossing cumulative probability p.
- Internal logic: sort descending, accumulate until threshold crossed, renormalize remaining set.
- Failure case: at very flat distributions (model is very unsure), top-p can still include a large, noisy candidate set.

**Speculative decoding engine**

- Purpose: speed up sequential generation without changing output distribution.
- Input: a small/fast draft model, the large target model, current sequence.
- Output: multiple verified tokens per "round" instead of one.
- Internal logic: draft model proposes N tokens; target model runs one batched forward pass scoring all N positions at once; accepts the longest prefix matching what the target model would have chosen anyway, rejects/resamples from the first mismatch onward.
- Failure case: if the draft model's guesses are frequently wrong, you gain little speedup (you still need the target model's full verification pass) and add complexity for marginal benefit.

---

## 10. Practical Usage

### Installation

```bash
pip install transformers torch --break-system-packages
```

### Imports

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
```

### Basic Example

```python
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

inputs = tokenizer("The weather today is", return_tensors="pt")
outputs = model.generate(
    **inputs,
    max_new_tokens=20,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
)
print(tokenizer.decode(outputs[0]))
```

`do_sample=True` switches from greedy to sampling-based decoding; `temperature` and `top_p` shape the randomness as described in Section 8.

### Real Example (comparing greedy vs sampled output for the same prompt)

```python
greedy_out = model.generate(**inputs, max_new_tokens=20, do_sample=False)
sampled_out = model.generate(**inputs, max_new_tokens=20, do_sample=True, temperature=1.0, top_p=0.95)
print("Greedy:", tokenizer.decode(greedy_out[0]))
print("Sampled:", tokenizer.decode(sampled_out[0]))
```

Running this a few times shows greedy always produces the identical output, while sampled output varies each run — directly demonstrating where the randomness in chat responses actually comes from.

### Common Libraries

- HuggingFace `transformers` (`generate()` method exposes all sampling params)
- `vllm` (production serving, also supports speculative decoding configs)

### Common APIs

- OpenAI/Anthropic/Google chat APIs: `temperature`, `top_p` (most don't expose raw `top_k` at the API level, keeping it simpler for end users)

### Configuration Options

- `temperature` (0 = deterministic-ish, higher = more random)
- `top_p` (nucleus threshold, commonly 0.9-0.95)
- `top_k` (fixed candidate count, less commonly exposed at API level than top_p)
- `stop` / stop sequences (forces decoding to halt on certain strings)

### Expected Output

Text that varies run-to-run (with sampling) or is perfectly deterministic (greedy / temperature=0), demonstrating the direct, controllable link between these parameters and output behavior.

---

## 11. Production Usage

OpenAI and Anthropic both default their chat APIs to temperature + top-p sampling rather than greedy decoding, because greedy decoding's repetitive failure mode is a poor user experience for general chat. On the infrastructure side, speculative decoding (originally pushed by Microsoft and OpenAI research) is now a standard latency optimization in production inference engines, delivering roughly 2-3x faster generation without altering what the model would have output anyway — important because it's a "free" speedup in the sense that it doesn't trade off quality for speed, only adds engineering complexity (you need a compatible smaller draft model). Newer research (Speculative Speculative Decoding, March 2026) pushes this further by overlapping the drafting and verification stages more completely, aiming to maximize GPU utilization during decoding specifically — the stage that's historically been memory-bandwidth-bound rather than compute-bound.

---

## 12. Design Decisions

**Why not always use greedy decoding?** It's deterministic and simple, but it has no mechanism to escape repetitive loops, and it discards the model's genuine uncertainty — when the model is 49% confident between two very different good answers, greedy arbitrarily commits to one every single time with no variation.

**Why top-p over top-k?** Top-k uses a fixed candidate pool size regardless of how confident the model is at that step. Top-p adapts: when the model is very confident (probability mass concentrated in 1-2 tokens), the candidate pool shrinks naturally; when it's uncertain (mass spread across many tokens), the pool grows. This generally produces more natural-feeling variability than a fixed k.

**Why does speculative decoding work without hurting quality?** Because the large model still makes the final call on every single token — the draft model's guesses are only ever a shortcut for what the large model would have generated anyway; any mismatch is detected and corrected by the verification step, not silently allowed through.

---

## 13. Tradeoff Matrix

|Decision|Speed|Cost|Accuracy/Quality|Complexity|Determinism|
|---|---|---|---|---|---|
|Greedy|Baseline|Baseline|Lower (repetitive)|Lowest|Fully deterministic|
|Temperature 0.7 + top-p 0.9|Baseline|Baseline|Good general-purpose balance|Low|Non-deterministic (unless seeded)|
|High temperature (1.2+)|Baseline|Baseline|More creative, more hallucination risk|Low|Non-deterministic|
|Beam search|Slower (k× model runs)|Higher|Higher quality for some tasks (translation)|Medium|Deterministic given fixed beam|
|Speculative decoding|2-3x faster|Lower (less wall-clock GPU time)|Identical to target model|High (needs draft model)|Same as underlying sampling method|

---

## 14. Cost Impact

Sampling parameters themselves (temperature, top-p, top-k) don't change compute cost — they're cheap post-processing on top of logits that were already computed. Speculative decoding, however, directly reduces cost and latency by getting more output tokens per unit of large-model compute time, which matters a lot for any latency-sensitive or high-volume production application — fewer GPU-seconds per response at the same throughput. Beam search, by contrast, increases cost because it requires running multiple candidate sequences through the model simultaneously rather than just one.

---

## 15. Failure Modes

**Technical Failure: Repetition loops**

- Cause: greedy decoding (or very low temperature) with no mechanism to break ties or escape local optima.
- Symptoms: the model repeats the same phrase or sentence structure verbatim.
- Fix: raise temperature slightly, use top-p/top-k sampling instead of pure greedy, or add a repetition penalty if the API/library supports it.

**Quality Failure: Incoherent output at high temperature**

- Cause: temperature set too high, flattening the distribution enough that genuinely poor tokens get picked with meaningful probability.
- Symptoms: grammatically broken or nonsensical text, increased hallucination.
- Fix: lower temperature, or tighten top-p/top-k to limit how far into the long tail sampling can reach even at high temperature.

**Operational Failure: Non-reproducible outputs in testing**

- Cause: sampling is inherently random when temperature > 0 and no seed is fixed.
- Symptoms: automated tests that expect deterministic output fail intermittently.
- Fix: set temperature to 0 (or use a fixed seed if the API supports it) for tests; reserve sampling-based randomness for actual user-facing generation.

**Production Failure: Speculative decoding gains evaporate**

- Cause: draft model's predictions rarely match the target model's actual choices (poor draft model quality or domain mismatch).
- Symptoms: little to no latency improvement despite the added complexity of running speculative decoding infrastructure.
- Fix: choose/tune a draft model with output distributions genuinely close to the target model for your actual workload, not just a generically smaller model.

---

## 16. Optimization Techniques

- Tune `temperature` and `top_p` per task type: low temperature for code/factual tasks, higher for creative tasks.
- Use speculative decoding in production serving for latency-sensitive applications — it's close to a "free" speedup.
- Use a fixed seed (where supported) for any test or evaluation pipeline that needs reproducibility.
- Consider adaptive sampling that adjusts parameters dynamically based on task complexity, rather than one fixed setting for an entire application.

---

## 17. Interview Preparation

### Beginner Questions

**Q: What's the difference between temperature and top-p?** A: Temperature reshapes the entire probability distribution before sampling (sharper or flatter). Top-p then filters that distribution down to the smallest set of top tokens whose cumulative probability crosses a threshold, excluding the long tail of unlikely tokens entirely. They're applied in sequence, not as alternatives to each other.

### Intermediate Questions

**Q: Why does greedy decoding tend to produce repetitive text?** A: Greedy always picks the single highest-probability token, with no randomness to break out of a state where the highest-probability continuation is itself a repeated phrase — once that pattern starts, it can reinforce itself with no escape mechanism.

### Advanced Questions

**Q: How does speculative decoding speed up generation without changing the output distribution?** A: A smaller draft model proposes several tokens ahead cheaply. The large target model then verifies all of those proposed tokens in a single batched forward pass (which is much more GPU-efficient than one-token-at-a-time generation). Any token the draft model got "wrong" (meaning the target model wouldn't have generated it) is rejected and resampled correctly from that point onward — so the final output always reflects exactly what the target model would have produced on its own, just generated faster because correct guesses let you skip ahead multiple tokens per verification pass.

---

## 18. Common Mistakes

**Mistake**: assuming higher temperature always means "better" or "more human-like" output. _Why it happens_: "more random" sounds like "more creative" in a positive sense. _Correct understanding_: past a certain point, higher temperature just means more incoherence and hallucination — it's a tradeoff knob, not a quality dial.

**Mistake**: thinking speculative decoding changes what the model "says." _Why it happens_: it sounds like an approximation technique. _Correct understanding_: it's purely a speed optimization — the target model still verifies and has final say on every token, so output quality/distribution is unchanged, only generation speed improves.

---

## 19. Current Industry State

Temperature + top-p sampling remains the production default across OpenAI, Anthropic, Google, and Meta's chat-facing APIs as of mid-2026. On the serving infrastructure side, speculative decoding has moved from research idea to standard production technique for latency optimization, and newer approaches like Speculative Speculative Decoding (introduced March 2026) are pushing further into maximizing decode-stage GPU utilization, an area that's historically been memory-bandwidth-bound rather than compute-bound during the token-by-token generation phase.

---

## 20. Current Problems & Research

The core unsolved tension is still quality-vs-creativity: there's no single "correct" temperature or top-p setting — it's task-dependent and currently mostly hand-tuned rather than automatically optimized. Adaptive sampling research (2025) is exploring dynamically adjusting sampling parameters based on input complexity in real time, but this isn't yet a mainstream production default. On the speed side, the open research direction is squeezing more overlap between drafting and verification (SSD-style approaches) to push decode-stage throughput further, since sequential token generation remains one of the few parts of the LLM pipeline that resists straightforward parallelization.

---

## 21. Future Evolution

Expect sampling parameter selection to become more automated — auto-tuned per task or even per request, rather than a developer manually picking one `temperature` value for an entire application. On the speed front, speculative decoding and its successors (SSD and whatever follows) are likely to keep becoming standard infrastructure rather than an optional optimization, since the underlying sequential-generation bottleneck isn't going away as long as autoregressive decoding remains the dominant generation paradigm.

---

## 22. Engineer Checklist

[ ] Explain logits, softmax, and how a probability distribution becomes a chosen token [ ] Explain temperature, top-k, and top-p, and how they interact [ ] Explain why greedy decoding produces repetitive output [ ] Use `generate()` parameters to control output randomness in code [ ] Explain speculative decoding and why it doesn't change output quality [ ] Discuss when to use low vs. high temperature for different task types [ ] Recognize non-determinism as expected behavior (and know how to control it for testing)

---

## 23. Knowledge Graph

```
Sampling & Decoding
├── Quality/diversity tradeoff
│   ├── Greedy decoding
│   ├── Temperature scaling
│   ├── Top-k sampling
│   ├── Top-p (nucleus) sampling
│   └── Beam search
└── Speed optimization (separate concern)
    ├── Speculative decoding
    └── Speculative Speculative Decoding (SSD)
```

---

## 24. If You Remember Only 10 Things

1. The model outputs logits (raw scores), not text — decoding is the separate step that turns those into an actual chosen token.
2. Greedy decoding always picks the top token; it's deterministic but prone to repetitive loops.
3. Temperature scales the distribution before softmax — lower = more focused, higher = more random/creative.
4. Top-k caps the candidate pool to a fixed size; top-p adapts the pool size to the model's actual confidence at that step.
5. Top-p is generally preferred over top-k because it adjusts dynamically rather than using one fixed cutoff.
6. Sampling randomness is why the same prompt can produce different outputs each run (and why a seed gives reproducibility).
7. Speculative decoding speeds up generation 2-3x by having a small draft model guess ahead and the big model verify in batches.
8. Speculative decoding doesn't change output quality — the target model always has final say on every token.
9. There's no single "correct" sampling setting — low temperature suits code/facts, higher suits creative tasks.
10. Sequential token generation is one of the few LLM pipeline stages that resists easy parallelization, which is exactly why speculative decoding research matters so much for latency.