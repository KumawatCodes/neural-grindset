---
title: "KV-Cache"
phase: "Phase-1 — Core AI Foundations"
group: "02_LLM-Fundamentals"
tags: [ai-engineering, phase-1, study-notes]
status: empty
created: 2026-06-07
---
# KV-Cache

## 1. Executive Summary

KV-cache (Key-Value cache) is the single biggest reason modern LLM inference is fast enough to be usable at all. Without it, generating token N would require recomputing attention from scratch against all N-1 previous tokens — every single time you generate the next token. KV-cache stores those previous computations so each new token only needs a small amount of new work. It's also the single biggest consumer of GPU memory during inference, which is why it directly drives how many concurrent users a server can handle and why long-context requests are so expensive.

You'll run into this whenever you're thinking about why long conversations get progressively slower to start streaming, why context length and "how many users can this server handle at once" are tightly linked, or why providers offer prompt caching as a cost-saving feature.

### 30-Second Interview Answer

"KV-cache stores the Key and Value vectors computed for every token already processed, so when generating the next token you don't have to recompute attention against the entire history from scratch — you just compute the new token's Q/K/V and attend against the cached K/V from before. This turns each generation step from O(n) work (recomputing everything) into roughly O(1) incremental work, at the cost of GPU memory that grows linearly with sequence length and the number of concurrent requests."

### 2-Minute Interview Answer

"Autoregressive generation produces one token at a time, and each new token's attention computation needs the Key and Value vectors of every prior token in the sequence. Without caching, you'd recompute those K/V vectors for the entire history on every single generation step — wasteful, since they don't change once computed (only the new token adds new K/V vectors). KV-cache stores them so each step only computes Q/K/V for the one new token and reuses everything else.

The catch is memory: KV-cache size scales with sequence length × number of layers × number of attention heads × head dimension × 2 (for K and V) × batch size (concurrent requests). For long contexts or many simultaneous users, this becomes the actual bottleneck — not raw compute, but GPU memory bandwidth and capacity. This is why production serving engines like vLLM use 'paged attention,' managing KV-cache in fixed-size memory pages similar to how an OS manages virtual memory, instead of allocating one giant contiguous block per request. It's also why prompt caching exists as an API feature — if your system prompt is identical across many requests, its KV-cache can be computed once and reused, which is where the 85-90% cost savings on cached input comes from. At the extreme end, architectures like Mooncake separate the compute-heavy 'prefill' stage from the memory-heavy 'decode' stage across different hardware pools specifically to manage this memory bottleneck at cluster scale."

---

## 2. The Real Engineering Problem

Imagine serving a chatbot where each response is generated token by token, and on every single token, the model recomputes attention scores against the entire conversation so far from the very beginning, every single time. For a 2000-token conversation generating a 200-token response, that's roughly 200 full re-computations of attention over an ever-growing sequence — most of which is identical work repeated over and over, since the earlier tokens' Key and Value vectors never change once computed.

This isn't just inefficient — it makes the cost of generating each additional token scale with the entire conversation length, meaning long conversations get progressively, painfully slower to generate each new token, not just slower overall. Engineers needed a way to compute each token's contribution to attention exactly once and reuse it for every future step, rather than recomputing the whole history on every step.

---

## 3. Why This Exists

KV-cache exists because Key and Value vectors for already-processed tokens are mathematically static — they don't depend on what comes after them in the sequence (only Query vectors for the current generation step need to be recomputed each time, since they represent "what is the current token looking for"). Caching the static part and only computing the dynamic part each step is a straightforward, large efficiency win that doesn't sacrifice any accuracy.

If KV-caching disappeared, generation speed for long sequences would collapse — each additional output token would cost proportionally more than the last, making anything beyond short responses on long contexts impractically slow. This single optimization is part of why providers can offer multi-thousand-token responses on hundred-thousand-token contexts at all.

---

## 4. Mental Model

Think of KV-cache like taking notes during a long meeting instead of trying to mentally re-derive the entire conversation every time someone asks you a follow-up question. Once someone says something in the meeting, you write down a compact summary (the Key and Value) and file it. When a new question comes in, you don't replay the whole meeting in your head — you just glance at your notes (the cache) and combine them with the new question (the Query) to figure out your answer. The notes for everything said so far never need to be rewritten; you only add a new note for each new thing said.

