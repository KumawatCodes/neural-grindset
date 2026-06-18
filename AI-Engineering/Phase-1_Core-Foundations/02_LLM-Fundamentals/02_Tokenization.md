---
title: "Tokenization"
phase: "Phase-1 — Core AI Foundations"
group: "02_LLM-Fundamentals"
tags: [ai-engineering, phase-1, study-notes]
status: empty
created: 2026-06-07
---
# Tokenization

## 1. Executive Summary

Tokenization is the step that turns your text into the numbers a model actually computes on. Before any attention, any FFN, any sampling — your prompt gets chopped into chunks called tokens, and each chunk is mapped to an integer ID. Every cost you pay (API pricing), every context limit you hit, and a lot of weird model behavior (struggling with "strawberry has how many r's") trace back to tokenization decisions made before the model ever sees your text.

You'll run into this directly when you're estimating API costs, hitting context window limits, or debugging why a model mishandles code, typos, or non-English text.

### 30-Second Interview Answer

"Tokenization converts raw text into a sequence of integer IDs the model can process, usually using subword units via Byte Pair Encoding (BPE). It's a balance between vocabulary size and sequence length — a bigger vocabulary means fewer tokens per sentence but a bigger embedding table; a smaller vocabulary means the opposite. Almost every frontier model uses some BPE variant, though byte-level tokenizers like Meta's Byte Latent Transformer are starting to challenge that for handling code and typos better."

### 2-Minute Interview Answer

"Models can't operate on raw characters efficiently (too many tokens, no semantic grouping) or raw words (vocabulary explodes — every typo, conjugation, or rare word needs its own slot, and you still can't handle words you've never seen). Subword tokenization, mainly BPE, splits text into frequently-occurring chunks: common words become a single token, rare words get split into recognizable pieces. This is learned from a training corpus by repeatedly merging the most frequent adjacent byte/character pairs until you hit a target vocabulary size, usually 50K-100K tokens.

This works well for English prose but has known weak points: it handles low-resource languages poorly (less training data means worse merges), it breaks character-level reasoning (a model literally can't 'see' individual letters in 'strawberry' if it's one or two tokens), and it's brittle around typos and code syntax. That's driving recent research into byte-level approaches — Meta's Byte Latent Transformer groups raw bytes into dynamic patches instead of using a fixed vocabulary, handling typos and code more gracefully at the cost of longer sequences. As of 2026 this hasn't displaced BPE/SentencePiece in any frontier production model, but it's the most credible near-term challenger."

---

## 2. The Real Engineering Problem

Imagine training a model on raw Unicode characters. "Tokenization" itself in English is 12 characters — meaning a model would need to track relationships across 12 separate steps just to process one word, before even getting to the next word in the sentence. Multiply that across a 2000-word document and your sequence length explodes into the tens of thousands of characters, hammering directly into the O(n²) attention cost problem (see Transformer note).

Now imagine the opposite: treat every whole word as one unit. You get a vocabulary that needs an entry for every word, every conjugation, every typo, every brand name, every made-up word a user might type. This vocabulary becomes unmanageably large, and any word the model hasn't seen during training becomes an unrecognized "UNK" token, with no fallback.

Engineers needed a middle ground: chunks frequent enough to keep sequences short, but flexible enough to represent words never seen during training by falling back to smaller, recognizable pieces.

---

## 3. Why This Exists

Subword tokenization (BPE) exists to balance compression (fewer tokens per sentence = cheaper, faster) against generalization (handling rare or unseen words gracefully). It became the industry default because it's the simplest approach that solves both problems reasonably well, and it's fast, deterministic, and well-tooled (HuggingFace Tokenizers, SentencePiece).

If tokenization disappeared and models had to process raw bytes directly with standard attention, sequence lengths would balloon 4-5x, and the O(n²) attention cost would make training and inference far more expensive for the same effective context — this is exactly the cost byte-level approaches like MambaByte and BLT have to engineer around using non-quadratic architectures.

---

## 4. Mental Model

Think of BPE like building a phrasebook by observation. Start with every individual character as its own "word" in your phrasebook. Read a huge amount of text, and notice that certain pairs of characters show up together constantly — "t" and "h" appear together so often that you merge them into "th." Then "th" and "e" merge into "the," because that's common too. Keep doing this — merge the most frequent adjacent pair, over and over — until your phrasebook has, say, 100,000 entries. Common words ("the," "is," "and") become single entries early. Rare words stay split into smaller, more primitive pieces.

