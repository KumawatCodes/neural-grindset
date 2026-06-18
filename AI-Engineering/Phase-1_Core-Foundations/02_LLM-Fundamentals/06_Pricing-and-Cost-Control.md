---
title: "Pricing & Cost Control"
phase: "Phase-1 — Core AI Foundations"
group: "02_LLM-Fundamentals"
tags: [ai-engineering, phase-1, study-notes]
status: empty
created: 2026-06-07
---
# Pricing & Cost-Control

## 1. Executive Summary

Pricing and cost-control is the discipline of understanding how LLM providers charge for usage and how engineers design systems to keep that bill under control. It matters because inference (running the model to answer requests) is not a side cost — by 2026, it's roughly 85% of an enterprise's entire AI budget. Training a model once is expensive, but serving it to millions of users every day, forever, costs far more over its lifetime. Every $1B spent on training a frontier model produces roughly $15-20B in downstream inference costs.

You'll run into this the moment you build anything beyond a toy demo: a feature that worked fine on your test account suddenly costs $40,000/month in production because nobody accounted for token volume, context length, or retry storms. Engineers who understand pricing mechanics (per-token billing, caching discounts, batch discounts) can cut costs by 50-90% without touching model quality. Engineers who don't understand it get paged at 3 AM because the AI feature blew through the monthly budget in a week.

### 30-Second Interview Answer

"LLM providers charge per token — separately for input and output, with output usually costing 4-5x more than input because generation is the expensive part. The big cost levers are: prompt caching (reusing repeated context like system prompts cuts cost by 85-90%), batch APIs (50% discount if you don't need instant responses), and context length (longer contexts cost more per token in tiered pricing). At scale, inference dominates the AI budget — not training — so cost-control is really about minimizing redundant token processing, not about making the model itself cheaper."

### 2-Minute Interview Answer

"Pricing for LLMs is per-token: you pay for every token in your prompt (input) and every token the model generates (output), usually billed separately because output tokens require a full forward pass each, while input tokens can be processed in parallel during prefill. Output tokens are typically priced 4-5x higher than input tokens for this reason.

The biggest lever for cost control is prompt caching: if your request reuses the same prefix repeatedly — like a long system prompt, a knowledge base injected into context, or a multi-turn conversation history — providers let you cache the KV-cache computation for that prefix and charge a fraction (often 10-15% of normal price) on cache hits. This alone can cut costs 85-90% for chatbot-style or agentic workloads that repeat large context blocks across calls.

The second lever is batch processing: if your workload isn't latency-sensitive (e.g. nightly data processing, bulk classification), providers offer ~50% discounts for batched, asynchronous requests processed within a longer SLA window (often 24 hours).

The third lever is context-aware tiered pricing — going above certain context thresholds (e.g. 200K tokens) can double the per-token price, because serving very long contexts requires more GPU memory and reduces how many concurrent requests a server can handle.

At the org level, this becomes a FinOps problem: you need real-time token usage monitoring, budget alerts, multi-vendor routing (sending cheap/simple queries to a smaller cheaper model and only routing hard queries to the expensive frontier model), and architectural choices like RAG instead of stuffing everything into context, since RAG retrieves only relevant chunks instead of paying to process an entire document on every single query."

---

## 2. The Real Engineering Problem

Picture a startup building an AI customer support agent. In the demo, it costs almost nothing — a handful of test queries, a short system prompt, no real traffic. Three weeks after launch, the finance team flags a $28,000 invoice from the LLM provider. What happened?

The system prompt was 3,000 tokens long (product details, tone guidelines, safety rules). It was being resent, in full, on every single customer message, because the conversation history was passed fresh every time with no caching enabled. Multiply 3,000 tokens × every message × thousands of daily conversations × multiple turns per conversation, and the system prompt alone accounted for more cost than the actual useful work of answering questions. Nobody had budgeted for the fact that "the same 3,000 tokens are being paid for, in full, again and again."