### How To Visualize It

```
Without KV-cache (recompute every step):
Step 1: attend over [tok1]                          → 1 unit of work
Step 2: attend over [tok1, tok2]                     → 2 units of work
Step 3: attend over [tok1, tok2, tok3]                → 3 units of work
...
Step N: attend over [tok1...tokN]                     → N units of work
Total work across N steps: ~N²/2  (quadratic!)

With KV-cache (reuse stored K/V):
Step 1: compute K1,V1 for tok1, cache them            → 1 unit of work
Step 2: compute K2,V2 for tok2 only, reuse cached K1,V1 → ~1 unit of work
Step 3: compute K3,V3 for tok3 only, reuse cache       → ~1 unit of work
...
Step N: compute KN,VN only, reuse cache                → ~1 unit of work
Total work across N steps: ~N  (linear!)
```

---

## 5. Engineering Evolution

```
Problem: Recomputing attention from scratch on every generation step wastes work and scales badly
↓
Old Solution: No caching — recompute full attention every step
↓
Limitation: Generation cost grows quadratically with sequence length over a full generation
↓
New Solution: KV-cache — store Key/Value vectors for all processed tokens, reuse them
↓
Current Best Practice: Paged KV-cache (vLLM-style) + prefix caching + disaggregated prefill/decode (Mooncake-style)
↓
Current Limitation: KV-cache itself consumes huge GPU memory at long context / high concurrency, becoming the new bottleneck
↓
Future Direction: KV-cache offloading to CPU/SSD with RDMA, predictive eviction, cluster-scale disaggregated cache pools
```

---

## 6. Vocabulary Map

|Term|Meaning|Why It Exists|Where Used|Aliases|
|---|---|---|---|---|
|KV-cache|Stored Key and Value vectors for all previously processed tokens|Avoids recomputing static attention components every generation step|Every autoregressive generation, every production serving engine|KV cache, kv_cache|
|Prefill|The initial pass that processes the entire input prompt at once and populates the KV-cache|Input prompt processing is parallelizable, unlike token-by-token generation|Start of every request|Prompt processing|
|Decode (generation stage)|The token-by-token generation phase that reuses the KV-cache|Where KV-cache savings actually pay off, one token at a time|After prefill, until completion|Generation phase|
|Paged attention|Manages KV-cache in fixed-size memory pages, like OS virtual memory|Avoids wasteful, rigid pre-allocation of one large contiguous memory block per request|vLLM and similar serving engines|PagedAttention|
|Prefix caching|Reusing KV-cache for an identical shared prefix (e.g. system prompt) across multiple requests|Avoids redundant prefill computation for repeated content|OpenAI, Anthropic, Google APIs|Prompt caching|
|KV-cache offloading|Moving KV-cache data to CPU RAM or SSD when GPU memory is full|GPU memory is limited and expensive; offloading trades latency for capacity|Long-context or high-concurrency serving|—|
|Mooncake|A disaggregated architecture separating prefill (compute-bound) and decode (memory-bound) onto different resource pools|Lets each stage be optimized and scaled independently|Moonshot AI's Kimi serving infrastructure|KVCache-centric disaggregation|
|RDMA|Remote Direct Memory Access — fast network transfer between machines, bypassing CPU overhead|Needed to move KV-cache data between disaggregated prefill/decode nodes fast enough to be useful|Cluster-scale disaggregated serving|—|

---

## 7. System Placement

```
Incoming request (system prompt + history + new message)
   ↓
Prefill stage: full forward pass over entire input
   → populates KV-cache for every input token
   ↓
Decode stage: generate token 1
   → uses full KV-cache, computes new K/V for token 1, appends to cache
   ↓
Decode stage: generate token 2
   → uses updated KV-cache (now includes token 1), appends token 2's K/V
   ↓
... repeats until stop condition ...
   ↓
KV-cache discarded (or kept if conversation continues in same session)
```

KV-cache sits between the Transformer's attention mechanism and the serving infrastructure — it's a runtime artifact, not a trained model component, which is why it's managed at the inference-serving layer (vLLM, TensorRT-LLM) rather than inside the model weights themselves.

---

## 8. Internal Working

