---
title: "Context Windows"
phase: "Phase-1 — Core AI Foundations"
group: "02_LLM-Fundamentals"
tags: [ai-engineering, phase-1, study-notes]
status: empty
created: 2026-06-07
---
# Context Windows

## 1. Executive Summary

The context window is the maximum number of tokens a model can "see" at once — your system prompt, conversation history, retrieved documents, and the response it's generating, all combined. It's the single number that decides whether your use case ("review this whole codebase," "summarize this 200-page PDF") is even possible in one call, and it's the thing most directly responsible for cost and latency surprises.

You'll hit this constantly: building RAG pipelines, deciding whether to chunk a document or just paste it whole, debugging why a model "forgot" something you told it 50 messages ago, or explaining to a teammate why a 1M-token context window doesn't mean the model is reliably good across all 1M tokens.

### 30-Second Interview Answer

"The context window is the max tokens a model can process in a single request — input plus output combined. Bigger isn't free: cost and latency scale up sharply with length, and models reliably show worse retrieval for information buried in the middle of a long context, a pattern called 'lost in the middle.' Production systems treat context windows as a budget to manage carefully (via RAG, summarization, caching) rather than a number to maximize by default."

### 2-Minute Interview Answer

"Context window size is bounded by two things: the model's training (it was only trained to handle sequences up to some length reliably) and the quadratic cost of attention, which makes very long contexts expensive and slow regardless of whether the model is technically capable of processing them. As of 2026, baseline production context windows sit around 128K-200K tokens, with some models pushing to 1M-10M for specialized use cases like whole-codebase or whole-video processing.

The practical catch is that advertised context length and effective context length aren't the same thing — models commonly degrade well before the limit, and there's a well-documented 'lost in the middle' effect where information at the very start or very end of a long prompt is retrieved more reliably than information buried in the middle. This is why production systems don't just dump everything into one giant prompt — they use multi-tier memory architectures: a small 'active' window of the most relevant recent context, plus an external searchable store (RAG, vector DB) for everything else, pulling in only what's needed per query. Context engineering — deciding what actually goes into the window, not just how big the window is — has become its own discipline, partly because a large share of real-world agent failures trace back to context drift and memory loss rather than the model itself being incapable."

---

## 2. The Real Engineering Problem

Imagine you're building an AI code review tool (your CodeSentinel project is a good real example) and a user wants a full review of a 40,000-line codebase. You could try to paste the entire codebase into a single prompt. Even with a 1M-token model, this is enormously expensive per request, slow, and — critically — the model's accuracy on details buried in the middle of that 40,000-line dump is measurably worse than on the files at the start or end of your prompt.

The naive fix — "just use the biggest context window model available" — doesn't actually solve the problem. It trades one failure mode (can't fit the input) for another (input fits, but the model unreliably attends to most of it, and you're paying for tokens that aren't even helping accuracy). Engineers needed a way to decide, deliberately, what content earns a place in the context window, rather than relying on raw window size to bail them out.

---

## 3. Why This Exists

Context windows exist because attention's O(n²) cost makes "just process everything" economically and computationally unworkable past a certain length — there has to be a hard cutoff somewhere, and that cutoff is set during training (the lengths the model was actually trained and validated on). The size of the window is a deliberate tradeoff providers make between capability (longer = more use cases unlocked) and serving cost (longer = exponentially more GPU memory and compute per request).

If context windows didn't exist as a concept — if models could attend losslessly to unlimited length at no cost — RAG, chunking, and most of context engineering as a discipline would be unnecessary. The entire field of "what do I put in the prompt" exists specifically because the window is finite and imperfect.

---

## 4. Mental Model

Think of the context window like your own short-term working memory during a long meeting. You can hold maybe the last 10-15 minutes of discussion vividly in your head, plus whatever's written on the whiteboard (your "system prompt," always visible). If someone references something said an hour ago, you don't actually re-derive it from memory perfectly — you either remember it strongly because it was important, remember it weakly and might get it wrong, or you've genuinely lost it and need someone to remind you (the "retrieval" step in RAG).

A 1M-token context window is like extending that meeting to a week long, with a full transcript available — technically all there, but you will reliably do worse recalling something said on day 3 versus something said in the last five minutes or written on the whiteboard. Bigger window ≠ uniformly good recall across the whole window.

### How To Visualize It