This is the real engineering problem: token-based pricing makes redundant work expensive in a way that's invisible until the invoice arrives. Engineers need pricing models, caching strategies, and usage monitoring built into the system from day one — not bolted on after a budget crisis.

---

## 3. Why This Exists

Per-token pricing exists because tokens are a reasonable proxy for compute (FLOPs). Processing more tokens means more matrix multiplications means more GPU time means more cost to the provider — so passing that cost through per-token is the most direct, defensible way to charge for a resource whose cost genuinely scales with usage. It's also transparent: a developer can estimate cost before making a call, instead of guessing at some opaque "request" or "session" unit.

If per-token pricing didn't exist, providers would have to choose between flat subscription pricing (which punishes light users and gives heavy users a free ride, encouraging abuse) or fully opaque enterprise contracts (which kill the self-serve developer ecosystace that made these APIs popular in the first place). Cost-control practices (caching, batching, tiering) exist because, without them, the natural growth of conversation length and context usage in real applications causes runaway, unpredictable spend — engineers need levers to bend that cost curve back down.

---

## 4. Mental Model

Think of token pricing like a taxi meter that runs separately for "listening" and "talking." Every word the customer says to the driver (input tokens) costs a little. Every word the driver says back (output tokens) costs more, because talking back requires the driver to actually think and construct a response, not just listen passively. If the customer repeats the same long backstory at the start of every ride (the system prompt), a smart taxi company would let the driver "remember" that backstory from a sticky note instead of charging full price to re-hear it every time — that's prompt caching. If the customer doesn't need an answer right now and is fine waiting until tomorrow, the taxi company offers a discount for non-urgent rides — that's the batch API.

### How To Visualize It

```
Single chatbot turn, no caching:
[System prompt: 3,000 tok] + [History: 2,000 tok] + [New msg: 50 tok]  → pay for ALL 5,050 input tokens
                                                                         every single turn, even though
                                                                         5,000 of those tokens are identical
                                                                         to the previous turn.

Same turn, WITH prompt caching:
[System prompt: 3,000 tok — CACHED, ~10-15% price] 
+ [History: 2,000 tok — CACHED if unchanged, ~10-15% price]
+ [New msg: 50 tok — full price]
→ pay close to full price for only 50 tokens, fraction price for 5,000 tokens.
```

---

## 5. Engineering Evolution

```
Problem: Token-based costs grow with conversation length and context size, becoming unpredictable
↓
Old Solution: Flat per-token pricing, no caching, no batching — pay full price for every token, every call
↓
Limitation: Repeated context (system prompts, long histories, RAG documents) gets billed at full price
            again and again, causing runaway costs that don't reflect new "useful" work being done
↓
New Solution: Prompt caching (85-90% discount on repeated prefixes) + Batch API (50% discount for
              non-urgent work) + context-aware tiered pricing
↓
Current Best Practice: Architect prompts so static/repeated content sits at the front (for caching),
                        route easy queries to cheap models, batch non-urgent workloads, monitor token
                        usage in real time, use RAG instead of stuffing full documents into context
↓
Current Limitation: Caching only works on exact-match prefixes; agentic workflows with constantly
                     shifting context still struggle to get cache hits; cost forecasting for new
                     features remains hard
↓
Future Direction: Per-action/outcome-based pricing instead of per-token, agentic plan caching
                   (cache reusable task templates, not just text prefixes), automatic context
                   compaction built into the API itself
```

---

## 6. Vocabulary Map