### How To Visualize It

```
Raw text: "tokenization is hard"

Character level:  t-o-k-e-n-i-z-a-t-i-o-n- -i-s- -h-a-r-d   (20 tokens)

BPE (subword) level:  [token][ization] [is] [hard]            (4 tokens)
                       ↑ common prefix    ↑ whole word kept
                          recognized          since frequent

Word level:  [tokenization] [is] [hard]                       (3 tokens, but
                                                                "tokenization"
                                                                only works if
                                                                it was seen
                                                                during training)
```

BPE sits in the sweet spot: nearly as compact as word-level, but degrades gracefully (splits into smaller known pieces) instead of failing entirely on unseen words.

---

## 5. Engineering Evolution

```
Problem: Models need numeric input; raw characters are too long, raw words don't generalize
↓
Old Solution: Word-level tokenization with a fixed vocabulary
↓
Limitation: Unbounded vocabulary size, fails completely on unseen/rare words (UNK token)
↓
New Solution: Subword tokenization — BPE, WordPiece, SentencePiece/Unigram
↓
Current Best Practice: Custom BPE-family tokenizers (50K-100K vocab) per frontier model, with token-counting utilities exposed in APIs
↓
Current Limitation: Poor on low-resource languages, brittle on typos/code, can't do character-level reasoning
↓
Future Direction: Byte-level tokenization (Byte Latent Transformer, MambaByte) — still experimental at frontier scale
```

---

## 6. Vocabulary Map

|Term|Meaning|Why It Exists|Where Used|Aliases|
|---|---|---|---|---|
|Token|A chunk of text (word, subword, or character) mapped to an integer ID|The atomic unit models actually compute on|Every step of the pipeline|—|
|Vocabulary size|Total number of unique tokens a tokenizer can produce|Tradeoff knob between sequence length and embedding table size|Tokenizer config|Vocab|
|BPE (Byte Pair Encoding)|Merge the most frequent adjacent byte/character pairs repeatedly to build a vocabulary|Balances compression with generalization to unseen words|GPT, Llama, most frontier models|—|
|WordPiece|Similar to BPE but selects merges by likelihood improvement, not raw frequency|Slightly different optimization target, used historically by BERT-family models|BERT, some Google models|—|
|SentencePiece / Unigram|Tokenizer framework that can operate directly on raw text (no pre-tokenization by whitespace), good for multilingual text|Handles languages without clear word boundaries (e.g. Japanese) better than word-based pre-splitting|Gemini, multilingual models|Unigram LM tokenizer|
|Unknown token (UNK)|Fallback token for input the tokenizer can't represent|Needed when word-level vocab encounters something unseen|Older word-level tokenizers|OOV (out-of-vocabulary)|
|Byte Latent Transformer (BLT)|Groups raw bytes into variable-length patches instead of a fixed vocabulary|Handles typos, code, and low-resource languages without a fixed vocab's failure modes|Meta research (2024-2025), not yet frontier-production|BLT|
|Token density|Number of tokens needed per character/word for a given text|Determines real-world cost and effective context usage|Pricing, context budgeting|Tokens-per-word|

---

## 7. System Placement

```
Raw user text
   ↓
Tokenizer (BPE/SentencePiece) → sequence of token IDs
   ↓
Embedding layer → sequence of vectors
   ↓
Transformer stack (attention + FFN)
   ↓
Output logits over vocabulary
   ↓
Sampling picks next token ID
   ↓
Detokenizer converts token IDs back to text
   ↓
Response shown to user
```

Tokenization is the very first and very last step of the pipeline — it's the translation layer between human text and the model's numeric world.

---

## 8. Internal Working

Trace the string `"unbelievable"` through a trained BPE tokenizer:

1. Start with the raw bytes/characters: `u-n-b-e-l-i-e-v-a-b-l-e`.
2. The tokenizer has a pre-built merge table (learned during training) — it checks which adjacent pairs in this word match known merges, in priority order.
3. Suppose `"un"` is a known merge (common prefix) — characters `u` and `n` combine into one token `un`.
4. Suppose `"able"` is a known whole-token merge — `a-b-l-e` combines into `able`.
5. The remaining middle, `believ`, might further merge into recognizable chunks like `believ` if that's frequent enough in training data, or stay split as `bel-iev` if not.
6. Final tokenization might look like: `["un", "believ", "able"]` — 3 tokens for a 12-character word.
7. Each of these subword strings maps to a fixed integer ID via a lookup table (the vocabulary), e.g. `["un" → 403, "believ" → 19234, "able" → 1820]`.
8. These integer IDs are what actually get embedded and fed into the Transformer — the model never sees the string "unbelievable" at all, only `[403, 19234, 1820]`.