Trace what happens to the KV-cache across a 3-token prompt followed by 2 generated tokens:

1. **Prefill**: the prompt `["The", "cat", "sat"]` is processed in one parallel forward pass. For every layer, every attention head computes Key and Value vectors for all 3 tokens simultaneously. These are stored: `cache = {K: [K_the, K_cat, K_sat], V: [V_the, V_cat, V_sat]}` per layer/head.
2. The model also computes the first output logits (based on "sat" attending to everything, including itself) and samples token 4, say `"on"`.
3. **Decode step 1**: to process `"on"`, the model only computes Q, K, V for this single new token. It computes `"on"`'s attention by comparing its Query against the _cached_ Keys for `["The", "cat", "sat"]` plus its own new Key — no recomputation of the earlier tokens' K/V needed.
4. The cache is updated: `cache = {K: [K_the, K_cat, K_sat, K_on], V: [V_the, V_cat, V_sat, V_on]}`.
5. The model samples the next token, say `"the"`.
6. **Decode step 2**: same pattern — only `"the"`'s Q/K/V are computed fresh; attention reuses the now-4-token cache, then appends `"the"`'s K/V, growing the cache to 5 entries.
7. This repeats for every subsequent token. The cache only ever grows (within a single request) — it's never recomputed from scratch, only extended.
8. Memory used by this cache = (number of layers) × (number of heads) × (head dimension) × (sequence length so far) × 2 (K and V) × (bytes per value, e.g. 2 for FP16) — multiplied again by however many concurrent requests the server is handling simultaneously.

---

## 9. Core Components

**Cache storage (per layer, per head)**

- Purpose: hold Key/Value vectors for every token processed so far in a request.
- Input: newly computed K/V vectors each decode step.
- Output: the full set of K/V vectors available for the next attention computation.
- Internal logic: simple append-only growth during generation (within one request).
- Failure case: if not managed carefully, naive implementations pre-allocate a fixed maximum-length buffer per request, wasting memory for requests that end up much shorter than the max.

**Paged attention (memory manager)**

- Purpose: allocate/manage KV-cache memory efficiently across many concurrent requests of varying lengths.
- Input: requests with unknown final length.
- Output: dynamically allocated memory "pages" assigned as needed, freed when a request completes.
- Internal logic: borrowed from OS virtual memory paging — fixed-size blocks, mapped per request, avoiding fragmentation and over-allocation.
- Failure case: without this, a server handling many requests of unpredictable length either wastes memory (over-allocating) or crashes (under-allocating); this is the difference between a toy inference script and a production serving engine.

**Prefix cache (cross-request reuse)**

- Purpose: avoid recomputing identical shared content (e.g., the same system prompt) across many separate requests.
- Input: a content hash/identity check for the shared prefix.
- Output: reused KV-cache entries instead of fresh computation.
- Internal logic: if the start of a new request's tokens exactly matches a cached prefix, skip prefill for that portion and reuse the stored cache.
- Failure case: only works for exact prefix matches — even a single differing token at the start invalidates the reuse for everything after that point.

**Disaggregated prefill/decode (Mooncake-style)**

- Purpose: optimize prefill (compute-bound, parallelizable) and decode (memory-bandwidth-bound, sequential) independently rather than forcing one GPU pool to do both well.
- Input: incoming request, routed to a prefill-optimized node first.
- Output: KV-cache transferred (via RDMA) to a decode-optimized node, which then handles token-by-token generation.
- Internal logic: separates two workloads with very different resource profiles onto hardware/pools tuned for each.
- Failure case: requires fast, reliable cache transfer (RDMA) between nodes — if that link is slow or unreliable, the disaggregation adds latency instead of removing it.

---

## 10. Practical Usage

### Installation

```bash
pip install vllm --break-system-packages
```

### Imports

```python
from vllm import LLM, SamplingParams
```

### Basic Example

```python
llm = LLM(model="gpt2")
params = SamplingParams(temperature=0.7, max_tokens=50)
output = llm.generate("Once upon a time", params)
print(output[0].outputs[0].text)
```

vLLM handles KV-cache management (paged attention) transparently — you don't manually manage the cache, but every speed/memory benefit described in this note is happening underneath this call.