|Term|Meaning|Why It Exists|Where Used|Aliases|
|---|---|---|---|---|
|Per-token pricing|Billing based on number of input/output tokens processed|Tokens approximate real compute cost|All major LLM APIs|Token-based billing|
|Input tokens|Tokens in the prompt sent to the model|Needs separate, usually cheaper pricing (parallel prefill)|Every API call|Prompt tokens|
|Output tokens|Tokens the model generates in its response|Costs more — each token requires a full sequential forward pass|Every API call|Completion tokens, generated tokens|
|Prompt caching|Reusing the cached KV-cache computation for a repeated prefix|Avoids paying full price to recompute identical context|Multi-turn chat, RAG, agents|Context caching, cache_control|
|Cache hit / miss|Whether a request's prefix matched a previously cached one|Determines whether the discount applies|Caching systems|—|
|Batch API|Asynchronous, non-real-time request processing at a discount|Lets providers schedule work during idle GPU capacity|Bulk classification, offline jobs|Batch processing, Flex processing|
|Context-aware tiered pricing|Higher per-token price beyond a context length threshold|Long context requires more GPU memory per request, reducing concurrency|Extended-context requests|Long-context surcharge|
|FinOps (for AI)|Financial operations discipline applied to AI infrastructure spend|Token costs are volatile and need active management, like cloud cost FinOps|Enterprise AI cost governance|AI cost governance|
|Plan caching|Caching a reusable structured "task plan," not just raw text|Agentic workflows repeat task patterns more than exact text|Agent frameworks|Task-level caching|
|Context compaction|Automatically summarizing/shrinking conversation history|Reduces token volume without manual prompt engineering|Newer chat/agent APIs|Auto-summarization|
|Multi-vendor arbitrage|Routing requests to whichever provider/model is cheapest for that task|Different models have very different price/quality tradeoffs|Cost-sensitive production systems|Model routing|

---

## 7. System Placement

```
User Request
   ↓
Application Layer (decides: which model? cache this prefix? batch this?)
   ↓
Cost-Control Layer (token counting, budget checks, routing logic)
   ↓
LLM Provider API (charges per input/output token, applies cache/batch discounts)
   ↓
Billing/Usage Dashboard ← (engineers monitor here to catch runaway costs)
   ↓
Response back to User
```

Cost-control sits as a layer wrapping every LLM call — not inside the model itself. It's an application-and-infrastructure-level concern: deciding what to send, how to structure it for caching, which model tier to use, and whether the request needs to be real-time or can be batched.

---

## 8. Internal Working

Trace a single chatbot request through a cost-aware system:

1. User sends a message. The app assembles the full prompt: system prompt (static, 3,000 tokens) + conversation history (grows each turn) + new user message.
2. Before sending, the app checks: has this exact prefix (system prompt + history-so-far) been sent before and is it still within the cache TTL (time-to-live, often 5 minutes to 1 hour)? If yes, it's marked for caching via a `cache_control` header (Anthropic-style) or happens automatically if length exceeds a threshold (OpenAI-style, automatic above ~1,024 tokens).
3. The request is sent. The provider's server checks if the prefix matches a cached KV-cache entry on its GPUs. Cache hit → only the new tokens (the new user message) need a fresh forward pass; the cached prefix's computation is reused. Cache miss → everything is computed fresh and the result is cached for next time.
4. Billing is computed: cached input tokens at a steep discount (often ~10% of normal price), non-cached input tokens at full price, output tokens at the (usually higher) output rate.
5. The app receives the response, logs the actual token usage returned in the response metadata, and updates its real-time cost dashboard / budget tracker.
6. If usage approaches a budget threshold, the app might switch to a cheaper model for subsequent requests, trigger an alert, or apply rate limiting.

---

## 9. Core Components

**Token Counter**

- Purpose: Estimate or measure exact token usage before/after a call.
- Input: Raw prompt text.
- Output: Token count (input/output split).
- Internal Logic: Runs the same tokenizer the model uses (or an approximation) to count tokens locally before sending, to predict cost.
- Failure Cases: Using the wrong tokenizer (e.g. estimating GPT tokens with a Llama tokenizer) gives inaccurate cost predictions.

**Cache Controller**

- Purpose: Decide what part of a prompt should be marked cacheable and structure prompts to maximize cache hits.
- Input: Full prompt (system + history + new message).
- Output: Prompt with cache boundaries marked (explicit headers or automatic length-based triggers).
- Internal Logic: Keeps static/repeated content at the front of the prompt, dynamic content at the end, since caching works on prefix matches.
- Failure Cases: Putting dynamic content (like a timestamp) at the start of the prompt breaks cache hits for everything after it.