```
Context Window (128K tokens example)

┌──────────────────────────────────────────────────────────────────────────┐
│ System Prompt │ Early Chat │ ... Middle Content ... │ Recent Turns │ Q │
└──────────────────────────────────────────────────────────────────────────┘

      ↑ Strong Recall                ↓ Weak Recall             ↑ Strong Recall
   (Beginning)                   (Lost in Middle)               (End)

                    U-Shaped Retrieval Accuracy
```

---

## 5. Engineering Evolution

```
Problem: Models can only attend to a finite, costly sequence length
↓
Old Solution: Small fixed windows (2K-8K tokens), manual truncation of history
↓
Limitation: Couldn't handle long documents, multi-turn conversations lost early context entirely
↓
New Solution: Larger windows via RoPE + FlashAttention (128K-1M+ tokens)
↓
Current Best Practice: Multi-tier memory — small active window + external retrieval (RAG) + caching, validated against real benchmarks (not just trusting advertised limits)
↓
Current Limitation: "Lost in the middle," geometric cost/latency growth, advertised ≠ effective length
↓
Future Direction: Test-Time Training (compress context into weights), better compression/summarization, hybrid memory architectures
```

---

## 6. Vocabulary Map

|Term|Meaning|Why It Exists|Where Used|Aliases|
|---|---|---|---|---|
|Context window|Max tokens a model can process in one request (input + output)|Hard limit set by training and attention cost|Every API call|Context length, max tokens|
|Lost in the Middle|Pattern where models retrieve info at the start/end of context better than the middle|An empirically observed Transformer weakness, not a bug to "fix" easily|Long-document QA, long conversations|U-shaped attention|
|Context rot|General term for systematic accuracy degradation as context length grows|Quantifies the gap between advertised and effective context|Benchmarking long-context models|Context degradation|
|Effective context length|The length at which a model actually performs reliably, vs. its advertised max|Advertised limits are often optimistic|Model evaluation, RULER benchmark|Usable context|
|Prompt/context caching|Reusing computed attention state for repeated prefixes across requests|Avoids re-processing identical content (e.g. system prompts) every call|OpenAI, Anthropic, Google APIs|KV-cache reuse (see KV-cache note)|
|RAG (Retrieval-Augmented Generation)|Fetch only relevant external content per query instead of stuffing everything into context|Keeps context window small, relevant, and cheap|Search-augmented chat, document QA|Retrieval augmentation|
|Context engineering|The discipline of deciding what content goes into the window and how it's structured|Bigger window ≠ better outcomes without deliberate curation|Production agent design|—|
|RULER benchmark|A comprehensive long-context evaluation suite (NVIDIA)|Simple "needle in haystack" tests were too easy and overstated real capability|Long-context model evaluation|—|
|MemGPT-style memory|Treating the LLM like an OS with paged/virtualized memory across tiers|Gives the illusion of unlimited memory via structured external storage|Long-running agents|LLM-as-OS|

---

## 7. System Placement

```
User query + conversation history + retrieved documents (if RAG) + system prompt
   ↓
                 [ all of this must fit inside the context window ]
   ↓
Tokenizer → token sequence
   ↓
Transformer (attention cost scales with this sequence length)
   ↓
Output tokens (also count against the window, for output-limited models)
   ↓
Response + updated conversation history for next turn
```

The context window is the budget constraint that everything upstream of the model (RAG retrieval, history management, system prompt design) has to respect.

---

## 8. Internal Working

Trace what happens when a chat application sends a 9th message in a long conversation, with a 32K context window model:

1. The application has stored the full conversation history (turns 1-8) plus the new user message.
2. Before calling the API, the app checks: does the system prompt + full history + new message fit within 32K tokens (using the actual tokenizer to count)?
3. If it fits: send everything as-is. The model attends across the entire history during generation, with weaker reliability for details buried in turns 2-5 versus turn 1 (system prompt) and turns 7-9 (recent, closest to generation point).
4. If it doesn't fit: the app must make a decision — truncate the oldest turns, summarize older turns into a condensed form, or retrieve only the most relevant past turns (treating history like a small RAG problem).
5. Whatever is sent becomes one token sequence, fed through the full Transformer stack (Section 8 of the Transformer note) in one pass for the prompt (the "prefill" stage), then token-by-token for the response (the "decode" stage, using KV-cache from the prefill).
6. The new response gets appended to history, and the cycle repeats for turn 10 — meaning the "how much fits" problem gets harder every single turn unless something is actively managed.

---

## 9. Core Components

**Prefill stage**