This is also why models sometimes fail at character-level tasks: if "strawberry" is tokenized as `["straw", "berry"]`, the model has no direct access to the individual letters "s-t-r-a-w-b-e-r-r-y" to count them — it only ever saw two opaque chunks.

---

## 9. Core Components

**Pre-tokenizer**

- Purpose: initial rough splitting (e.g., on whitespace/punctuation) before subword merging.
- Input: raw text.
- Output: a list of "words" or pre-chunks.
- Internal logic: regex-based rules (handles things like contractions, punctuation).
- Failure case: languages without whitespace word boundaries (Chinese, Japanese) need special handling — naive whitespace splitting fails outright.

**Merge table / vocabulary**

- Purpose: the learned mapping from frequent byte/character sequences to token IDs.
- Input: pre-tokenized chunks.
- Output: final token sequence.
- Internal logic: greedy application of learned merges, in priority order (most-frequent-first, learned during training).
- Failure case: domain mismatch — a tokenizer trained mostly on English/code will tokenize, say, Hindi or Swahili text far less efficiently (more tokens per word), directly increasing cost for those languages.

**Detokenizer**

- Purpose: convert generated token IDs back into readable text.
- Input: sequence of token IDs.
- Output: text string.
- Internal logic: reverse lookup + careful handling of spacing/byte-fallback for unusual characters.
- Failure case: streaming generation can produce a partial multi-byte character (e.g., mid-emoji) that needs buffering before it can be safely decoded into valid text.

---

## 10. Practical Usage

### Installation

```bash
pip install tiktoken transformers --break-system-packages
```

### Imports

```python
import tiktoken
from transformers import AutoTokenizer
```

### Basic Example

```python
enc = tiktoken.get_encoding("cl100k_base")  # used by GPT-4-class models
tokens = enc.encode("Tokenization is the first step.")
print(tokens)
print(len(tokens), "tokens")
print(enc.decode(tokens))
```

`encode` converts text to integer token IDs; `decode` reverses it. `len(tokens)` is exactly what your API bill is based on for that input.

### Real Example (estimating cost before calling an API)

```python
prompt = open("my_codebase_review_prompt.txt").read()
token_count = len(enc.encode(prompt))
estimated_cost = (token_count / 1_000_000) * 3.00  # e.g. $3 per 1M input tokens
print(f"{token_count} tokens, ~${estimated_cost:.4f} input cost")
```

This is the exact check worth running before sending a large prompt (e.g., a full repo) to an API — token count, not character count, is what determines cost and whether you'll hit a context limit.

### Common Libraries