**Budget Monitor**

- Purpose: Track real-time spend against a budget and alert before overruns.
- Input: Per-call token usage and pricing.
- Output: Running cost totals, alerts, dashboards.
- Internal Logic: Aggregates usage logs, applies current pricing tables, compares against thresholds.
- Failure Cases: Stale pricing tables (provider changed prices) lead to inaccurate cost tracking.

**Model Router**

- Purpose: Send each request to the cheapest model capable of handling it well.
- Input: Query, complexity signal (sometimes a cheap classifier model).
- Output: Choice of model tier (e.g. Haiku vs Sonnet vs Opus).
- Internal Logic: Simple queries → cheap fast model; complex reasoning → expensive frontier model.
- Failure Cases: Misrouting a hard query to a cheap model degrades quality in ways that are hard to detect automatically.

---

## 10. Practical Usage

### Installation

No special install needed beyond the provider's SDK (e.g. `pip install anthropic` or `pip install openai`). Token counting can use `tiktoken` (OpenAI) or the provider's own counting utility.

### Imports

```python
import anthropic
client = anthropic.Anthropic()
```

### Basic Example (no caching — full price every call)

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    system="You are a customer support agent for Acme Corp. [3000 tokens of policy text...]",
    messages=[{"role": "user", "content": "What's your return policy?"}]
)
```

Every call re-sends and re-bills the full 3,000-token system prompt.

### Real Example (with prompt caching)

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=300,
    system=[
        {
            "type": "text",
            "text": "You are a customer support agent for Acme Corp. [3000 tokens of policy text...]",
            "cache_control": {"type": "ephemeral"}  # mark this block as cacheable
        }
    ],
    messages=[{"role": "user", "content": "What's your return policy?"}]
)
print(response.usage)  # shows cache_creation_input_tokens vs cache_read_input_tokens
```

Line by line: the `cache_control` field tells the provider "this block rarely changes, cache it." The first call pays full price and creates the cache (`cache_creation_input_tokens`). Every subsequent call within the TTL window pays the discounted `cache_read_input_tokens` rate for that block instead.

### Common Libraries

`anthropic`, `openai`, `tiktoken` (token counting), `langchain` / `litellm` (multi-provider routing and cost tracking).

### Common APIs

Anthropic Messages API (`cache_control` headers), OpenAI Chat Completions/Responses API (automatic caching above 1,024 tokens), Google Gemini API (implicit + explicit caching with configurable TTL), Batch APIs (Anthropic Batch, OpenAI Batch).

### Configuration Options

Cache TTL (5 min default, up to 1 hour), batch vs real-time mode, model tier selection, max_tokens cap (limits worst-case output cost per call).

### Expected Output

A response object whose `usage` field breaks down input tokens, output tokens, and (if applicable) cached vs non-cached input tokens — this is what you log for cost tracking.

---

## 11. Production Usage

**Anthropic**: Offers explicit `cache_control` headers giving developers fine-grained control over what's cached, with 85-90% discounts on cache hits and both 5-minute and 1-hour cache durations for different workload patterns. Their Batch API gives further discounts for non-urgent bulk workloads.

**OpenAI**: Automatic prompt caching kicks in for prompts over 1,024 tokens with no developer action needed — simpler to use but less control than Anthropic's explicit model. Their newer Responses API (June 2026) adds built-in context compaction (auto-summarizing history) and Priority/Flex processing tiers, letting developers explicitly trade latency for cost.

**Google**: Gemini offers both implicit and explicit caching with configurable TTLs up to an hour, aimed at the very long context windows (1M-2M tokens) where caching savings matter most.