- Purpose: process the entire input prompt in one parallel pass, building the KV-cache.
- Input: full token sequence (system prompt + history + new message).
- Output: KV-cache populated for every input token; first output token generated.
- Internal logic: standard Transformer forward pass across the whole input at once.
- Failure case: very long prompts make prefill itself slow and memory-heavy, even before generation starts.

**Decode stage**

- Purpose: generate output tokens one at a time, using the cached attention state from prefill.
- Input: KV-cache + most recently generated token.
- Output: next token, repeated until stop condition.
- Internal logic: only needs to compute attention for the new token against the cache, not recompute everything.
- Failure case: KV-cache itself grows with context length, eventually becoming the memory bottleneck (covered in KV-cache note).

**Context management layer (application-side, not model-side)**

- Purpose: decide what actually goes into the window each turn.
- Input: full history, available documents, system instructions.
- Output: a curated token sequence within budget.
- Internal logic: truncation, summarization, retrieval, or priority-based inclusion (critical > high > medium > low priority content).
- Failure case: naive truncation can drop critical early instructions; naive summarization can lose specific details a later query needs.

---

## 10. Practical Usage

### Installation

```bash
pip install anthropic tiktoken --break-system-packages
```

### Imports

```python
import anthropic
import tiktoken
```

### Basic Example (checking budget before sending)

```python
enc = tiktoken.get_encoding("cl100k_base")
system_prompt = "You are a helpful code reviewer."
history = "...(prior conversation)..."
new_message = "Review this function for bugs."

full_input = system_prompt + history + new_message
token_count = len(enc.encode(full_input))
CONTEXT_LIMIT = 128_000

if token_count > CONTEXT_LIMIT * 0.9:
    print("Approaching context limit — consider summarizing history.")
```

This is the basic guardrail every production app needs: check actual token count against the model's window before sending, with headroom for the model's own output tokens.

### Real Example (sliding window with summarization)

```python
def manage_history(history, max_tokens=20_000):
    token_count = len(enc.encode(history))
    if token_count > max_tokens:
        old_part, recent_part = history[:len(history)//2], history[len(history)//2:]
        summary = summarize(old_part)  # call a cheaper model to compress old turns
        return summary + recent_part
    return history
```

This pattern — keep recent turns verbatim, summarize older turns — is the standard "sliding window with compaction" approach used in production agents instead of blindly growing the prompt forever.

### Common Libraries

- `tiktoken` / model-specific tokenizers for counting
- `langchain` / `llama-index` for RAG and memory management abstractions
- Vector DBs (Chroma, Pinecone, Weaviate) for external retrieval — directly relevant to your PlacementRadar RAG pipeline

### Common APIs

- Anthropic Messages API with explicit `cache_control` for prefix caching
- OpenAI's context compaction feature (auto-summarizes history)

### Configuration Options

- `max_tokens` (output limit, separate from total context)
- Cache TTL settings (how long a cached prefix stays reusable)

### Expected Output

Either a successful response within budget, or an explicit context-length error if you exceed the limit — the latter is something every production app needs to handle gracefully, not let surface as a raw API error to the user.

---

## 11. Production Usage

Anthropic's Claude Sonnet line runs up to 1M-token context windows; Google's Gemini line pushes to 2M for native multimodal (video/audio) processing; Meta's Llama 4 Scout claims up to 10M, the largest publicly available window, aimed at whole-codebase or whole-book use cases. None of these numbers should be taken as "the model is uniformly reliable across that whole range" — production teams validate effective context length with their own tests (multi-needle retrieval, not just simple needle-in-haystack) rather than trusting the advertised maximum.

A large share of real-world enterprise agent failures have been attributed to context drift and memory loss rather than model capability limits — which is why production patterns favor multi-tier memory (an active short window plus external searchable storage) over simply maximizing window size. This is directly analogous to what your PlacementRadar "Weak Point Radar" RAG pipeline does: retrieve only what's relevant per query instead of stuffing an entire knowledge base into context.

---

## 12. Design Decisions

**Why not just always use the largest available context window?** Cost and latency scale up sharply with length — 1M-token requests are dramatically more expensive and slower than 8K-token requests, and throughput for serving infrastructure can collapse by an order of magnitude or more at extreme lengths. For most production use cases, a well-curated 8K-32K context with good retrieval beats a sloppy 200K context with everything dumped in.

**Why RAG instead of just relying on a big context window?** RAG keeps the context focused and small, avoiding the "lost in the middle" penalty entirely for irrelevant content, at the cost of retrieval errors (you might fetch the wrong chunk) and added system complexity (you need an embedding pipeline and a vector store).