- `tiktoken` (OpenAI's fast BPE tokenizer)
- HuggingFace `tokenizers` / `transformers` (most other models)
- `sentencepiece` (Google's library, used by Gemini and many multilingual models)

### Common APIs

- OpenAI/Anthropic/Google all expose token counting either via local tokenizer libraries or as a first-class API utility (token-counting endpoints are now standard as of 2026).

### Configuration Options

- Vocabulary size (set at tokenizer training time, not at inference time — you can't change this per-request)
- Special tokens (e.g., `<|endoftext|>`, `<|im_start|>`) reserved for structural markers like chat turns

### Expected Output

A list of integers (token IDs) and, in reverse, the original text. The integer count is the unit every cost and context-limit conversation revolves around.

---

## 11. Production Usage

OpenAI, Anthropic, and Meta all maintain proprietary BPE-family tokenizers tuned to their own training data — not generic HuggingFace defaults. Google leans on SentencePiece/Unigram, partly because it handles non-whitespace-delimited languages (Japanese, Chinese) more gracefully without a separate pre-tokenization step. As of June 2026, OpenAI's newer developer tooling treats token counting as a first-class API feature rather than something developers have to compute locally, reflecting how central token budgeting has become to production cost control.

At scale, providers also cache tokenized system prompts — since your system prompt is usually identical across many requests, tokenizing it repeatedly would be wasted work; this ties directly into prefix caching covered in the KV-cache note.

---

## 12. Design Decisions

**Why BPE over word-level?** Word-level vocabularies are unbounded (every typo or rare word needs a slot) and fail hard on anything unseen. BPE degrades gracefully — worst case, it falls back to character-level splitting for truly novel strings, never producing a hard UNK failure.

**Why not character-level by default?** It avoids the vocabulary problem entirely but multiplies sequence length 4-5x, which directly multiplies attention's O(n²) cost and inference latency. The compression BPE gives you is the entire reason it's still preferred over pure character/byte tokenization in frontier production models.

**Why is vocabulary size usually 50K-100K, not larger?** A larger vocabulary means fewer tokens per sentence (cheaper, faster generation) but a much bigger embedding table (more parameters, more memory) and diminishing returns — most common subwords are already captured by ~100K.

---

## 13. Tradeoff Matrix

|Decision|Speed|Cost|Memory|Complexity|Scalability|
|---|---|---|---|---|---|
|Larger vocab (100K+)|Faster generation (fewer tokens)|Lower (fewer tokens billed)|Higher embedding table|Low|Lower (huge embedding layer)|
|Smaller vocab (30K)|Slower (more tokens)|Higher (more tokens billed)|Lower embedding table|Low|Higher|
|Byte-level (BLT/MambaByte)|Slower (5x longer sequences)|Higher (more tokens, unless paired with non-quadratic architecture)|Lower (no big vocab table)|High|Better generalization, worse raw throughput|
|Adaptive/domain tokenizer|Variable|Lower for that domain|Variable|High (multiple tokenizers to manage)|Good within domain, poor outside it|

---

## 14. Cost Impact

Token count is the literal unit of API pricing — every input and output token costs money, so tokenization efficiency for your specific content directly determines your bill. A prompt heavy in a language the tokenizer wasn't optimized for (e.g., Hindi, for many English-centric tokenizers) can use 2-3x more tokens than the equivalent English text for the same meaning, silently inflating costs for non-English users. Code is another case where naive tokenizers underperform — special characters and indentation can fragment into more tokens than expected, which matters directly for something like reviewing a large codebase through an LLM API (relevant to your CodeSentinel-style projects). Compute and memory cost scale with token count too, since longer token sequences mean longer attention computation and a bigger KV-cache to maintain.

---

## 15. Failure Modes

**Technical Failure: Character-level task failure**

- Cause: subword tokenization hides individual characters inside opaque multi-character tokens.
- Symptoms: model fails simple tasks like counting letters in a word, or reversing a string.
- Fix: explicitly ask the model to space out characters first, or use a tool/code execution step instead of relying on raw model reasoning.

**Scaling Failure: Non-English token inflation**

- Cause: tokenizer's merge table was learned mostly from English/code-heavy training data.
- Symptoms: same meaning costs significantly more tokens (and money) in other languages.
- Fix: budget API costs per-language explicitly if you have multilingual users; consider models with tokenizers specifically tuned for your target languages.

**Operational Failure: Streaming decode of partial tokens**

- Cause: a generated token can represent a partial multi-byte UTF-8 character.
- Symptoms: garbled or broken characters appearing mid-stream in a chat UI.
- Fix: buffer partial bytes until a complete character can be decoded before rendering to the user.

**Production Failure: Silent context overflow**

- Cause: developers estimate context budget by character count or word count instead of actual token count.
- Symptoms: requests unexpectedly truncated or rejected once token count (not character count) crosses the model's limit.
- Fix: always count tokens with the actual tokenizer library for your target model before sending a request.

---

## 16. Optimization Techniques

- Use the actual tokenizer (`tiktoken`, model-specific) to count tokens before sending requests, not approximations.
- Cache tokenized system prompts/prefixes where the API supports it (ties to prompt caching).
- For multilingual or code-heavy workloads, benchmark token density across your real content before committing to a model/tokenizer — don't assume English-token-count intuitions carry over.
- For repeated structured inputs (e.g., JSON schemas, fixed instructions), keep them stable and front-loaded so caching mechanisms recognize and reuse them.

---

## 17. Interview Preparation

### Beginner Questions

**Q: What is a token, and why isn't it just "a word"?** A: A token is the atomic unit a model processes — usually a subword chunk produced by an algorithm like BPE, not necessarily a whole word. Common words are often a single token; rare or long words get split into smaller recognizable pieces.

### Intermediate Questions

**Q: Why do most LLM providers use BPE instead of word-level tokenization?** A: Word-level vocabularies are unbounded and fail completely on unseen words (UNK tokens). BPE degrades gracefully by falling back to smaller subword units, while still compressing common words into single tokens for efficiency.

### Advanced Questions

**Q: Why might byte-level tokenization (e.g., Byte Latent Transformer) become more relevant going forward?** A: It removes the fixed-vocabulary failure modes entirely — no UNK tokens, no domain mismatch, much better handling of typos, code, and low-resource languages — at the cost of significantly longer sequences (and therefore higher compute) unless paired with an architecture that doesn't scale quadratically with length, which is part of why it's still experimental rather than frontier-production-default as of 2026.

---

## 18. Common Mistakes

**Mistake**: estimating token count from word or character count using rough multipliers ("1 word ≈ 1.3 tokens"). _Why it happens_: it's a reasonable approximation for plain English text. _Correct understanding_: this breaks down for code, non-English languages, and unusual formatting — always use the actual tokenizer for cost-sensitive or context-limit-sensitive work.

**Mistake**: assuming the model "sees" individual letters in a word. _Why it happens_: humans read letter by letter, so it's intuitive to assume models do too. _Correct understanding_: the model only sees whatever opaque subword tokens the tokenizer produced — letter-level reasoning requires the letters to actually appear as separate tokens, which they usually don't.

---

## 19. Current Industry State

BPE and SentencePiece/Unigram remain the production standard across OpenAI, Anthropic, Google, and Meta as of mid-2026, each running custom-trained vocabularies rather than off-the-shelf defaults. Byte-level approaches are moving from a fringe research idea toward something production teams are actually considering for 2026. Token counting has become a first-class, built-in API feature rather than something developers compute by hand, reflecting how central it's become to cost control and context management at scale.

---

## 20. Current Problems & Research

The unresolved issues are consistent: BPE-family tokenizers underperform on low-resource languages because their merge tables are learned from whatever training data was available (which skews heavily English/code), they handle typos and code syntax poorly because a single inserted character can completely change how a word gets split, and the embedding-layer-size-vs-sequence-length tradeoff has no clean solution — you're always picking a point on that curve. Meta's Byte Latent Transformer and MambaByte are the leading research directions tackling this by removing the fixed vocabulary entirely; the tradeoff is materially longer sequences, which is why neither has displaced BPE in a frontier production model yet.

---

## 21. Future Evolution

The most plausible near-term shift is hybrid tokenization — keeping BPE-style efficiency for natural-language prose while routing code, rare tokens, or non-Latin scripts through byte-level or adaptive handling. A full frontier-model release built on a pure byte-level path is plausible within the next development cycle but hasn't happened yet; expect incremental hybrid adoption before a full architectural switch.

---

## 22. Engineer Checklist

[ ] Explain why BPE exists and what problem word-level tokenization couldn't solve [ ] Trace a word through the merge process by hand [ ] Use `tiktoken` or a model's tokenizer to count tokens before sending a request [ ] Explain why non-English text often costs more tokens for the same meaning [ ] Explain why models struggle with character-level tasks [ ] Discuss byte-level tokenization as the emerging alternative and its tradeoffs [ ] Connect token count directly to API cost and context window limits

---

## 23. Knowledge Graph

```
Tokenization
├── Word-level (historical, obsolete for open-vocabulary needs)
├── Character-level (simple, but too long for production)
├── Subword (current standard)
│   ├── BPE
│   ├── WordPiece
│   └── SentencePiece / Unigram
├── Byte-level (emerging)
│   ├── Byte Latent Transformer (BLT)
│   └── MambaByte
└── Downstream impact
    ├── Pricing (tokens = billing unit)
    ├── Context window (tokens = the limit unit)
    └── KV-cache size (scales with token count)
```

---

## 24. If You Remember Only 10 Things

1. Tokenization converts text into integer IDs — it's the translation layer between your prompt and the model's math.
2. BPE builds its vocabulary by repeatedly merging the most frequent adjacent character/byte pairs in training data.
3. Common words become single tokens; rare words get split into smaller, more primitive pieces.
4. Vocabulary size is a tradeoff: bigger vocab = fewer tokens per sentence but a bigger embedding table.
5. Tokens, not words or characters, are the actual billing and context-limit unit — always count with the real tokenizer.
6. Non-English and code-heavy text often costs more tokens for the same meaning, due to training-data skew.
7. Models can fail character-level tasks (like counting letters) because individual letters are often hidden inside opaque multi-character tokens.
8. Byte-level tokenization (BLT, MambaByte) removes the fixed-vocabulary failure modes but multiplies sequence length.
9. Frontier providers run custom, proprietary tokenizers — not generic open-source defaults.
10. Token counting is now a first-class production feature because it drives cost, context limits, and caching behavior.