**Enterprise pattern**: Companies running high-volume agentic systems (customer support bots, coding assistants, internal copilots) report that inference costs make up the vast majority of their total AI infrastructure bill — far more than training or fine-tuning ever did — which is why FinOps practices (budget monitoring, multi-vendor routing, plan-level caching achieving ~46% cost reduction in agentic workloads) have become a standard part of AI platform engineering rather than an afterthought.

---

## 12. Design Decisions

**Why per-token instead of per-request pricing?** Per-request pricing would punish providers when a request happens to be huge (a 100-page document) and overcharge users on tiny requests. Per-token aligns cost with actual compute used, which is fairer and more predictable for both sides.

**Why charge more for output tokens than input tokens?** Input tokens can be processed in parallel during the "prefill" phase (the model reads the whole prompt at once). Output tokens must be generated one at a time, sequentially, autoregressively — each one requires a full pass through the model. Sequential work is inherently more expensive per token than parallel work.

**Why cache discounts instead of just lowering the base price?** A flat lower base price would lower revenue on all the genuinely new computation too. Cache discounts target the specific case where the provider is doing less actual work (reusing stored KV-cache), so the discount maps directly to reduced cost-to-serve, not just a blanket price cut.

**Why does batch processing get a discount?** Batch requests can be scheduled into idle GPU capacity instead of competing for real-time serving slots, so they cost the provider less to fulfill — the discount passes that savings to the user in exchange for accepting higher latency.

---

## 13. Tradeoff Matrix

|Approach|Speed|Cost|Memory/GPU|Complexity|Scalability|Reliability|
|---|---|---|---|---|---|---|
|Per-token, no caching|Baseline|Highest|Baseline|Lowest|Baseline|High|
|Prompt caching|Faster (cache hits)|85-90% lower on cached portion|Lower (less recompute)|Medium (prompt structuring)|Higher|High|
|Batch API|Much slower (hours)|~50% lower|N/A (provider-side)|Low|High for bulk jobs|High|
|Model routing (cheap+expensive mix)|Variable|Significantly lower overall|N/A|High (needs routing logic)|High|Medium (misrouting risk)|
|On-prem (>100 GPUs, >65% utilization)|Comparable|40-60% lower at scale|Self-managed|Very high (ops burden)|Limited by hardware owned|Medium (self-managed reliability)|
|Cloud (elastic)|Comparable|Higher per-unit at scale|Provider-managed|Low|Very high (instant scale)|High|

---

## 14. Cost Impact

**Compute**: Token volume is the direct cost driver — every additional repeated context token without caching is pure waste.

**Memory/GPU**: Longer contexts and higher concurrency both increase KV-cache memory pressure on the provider's side, which is why context-aware tiered pricing exists (you're paying partly for the GPU memory your request occupies, not just the FLOPs).

**Storage**: Cached prefixes need to be stored (in GPU memory or fast storage) for the cache TTL window — this is provider-side cost but is reflected in the discount structure.

**Network**: Negligible for text, but becomes relevant for multimodal (image/video/audio) inputs which consume disproportionately more tokens.

**Cloud Costs (practical example)**: A support bot sending an uncached 3,000-token system prompt for 50,000 conversations/month, averaging 4 turns each, sends that system prompt 200,000 times. At ~$3/million input tokens, that's 200,000 × 3,000 = 600M tokens = ~$1,800/month just for the repeated system prompt. With caching at ~90% discount on cache hits, that drops to roughly $200/month for the same prefix — the other $1,600 simply disappears.

**Engineering Complexity**: Implementing caching correctly (structuring prompts so static content is first, managing TTLs, handling cache misses gracefully) and budget monitoring adds real engineering work, but the payoff is usually a 50-90% cost reduction for chat/agentic workloads — one of the highest-leverage optimizations available.

---

## 15. Failure Modes

**Technical Failure: Cache misses due to prompt restructuring**

- Cause: Dynamic content (timestamps, random IDs, reordered fields) placed before the static content in the prompt.
- Symptoms: Cache hit rate near zero despite caching being "enabled"; costs stay high.
- Fixes: Always put static/repeated content first, dynamic content last; audit prompt structure for accidental non-determinism at the front.