**Why multi-tier memory over a single window?** Mirrors how operating systems handle memory hierarchies — fast/small (active context) vs. slow/large (external store) — letting an agent behave as if it has near-unlimited memory without paying the cost of attending to all of it every single turn.

---

## 13. Tradeoff Matrix

|Decision|Speed|Cost|Memory|Complexity|Scalability|Reliability|
|---|---|---|---|---|---|---|
|Small window (8K-32K) baseline|Fast|Cheap|Low|Low|Limited to small inputs|High|
|1M+ token window|Much slower|10-100x more expensive|Very high (KV-cache size)|Low (app-side)|Handles huge inputs|Lower (middle-content unreliable)|
|RAG + small window|Fast (after retrieval)|Cheap|Low|High (retrieval pipeline)|Scales to huge corpora|Medium (retrieval errors possible)|
|Hierarchical/multi-tier memory|Medium|Medium|Medium|High|High|Medium-high if retrieval works|
|Summarization/compaction|Faster after compaction|Reduced|Reduced|Medium|Good|Medium (risk of losing detail)|

---

## 14. Cost Impact

Context length directly drives compute (longer prefill, O(n²) attention cost component), memory (KV-cache grows with every token kept in context — covered fully in that note), and cloud cost (providers price extended context tiers higher per token than baseline, on top of the raw token-count cost). For a real example: if your CodeSentinel or PlacementRadar projects pass a full document or transcript into context on every single query rather than retrieving relevant chunks, you're paying full prefill cost on irrelevant content every time — RAG exists specifically to avoid that recurring cost. Prompt/context caching can cut repeated-prefix costs by a large margin (commonly 85-90% on the cached portion), which is why structuring your system prompt and stable instructions to be cacheable is a real, practical cost lever, not a minor detail.

---

## 15. Failure Modes

**Technical Failure: Silent quality drop near advertised limit**

- Cause: models often degrade well before their stated max context (a 200K-token model can become unreliable around 130K).
- Symptoms: answers ignore or misstate facts from earlier in a long prompt, with no error thrown.
- Fix: test your actual workload at realistic lengths with known-answer probes; don't assume advertised = effective.

**Scaling Failure: Throughput collapse at extreme context**

- Cause: KV-cache and attention cost grow with sequence length, consuming disproportionate GPU memory/compute.
- Symptoms: requests that work fine at 10K tokens become dramatically slower or hit rate/availability issues at 500K+.
- Fix: reserve very long context for genuinely necessary use cases; default to RAG/chunking otherwise.

**Operational Failure: Unmanaged history growth**

- Cause: a chat application naively appends every turn to history forever.
- Symptoms: cost per request creeps up turn after turn; eventually hits the context limit mid-conversation.
- Fix: implement sliding window + summarization or retrieval-based history management from day one, not as an afterthought.

**Production Failure: Context drift in agents**

- Cause: an agent's working context loses track of earlier goals/state as the conversation/task grows.
- Symptoms: the agent contradicts earlier decisions, repeats completed steps, or loses track of constraints set early in the task.
- Fix: explicit state tracking outside the raw conversation history (structured memory, not just "more context").

---

## 16. Optimization Techniques

- Use RAG to keep the active context window small and relevant rather than maximizing window size by default.
- Use prompt/context caching for stable prefixes (system prompts, fixed instructions) to avoid repeated processing cost.
- Implement sliding-window + summarization for long conversations instead of unbounded history growth.
- Validate effective context length empirically (multi-needle retrieval tests) rather than trusting advertised maximums.
- Use priority-based context inclusion (critical/high/medium/low) when building agent prompts, so the most important content is never the part that gets dropped or buried.

---

## 17. Interview Preparation

### Beginner Questions

**Q: What is a context window?** A: The maximum number of tokens (input + output combined) a model can process in a single request. Anything beyond that limit either gets rejected or must be truncated/managed by the application.

### Intermediate Questions

**Q: Why doesn't a 1M-token context window mean you can reliably use all 1M tokens?** A: Models show a well-documented "lost in the middle" effect — performance is strongest for content at the start and end of the context and weaker for content buried in the middle. Advertised max length and effective reliable length are different numbers, and the gap can be substantial (a model can degrade well before its stated limit).

### Advanced Questions

**Q: How would you design context management for a long-running agent that needs to remember things across hundreds of turns?** A: Use a multi-tier approach: a small active context window holding only the most recent/relevant turns, an external structured memory store (vector DB or similar) for everything else, and explicit retrieval to pull relevant past information back into the active window only when needed. Avoid relying on raw context window size to "remember" everything — that approach degrades in both reliability (lost in the middle) and cost (everything gets re-processed every turn) as the conversation grows.