### Real Example (using Anthropic's explicit prompt caching)

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    system=[
        {
            "type": "text",
            "text": "You are an expert code reviewer. [... long fixed instructions ...]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "Review this function: ..."}]
)
```

The `cache_control` flag tells Anthropic's API to cache the KV-cache state for this system prompt, so repeated calls with the same system prompt skip re-processing it, directly cutting cost and latency on the cached portion.

### Common Libraries

- `vllm` — industry-standard open-source serving engine with paged KV-cache
- `tensorrt-llm` — NVIDIA's optimized inference engine, also handles KV-cache management

### Common APIs

- Anthropic's explicit `cache_control` headers
- OpenAI's automatic prefix caching for prompts over a length threshold
- Google's implicit + explicit caching with configurable TTLs

### Configuration Options

- Cache TTL (how long a cached prefix remains valid/reusable, e.g. 5 minutes default, up to 1 hour for some providers)
- Whether caching is automatic (OpenAI) or requires explicit flags (Anthropic)

### Expected Output

Faster response times and lower cost on requests that share a prefix with a recently processed request — the actual generated text is identical either way; only speed and cost change.

---

## 11. Production Usage

vLLM's paged attention has become close to an industry standard for open-source/self-hosted serving, directly inspired by OS virtual memory management to handle many concurrent requests of unpredictable length without wasting GPU memory. Anthropic's Messages API exposes explicit `cache_control` for prompt caching with reported 85-90% cost reduction on cached input — a meaningful lever for any application (like a code review tool with a long, fixed system prompt) making many requests that share substantial fixed content. Moonshot AI's Kimi runs a "Mooncake" architecture that separates prefill and decode workloads onto different resource pools connected via RDMA, reportedly delivering a large throughput increase and letting the system handle significantly more concurrent requests than a non-disaggregated setup — this is the kind of infrastructure investment that becomes necessary specifically because KV-cache memory, not raw compute, is the bottleneck at scale.

---

## 12. Design Decisions

**Why cache K/V but not Q?** Query vectors represent "what is the current token looking for" — they're inherently tied to the specific generation step and aren't reused by future steps. Keys and Values represent "what does this token offer," which stays valid and gets looked up by every future token's Query — that's exactly what makes them cacheable.

**Why paged attention instead of fixed pre-allocated buffers?** Pre-allocating a buffer sized to the maximum possible sequence length per request wastes huge amounts of memory for the (common) case where requests are much shorter than the max. Paging allocates memory incrementally as needed, much closer to actual usage, letting a server handle far more concurrent requests with the same GPU memory.

**Why disaggregate prefill and decode onto separate hardware pools?** Prefill is compute-bound (a big parallel matrix multiplication over the whole prompt) while decode is memory-bandwidth-bound (small, sequential steps repeatedly reading the growing KV-cache). A single GPU pool optimized for one tends to underserve the other; separating them lets each stage run on infrastructure tuned for its actual bottleneck.

---

## 13. Tradeoff Matrix

|Decision|Speed|Cost|Memory|Complexity|Scalability|
|---|---|---|---|---|---|
|No caching (recompute every step)|Very slow at length|High (wasted compute)|Low (nothing stored)|Lowest|Poor|
|Local GPU KV-cache|Fast|Baseline|GPU-memory-limited|Low|Limited to single-node capacity|
|CPU offload|Slower (DDR latency)|Lower GPU cost|Much higher capacity|Medium|Better than GPU-only|
|SSD offload|Much slower (NVMe latency)|Lowest hardware cost|Highest capacity|Medium-high|Best raw capacity, worst latency|
|Mooncake-style disaggregation|Faster overall (better scheduling)|Higher infra complexity cost|Effectively pooled across cluster|High|Best at cluster scale|
|Prefix caching|Much faster on cache hits|85-90% cheaper on cached portion|Same memory, just reused|Low (mostly API-side)|Good for repeated-prefix workloads|

---

## 14. Cost Impact

KV-cache size, not raw model compute, is frequently the actual limiting factor for how many concurrent users a GPU can serve — every additional concurrent long-context conversation consumes more GPU memory just to hold its cache, directly capping throughput regardless of how fast the compute itself is. Prefix/prompt caching is one of the most concrete cost levers available to you as an API consumer: if your application sends the same long system prompt or document on every request (a RAG pipeline reusing the same retrieved context across follow-up questions, for instance), enabling caching can cut a substantial portion of your input token cost. On the infrastructure side, KV-cache offloading and disaggregation trade hardware/engineering complexity for the ability to serve far more concurrent long-context requests per GPU dollar spent — exactly the kind of tradeoff that becomes worth making once you're operating at meaningful scale rather than prototyping.

---

## 15. Failure Modes

**Technical Failure: GPU out-of-memory from KV-cache growth**

- Cause: long context length × many concurrent requests exceeds available GPU memory for cache storage.
- Symptoms: requests fail or get queued/rejected under load, even though raw compute capacity seems sufficient.
- Fix: use a serving engine with paged attention (vLLM-style) to manage memory more efficiently, or scale to KV-cache offloading/disaggregation at higher load.

**Scaling Failure: Prefix cache misses due to non-deterministic prompt construction**

- Cause: application code reorders, reformats, or slightly varies content that should be an identical cacheable prefix.
- Symptoms: expected cost savings from prompt caching don't materialize — every request looks "new" to the cache.
- Fix: keep cacheable content (system prompts, fixed instructions) byte-for-byte identical and positioned consistently (usually at the start) across requests.

**Operational Failure: Cache TTL expiry mid-burst**

- Cause: cached prefix expires (e.g., after 5 minutes of inactivity) right as a new burst of requests arrives.
- Symptoms: a sudden, unexpected cost/latency spike that looks like caching "isn't working" intermittently.
- Fix: understand your provider's TTL behavior and, if available, choose a longer TTL tier for workloads with bursty-but-infrequent traffic patterns.

**Production Failure: Disaggregated cache transfer latency**

- Cause: slow or unreliable network link between prefill and decode nodes in a disaggregated architecture.
- Symptoms: the disaggregation adds latency instead of the throughput gains it's supposed to provide.
- Fix: use high-speed interconnects (RDMA) specifically designed for this kind of cross-node memory transfer, not a generic network link.

---

## 16. Optimization Techniques

- Use a serving engine with paged attention (vLLM, TensorRT-LLM) instead of naive fixed-buffer KV-cache allocation.
- Structure prompts to put stable, repeated content (system prompts, fixed instructions) first and keep it byte-identical across requests to maximize prefix cache hits.
- Use explicit caching flags where the API requires them (Anthropic's `cache_control`) — don't assume caching happens automatically everywhere.
- For high-concurrency, long-context production workloads, evaluate disaggregated prefill/decode architectures rather than scaling a single monolithic serving pool.
- Monitor actual GPU memory usage attributable to KV-cache separately from model weight memory — they're different bottlenecks with different scaling behavior.

---

## 17. Interview Preparation

### Beginner Questions

**Q: What problem does KV-cache solve?** A: Without it, generating each new token would require recomputing attention against the entire previous sequence from scratch every single step. KV-cache stores the Key/Value vectors for already-processed tokens so each new step only needs to compute the new token's own K/V and reuse everything else.

### Intermediate Questions

**Q: Why does KV-cache grow with sequence length, and why does that matter in production?** A: Every token processed adds a new K/V entry per layer/head to the cache, so cache size scales linearly with sequence length (and multiplies further by the number of concurrent requests a server is handling). In production, this often becomes the actual memory bottleneck — not the model weights themselves — directly limiting how many concurrent users or how long a context a given GPU can serve.

### Advanced Questions

**Q: Explain why disaggregating prefill and decode onto separate hardware pools (Mooncake-style) can improve throughput.** A: Prefill is a large, parallel, compute-bound operation (process the whole prompt at once), while decode is a small, sequential, memory-bandwidth-bound operation (repeatedly read the growing cache to generate one token at a time). A single GPU pool tuned for one workload underserves the other. Separating them onto pools optimized for each — connected by a fast interconnect (RDMA) to transfer the KV-cache between stages — lets both stages run closer to their respective optimal hardware utilization, which is reported to deliver significant throughput gains at cluster scale.

---

## 18. Common Mistakes

**Mistake**: assuming KV-cache and "context window" are the same concept. _Why it happens_: both scale with sequence length and are often discussed together. _Correct understanding_: context window is the model's input/output token limit; KV-cache is the runtime memory structure that makes processing within that window efficient. A model could theoretically have a large context window but be served inefficiently without good KV-cache management, or vice versa.

**Mistake**: assuming prompt caching happens automatically on every provider. _Why it happens_: it's automatic on some platforms (OpenAI), leading to the assumption it's universal. _Correct understanding_: some providers (Anthropic) require explicit cache control flags — relying on assumed automatic caching can silently mean you're not getting the cost savings you expect.

---

## 19. Current Industry State

Paged KV-cache management (vLLM-style) is now close to an industry-standard practice for serving infrastructure, and explicit or automatic prompt/prefix caching is a standard API feature across OpenAI, Anthropic, and Google as of mid-2026. The more advanced frontier is disaggregated prefill/decode architectures (Mooncake-style), which are moving from a research idea into production retrofits at companies operating at very large scale, specifically to address the KV-cache memory wall that constrains long-context serving.

---

## 20. Current Problems & Research

The fundamental unsolved problem is that KV-cache memory consumption scales with sequence length and concurrency in a way that raw GPU memory capacity struggles to keep up with, especially as context windows push toward the million-token range — a single long-context request can consume hundreds of gigabytes of cache. Current research directions include better predictive cache eviction (deciding which cached entries are safe to discard under memory pressure), more efficient offloading to CPU/SSD tiers with lower latency penalties, and cluster-scale disaggregated cache pools (Mooncake and similar) that treat KV-cache as a shared cluster resource rather than something tied to a single GPU.

---

## 21. Future Evolution

Expect KV-cache management to keep shifting from a per-GPU, per-request concern toward a cluster-wide resource management problem, similar to how distributed systems treat memory and storage as pooled resources rather than per-machine silos. Disaggregated architectures like Mooncake are likely to become more common as long-context, high-concurrency serving becomes the norm rather than the exception, and predictive/ML-based cache eviction policies may start replacing simple recency-based eviction as workloads get more sophisticated.

---

## 22. Engineer Checklist

[ ] Explain why Key/Value vectors are cacheable but Query vectors aren't [ ] Explain how KV-cache turns O(n²) repeated work into roughly O(n) total work across a generation [ ] Explain why KV-cache memory, not just compute, is often the real production bottleneck [ ] Explain paged attention and why it beats fixed-buffer allocation [ ] Use explicit or automatic prompt caching in a real API call [ ] Explain disaggregated prefill/decode architectures and why they help throughput [ ] Connect KV-cache directly to context window cost and concurrency limits

---

## 23. Knowledge Graph

```
KV-Cache
├── Core mechanism
│   ├── Key/Value storage per layer/head
│   └── Prefill (build cache) vs Decode (reuse + extend cache)
├── Memory management
│   ├── Paged attention (vLLM-style)
│   ├── CPU/SSD offloading
│   └── Disaggregated prefill/decode (Mooncake)
├── Cost optimization
│   └── Prefix/prompt caching (cross-request reuse)
└── Downstream impact
    ├── Concurrency limits (how many users a GPU can serve)
    └── Context window cost economics
```

---

## 24. If You Remember Only 10 Things

1. KV-cache stores Key/Value vectors for already-processed tokens so each new token only needs incremental work, not full recomputation.
2. Without it, generation cost over a full response would scale quadratically with sequence length instead of linearly.
3. Query vectors aren't cached (they're step-specific); Key and Value vectors are cached (they stay valid for all future steps).
4. KV-cache memory, not raw compute, is frequently the real bottleneck limiting concurrent users a GPU can serve.
5. Cache size scales with sequence length × layers × heads × concurrent requests — long context and high concurrency compound directly.
6. Paged attention (vLLM-style) manages this memory like an OS manages virtual memory, avoiding wasteful fixed allocation.
7. Prompt/prefix caching reuses KV-cache across requests sharing identical fixed content (e.g. system prompts), cutting cost substantially.
8. Some providers cache automatically (OpenAI); others require explicit flags (Anthropic's `cache_control`) — don't assume.
9. Disaggregated architectures (Mooncake-style) separate compute-bound prefill from memory-bound decode onto different hardware pools for better throughput at scale.
10. KV-cache is a runtime/serving-layer concept, not a trained model component — it's managed by your inference engine, not your model weights.