**Scaling Failure: Unbounded conversation history growth**

- Cause: Appending every turn to history with no trimming or summarization.
- Symptoms: Token cost per turn grows linearly with conversation length; eventually hits context limits too.
- Fixes: Implement context compaction/summarization, sliding window history, or hierarchical memory (keep recent turns verbatim, summarize older ones).

**Operational Failure: No budget alerting**

- Cause: Treating LLM cost like a fixed line item instead of monitoring it like cloud infra spend.
- Symptoms: Budget overruns discovered only when the monthly invoice arrives.
- Fixes: Real-time token usage dashboards, automated alerts at spend thresholds, per-feature cost attribution.

**Production Failure: Retry storms inflating cost**

- Cause: Client-side retry logic re-sending the full prompt on every transient failure without backoff or dedup.
- Symptoms: Cost spikes correlated with provider outages or rate-limit errors, disproportionate to actual successful traffic.
- Fixes: Exponential backoff with jitter, idempotency keys, circuit breakers that stop retrying after a threshold.

---

## 16. Optimization Techniques

- **Prompt caching**: structure prompts with static content first; mark cache boundaries explicitly where supported.
- **Batch non-urgent work**: move bulk classification, embedding generation, and offline analysis to batch APIs for ~50% savings.
- **Model routing/cascading**: use a cheap, fast model to handle easy queries and only escalate to expensive frontier models for genuinely hard ones (often via a lightweight classifier or confidence threshold).
- **Context compaction**: summarize old conversation turns instead of keeping full verbatim history forever.
- **RAG over full-document stuffing**: retrieve only relevant chunks instead of paying to process an entire document on every query.
- **Output length capping**: set sane `max_tokens` limits — runaway generations (e.g. a model stuck in a repetition loop) are a real, avoidable cost risk.
- **Plan caching for agents**: cache reusable structured task plans/templates, not just raw text, since agentic workflows repeat task patterns more than exact prompts (reported ~46% cost reduction in production agentic systems).
- **Multi-vendor arbitrage**: route different workload types to whichever provider currently offers the best price/quality tradeoff for that task.

---

## 17. Interview Preparation

### Beginner Questions

**Q: Why is output more expensive than input per token?** A: Input tokens are processed in parallel during prefill (the model reads the whole prompt in one pass). Output tokens are generated one at a time, sequentially — each requires a full forward pass through the model, which is inherently more expensive per token. Expected reasoning: connects the cost asymmetry to the prefill/decode distinction, not just "because providers say so."

**Q: What is prompt caching and why does it save money?** A: It's reusing the already-computed KV-cache for a repeated prompt prefix instead of recomputing it from scratch on every call. Since the computation is reused rather than redone, the provider charges a steep discount for cache hits. Expected reasoning: ties the cost savings to actual reduced compute, not just a marketing discount.

### Intermediate Questions

**Q: Your chatbot's costs are growing faster than your user count. What do you check first?** A: Whether conversation history is growing unbounded and being resent in full every turn, and whether prompt caching is actually achieving hits (check the cache_read vs cache_creation token counts in usage logs). Unbounded history growth combined with no caching is the most common runaway-cost pattern. Expected reasoning: diagnostic, ties symptom to the most likely structural cause.

**Q: When would you use the Batch API instead of real-time calls?** A: Whenever the workload isn't latency-sensitive — nightly data processing, bulk classification/labeling, generating embeddings for a large corpus, or any job where waiting hours for results is acceptable. The discount (~50%) makes it worthwhile to restructure non-urgent workloads this way. Expected reasoning: recognizes batch as a latency-for-cost tradeoff, not a strictly worse option.

### Advanced Questions