---

## 18. Common Mistakes

**Mistake**: treating context window size as a direct proxy for "how good the model is at long documents." _Why it happens_: it's the marketed spec, so it feels like the relevant number. _Correct understanding_: effective context length (where retrieval is actually reliable) is often well below the advertised maximum — test it yourself for your use case.

**Mistake**: letting conversation history grow unbounded in a chat app. _Why it happens_: it's the simplest implementation — just append every turn. _Correct understanding_: this causes both a creeping cost increase and an eventual hard failure when the context limit is hit; manage history proactively from the start.

---

## 19. Current Industry State

128K-200K tokens is the practical baseline across mainstream chat use cases as of mid-2026, with 1M-2M tokens available for specialized needs (Claude, Gemini) and up to 10M for Meta's Llama 4 Scout aimed at extreme cases like whole-codebase ingestion. The industry consensus has shifted away from "bigger window = better" toward context engineering as its own discipline — multi-tier memory, strategic token budgeting, and validated (not assumed) effective context length. Both OpenAI and Anthropic now ship explicit support for context compaction/caching as production features rather than something developers have to hand-roll.

---

## 20. Current Problems & Research

The "lost in the middle" problem remains unsolved at a fundamental level — it's a consequence of how attention spreads across a sequence, not a simple bug. As context grows, the relative "signal" of any single relevant piece of information against everything else shrinks, which is why a single relevant sentence becomes statistically negligible amid millions of distractor tokens at extreme context lengths. NVIDIA's RULER benchmark exists because simpler "needle in haystack" tests were too easy and overstated real long-context capability — comprehensive multi-needle evaluation reveals failures that simple tests miss. The most promising emerging direction is Test-Time Training, which compresses long context directly into model weights at inference time rather than keeping it as raw attended tokens, reportedly giving large speedups and constant latency regardless of context length — though this hasn't yet become a production default.

---

## 21. Future Evolution

Expect context window sizes to plateau around the 1-2M range for most general-purpose models, with niche 10M+ windows remaining specialized rather than becoming the default. The more significant evolution is likely to be in intelligence about context use — better compression, smarter caching, and memory-augmented architectures — rather than further brute-force size growth. Context engineering (deliberate curation) is likely to keep displacing "just make the window bigger" as the dominant strategy for production reliability and cost control.

---

## 22. Engineer Checklist

[ ] Explain what a context window is and why it's bounded [ ] Explain "lost in the middle" and why advertised ≠ effective context length [ ] Implement token-count-based budget checks before sending a request [ ] Implement a sliding-window/summarization strategy for long conversations [ ] Explain when RAG is preferable to a large context window, and when it isn't [ ] Discuss multi-tier memory architectures for long-running agents [ ] Connect context window size directly to cost and KV-cache memory

---

## 23. Knowledge Graph

```
Context Windows
├── Hard limit (training + attention cost bounded)
├── Failure patterns
│   ├── Lost in the Middle
│   └── Context rot (advertised vs effective)
├── Management strategies
│   ├── RAG (retrieval instead of stuffing)
│   ├── Summarization / compaction
│   ├── Sliding window
│   └── Multi-tier memory (active + external store)
├── Cost levers
│   ├── Prompt/context caching
│   └── Token budgeting
└── Evaluation
    ├── Needle-in-haystack (basic, often misleading)
    └── RULER benchmark (comprehensive)
```

---

## 24. If You Remember Only 10 Things

1. Context window = max tokens (input + output) a model can process per request — it's a hard, bounded budget.
2. Bigger context window ≠ uniformly reliable across that entire length; "lost in the middle" is real and well-documented.
3. Advertised max context and effective usable context are different numbers — test your own use case, don't assume.
4. Cost and latency scale up sharply with context length, not linearly — long context is expensive in a way that surprises people.
5. RAG exists to keep context small and relevant instead of relying on raw window size to "fit everything."
6. Production systems use multi-tier memory (small active window + external retrieval) rather than one giant context.
7. Prompt/context caching can cut costs substantially on repeated prefixes (system prompts, fixed instructions).
8. Unmanaged conversation history growth is a common, avoidable production bug — plan for it from day one.
9. A large share of real agent failures trace to context/memory management, not raw model capability.
10. Context engineering (deciding what goes in the window) is now treated as its own discipline, separate from just picking a bigger model.