**Q: Why does context-aware tiered pricing exist, and what does it tell you about the provider's infrastructure?** A: Longer contexts require proportionally more GPU memory for KV-cache per request, which reduces how many concurrent requests a GPU can serve at once. The tiered pricing reflects that the marginal cost-to-serve genuinely increases with context length — it's not arbitrary, it tracks a real infrastructure constraint (memory bandwidth/capacity, not just FLOPs). Expected reasoning: connects pricing tiers to underlying serving infrastructure constraints (KV-cache memory), showing systems-level understanding.

**Q: Design a cost-control architecture for an agentic system that makes many LLM calls per user task.** A: Key elements: (1) a model router that sends sub-tasks to the cheapest capable model rather than always using the frontier model, (2) plan/task-level caching for repeated agent reasoning patterns, not just text-prefix caching, (3) context compaction to prevent the agent's working memory/history from growing unbounded across many tool calls, (4) real-time per-task cost attribution so you can identify which task types are disproportionately expensive, (5) circuit breakers to stop an agent loop that's spiraling into excessive tool calls or retries. Expected reasoning: shows awareness that agentic systems multiply the standard cost problems (caching, history growth, retries) across many calls per single user action, requiring task-level (not just call-level) cost controls.

---

## 18. Common Mistakes

**Mistake: Assuming the demo cost predicts production cost** Why it happens: Demos have low traffic and short conversations; production has both scale and conversation-length growth. Correct understanding: Cost scales with both traffic volume AND conversation/context length growth over time — model these separately, not as one number.

**Mistake: Putting dynamic content before static content in prompts** Why it happens: Engineers often build prompts by appending "context" (timestamps, user IDs) first, then static instructions, without thinking about cache structure. Correct understanding: Caching works on prefix matches — static, repeated content must come first for cache hits to occur at all.

**Mistake: Treating all queries as needing the most capable (expensive) model** Why it happens: Defaulting to "use the best model for everything" feels safest. Correct understanding: Most production traffic is simple; routing easy queries to cheaper models and reserving expensive models for genuinely hard cases cuts cost dramatically with minimal quality loss.

**Mistake: No budget alerting until the invoice arrives** Why it happens: LLM cost is treated like a fixed software license cost rather than variable cloud-style infrastructure spend. Correct understanding: LLM costs need the same real-time monitoring and alerting discipline as cloud infrastructure (FinOps), because usage and cost can spike unpredictably.

---

## 19. Current Industry State

Inference spend is now the dominant line item in enterprise AI budgets — roughly 85% of total spend, with training representing only 10-20% of a model's lifecycle cost. This has flipped the traditional intuition that "training is the expensive part." 2026 pricing across major providers (Anthropic Sonnet 4.5 at $3/$15 per million input/output tokens, Opus 4.5 at $5/$25, Haiku 4.5 at $1/$5) reflects clear tiering by capability, with extended-context pricing roughly doubling rates beyond 200K tokens.

Caching and batch discounts have become standard, expected features rather than novelties — prompt caching delivering 85-90% savings and batch APIs delivering ~50% savings are now baseline tools every serious production system uses. FinOps-style practices (real-time monitoring, multi-vendor routing, plan-level caching) are emerging as a standard discipline specifically for agentic AI cost control, mirroring how cloud FinOps emerged once cloud spend became unpredictable at scale. On-premises GPU infrastructure has become competitive with cloud pricing specifically above ~65% utilization and ~100+ GPU scale, pushing larger enterprises toward hybrid cloud/on-prem/edge strategies.

---

## 20. Current Problems & Research

**Cost forecasting remains genuinely hard.** New features and new usage patterns make it difficult to predict token volume in advance, and usage spikes can blow through budgets before alerting catches up.

**Caching only works on exact prefix matches.** Agentic workflows where context shifts dynamically between calls (different tool outputs, different intermediate reasoning) often fail to get cache hits even when much of the underlying task structure is repeated — this is why plan-level caching (caching the structured task template, not the raw text) is an active area of optimization, reporting ~46% cost reduction in early production deployments.

**The cloud-vs-on-prem cost crossover is shifting.** As GPU prices and provider pricing both move, the utilization/scale threshold at which on-prem becomes cheaper than cloud is a moving target that enterprises have to continuously re-evaluate rather than decide once.

**Research direction: context compaction as a built-in API feature** (rather than a manual engineering task) is emerging, with newer chat APIs auto-summarizing conversation history to reduce token volume without developers having to build custom summarization pipelines themselves.

---

## 21. Future Evolution

Pricing is likely to shift gradually from pure per-token billing toward per-action or outcome-based pricing for specific agentic capabilities — charging for "task completed" rather than "tokens consumed," which is more aligned with the value delivered but harder to price fairly. Plan/task-level caching for agentic systems will likely mature beyond today's early ~46% savings as frameworks standardize how reusable task templates are identified and cached. Competitive pressure between providers is also expected to continue driving down baseline per-token prices for general-purpose capability, even as pricing for genuinely frontier reasoning capability stays premium. Context compaction, model routing, and budget governance will likely become built-in platform features rather than custom engineering work that every team has to build themselves.

---

## 22. Engineer Checklist

After studying this note, I should be able to:

[ ] Explain why output tokens cost more than input tokens

[ ] Explain why it exists (token pricing approximates real compute cost)

[ ] Explain alternatives (subscription pricing, on-prem, outcome-based pricing)

[ ] Use prompt caching in code (cache_control headers)

[ ] Use it in production (structure prompts for cache hits, monitor usage)

[ ] Discuss tradeoffs (caching vs batch vs model routing vs on-prem)

[ ] Answer interview questions about runaway-cost diagnosis

[ ] Recognize bottlenecks (unbounded history growth, cache misses, retry storms)

[ ] Optimize it (caching, batching, routing, compaction, output capping)

[ ] Connect it to larger systems (KV-cache, context windows, inference economics)

---

## 23. Knowledge Graph

```
Pricing & Cost-Control
├── Pricing Models
│   ├── Per-token (input vs output split)
│   ├── Context-aware tiered pricing
│   └── Subscription / outcome-based (emerging)
├── Cost-Reduction Levers
│   ├── Prompt Caching
│   │   ├── Explicit (cache_control headers — Anthropic)
│   │   └── Automatic (length-threshold — OpenAI)
│   ├── Batch API (50% discount, async)
│   ├── Model Routing / Cascading
│   └── Plan/Task-Level Caching (agentic)
├── Cost-Control Infrastructure
│   ├── Token Counters
│   ├── Budget Monitors / Alerts
│   └── FinOps Practices
└── Related Topics
    ├── KV-Cache (underlies prompt caching mechanics)
    ├── Context Windows (drives tiered pricing thresholds)
    └── Inference vs Training (inference = 85% of AI budget)
```

---

## 24. If You Remember Only 10 Things

1. LLM pricing is per-token, billed separately for input and output, with output costing 4-5x more because generation is sequential while input prefill is parallel.
2. Inference, not training, dominates AI spend — roughly 85% of enterprise AI budget and 80-90% of a model's lifecycle compute cost.
3. Prompt caching is the single highest-leverage cost optimization, delivering 85-90% savings by reusing computation for repeated prompt prefixes.
4. Caching only works on exact prefix matches — static/repeated content must be structured at the front of the prompt.
5. Batch APIs offer ~50% discounts for non-latency-sensitive workloads by letting providers schedule work into idle capacity.
6. Context-aware tiered pricing (higher rates beyond a context threshold) reflects real GPU memory constraints, not arbitrary markup.
7. Unbounded conversation history growth, sent fresh every turn, is the single most common cause of runaway production costs.
8. Model routing — sending easy queries to cheap models, hard queries to expensive ones — cuts cost dramatically with minimal quality loss.
9. On-prem GPU infrastructure becomes cost-competitive with cloud above roughly 65% utilization and 100+ GPU scale; below that, cloud's elasticity wins.
10. FinOps-style real-time budget monitoring is now a required discipline for production AI systems, not optional — costs can spike unpredictably and silently.