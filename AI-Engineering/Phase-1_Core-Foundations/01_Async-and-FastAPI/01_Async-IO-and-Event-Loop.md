---
title: "Async I/O & Event Loop"
phase: "Phase-1 — Core AI Foundations"
group: "01_Async-and-FastAPI"
tags: [ai-engineering, phase-1, study-notes]
status: empty
created: 2026-06-07
---
ee# Async-IO & Event Loop

**AI Engineering Knowledge Base · June 2026**

---

## Table of Contents

1. [The Core Problem](#1-the-core-problem)
2. [Evolution Timeline](#2-evolution-timeline)
3. [Vocabulary Map](#3-vocabulary-map)
4. [First-Principles Explanation](#4-first-principles-explanation)
5. [Basic Architecture](#5-basic-architecture)
6. [Intermediate Architecture](#6-intermediate-architecture)
7. [Advanced Production Architecture](#7-advanced-production-architecture)
8. [Internal Working — Data Flow Trace](#8-internal-working--data-flow-trace)
9. [Component Deep Dive](#9-component-deep-dive)
10. [Design Decisions](#10-design-decisions)
11. [Alternatives and Competing Approaches](#11-alternatives-and-competing-approaches)
12. [Failure Modes](#12-failure-modes)
13. [Optimization Techniques](#13-optimization-techniques)
14. [Production Reality](#14-production-reality)
15. [Topic Connections](#15-topic-connections)
16. [Current Industry State (2025–2026)](#16-current-industry-state-20252026)
17. [Current Problems (Unsolved)](#17-current-problems-unsolved)
18. [Future Evolution](#18-future-evolution)
19. [Engineer's Mental Model — If You Remember Only 10 Things](#19-engineers-mental-model--if-you-remember-only-10-things)
20. [Knowledge Graph](#20-knowledge-graph)

---

## 1. The Core Problem

Imagine you're building an AI agent that calls GPT-4 for reasoning, then queries a vector DB for memory, then hits a SQL DB to log the result — all for one user request. Each I/O call takes ~200–800ms. If you process them one at a time, a single agent turn takes 2+ seconds. If 100 users hit you at once, your server is staring at the ceiling waiting for HTTP responses 98% of the time.

> **The Insight:** Waiting is not working. Traditional synchronous code blocks the entire thread during a network call. The CPU sits idle. This is the core waste async I/O fixes.

The original problem: Python's threading model has the **GIL** (Global Interpreter Lock — a mutex that prevents multiple threads from executing Python bytecode simultaneously). You can't use OS threads to parallelize I/O-heavy Python without fighting the GIL and paying high thread-overhead costs (each thread ≈ 8MB RAM).

**What breaks without async I/O:**

- A server handling 1,000 concurrent LLM API calls needs 1,000 threads — that's 8GB RAM just for thread stacks
- Thread context switching overhead degrades latency under load
- Race conditions when shared state is mutated across threads
- AI agents that poll for results waste CPU time checking repeatedly instead of being notified

> **The Shift:** Instead of "block and wait," async I/O says: "when you'd normally wait, tell the event loop to wake you up when the data is ready. Go do something else in the meantime." This is cooperative multitasking in a single thread.

---

## 2. Evolution Timeline

```
Pre-2000s — Blocking I/O
  Synchronous code: one request, one thread.
  Fine for desktop apps. Terrible for servers under load.
  ↓
2000s — OS Threads
  Thread-per-request model. Works until you hit the C10K problem
  (10,000 concurrent connections). Thread memory overhead kills servers.
  ↓
2006 — Callback Hell (Node.js/Twisted)
  Non-blocking I/O via callbacks. Logic was correct but code looked
  like a pyramid of doom. Deeply nested callbacks were unmaintainable.
  ↓
2012–2014 — Python generators + yield from
  Tulip project (what became asyncio). Generators could be
  paused/resumed. yield from let you compose them. Still not clean.
  ↓
2015 — Python 3.5: async/await (PEP 492)
  Native coroutine syntax. async def + await made async code look
  like sync code. This was the breakthrough moment for readability.
  ↓
2016 — uvloop
  Drop-in replacement for asyncio's event loop, built on libuv
  (same engine as Node.js). 2–5× faster. Zero code changes needed.
  ↓
2019–2021 — Production maturity
  FastAPI, HTTPX, asyncpg, aiobotocore — the async ecosystem grew.
  LLM API clients started shipping async variants. Patterns solidified.
  ↓
2022–2023 — Task Groups (Python 3.11)
  Structured concurrency (borrowed from Trio/Kotlin). Task Groups
  guarantee child tasks don't outlive their scope. Errors propagate
  cleanly. No more "orphaned tasks."
  ↓
2025–2026 — EDA + Agentic AI (Current State of the Art)
  Event-Driven Architecture becomes the standard for AI agents.
  AnyIO 4.11 adds subinterpreter support.
  Free-threaded Python 3.14 experiments with GIL removal.
  ↓
Future Direction
  Structured concurrency as default. Free-threaded CPython maturity.
  Subinterpreter parallelism. EDA replacing all polling in agentic AI.
```

> **Why each transition happened:** Every transition was forced by a scaling limit — threads ran out of memory → callbacks became unmaintainable → generators were hard to compose → async/await unified everything under readable syntax → structured concurrency fixed reliability → EDA eliminated the last polling overhead.

---

## 3. Vocabulary Map

| Term                       | Meaning + Why it exists                                                                                                                                                                | Aliases                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| **Event Loop**             | The scheduler that runs async tasks, watches file descriptors, fires callbacks, and manages timers. It's the "operating system" inside your process. Everything async goes through it. | loop, run loop, reactor                              |
| **Coroutine**              | A function defined with `async def` that can be suspended (at `await` points) and resumed. Not a thread — runs in a single thread, pauses cooperatively.                               | coro, async function                                 |
| **Task**                   | A coroutine scheduled to run on the event loop. `asyncio.create_task()` wraps a coroutine in a Task. Tasks can run concurrently; coroutines alone cannot.                              | asyncio.Task, future                                 |
| **Awaitable**              | Anything you can put after `await`: coroutines, Tasks, Futures. The event loop knows how to suspend/resume these.                                                                      | —                                                    |
| **Future**                 | A low-level placeholder for a result that isn't ready yet. Like a Promise in JavaScript. Tasks are Futures under the hood.                                                             | Promise (JS), deferred                               |
| **GIL**                    | Global Interpreter Lock — CPython's mutex preventing true thread parallelism for CPU work. Async I/O sidesteps it because you're not CPU-bound; you're I/O-bound.                      | Global Interpreter Lock                              |
| **Structured Concurrency** | A discipline where tasks are created inside scopes (Task Groups / Nurseries). Child tasks cannot outlive their scope. Errors propagate cleanly. Prevents task leaks.                   | Task Groups, Nursery (Trio), scope-based concurrency |
| **Backpressure**           | A mechanism to slow down producers when consumers can't keep up. Without it, queues grow unbounded and memory explodes. Implemented via `Queue(maxsize)` + `Semaphore`.                | flow control, rate limiting                          |
| **uvloop**                 | Drop-in replacement for asyncio's event loop, written in Cython on top of libuv (C library). 2–5× faster due to fewer Python object allocations in the hot path.                       | —                                                    |
| **EDA**                    | Event-Driven Architecture — design where components emit events and others react to them. Eliminates polling. Central to agentic AI systems.                                           | event-driven, pub-sub architecture                   |
| **Semaphore**              | A counter that limits concurrency. `asyncio.Semaphore(10)` means at most 10 coroutines can hold the semaphore simultaneously. Used to cap outbound API calls.                          | concurrency limiter                                  |
| **to_thread()**            | `asyncio.to_thread(blocking_fn)` — runs a sync/blocking function in a thread pool executor so it doesn't block the event loop. Essential for CPU-bound work inside async code.         | run_in_executor, thread offloading                   |
| **AnyIO**                  | Compatibility layer that lets you write one async codebase that runs on asyncio or Trio backends. Adds structured concurrency primitives to both.                                      | —                                                    |
| **gather()**               | `asyncio.gather(*coros)` — runs multiple coroutines concurrently and waits for all. Equivalent to Promise.all() in JavaScript.                                                         | fan-out, parallel await                              |
| **Nursery**                | Trio's term for Task Groups. A scope where child tasks are created; the scope doesn't exit until all children finish or one fails.                                                     | Task Group (Python 3.11+)                            |
| **Free-threading**         | Python 3.14 experimental mode (PEP 703) that removes the GIL. Allows true parallelism for CPU work. Currently 10–15% slower for single-threaded code due to atomic reference counting. | no-GIL Python, PEP 703                               |
| **I/O-bound**              | Work where most time is spent waiting for I/O (network, disk). Async I/O excels here. Contrast with CPU-bound (compute-heavy), where multiprocessing or free-threading is better.      | network-bound                                        |

---

## 4. First-Principles Explanation

A CPU executes instructions at ~3GHz. A network call to an LLM API takes ~300ms. That's 900,000,000 CPU cycles spent doing nothing while waiting for a response. This is the fundamental mismatch async I/O addresses.

The OS already handles async I/O at the system level: `epoll` (Linux), `kqueue` (macOS), `IOCP` (Windows). These syscalls let you say "tell me when any of these 10,000 file descriptors has data" and block once instead of polling each. The event loop is Python's interface to these OS primitives.

> **Mental Model:** Think of the event loop as a restaurant manager and coroutines as waiters. A waiter takes an order (starts a request), hands it to the kitchen (sends the I/O), and immediately starts serving another table instead of standing at the kitchen window. When the kitchen rings a bell (data ready), the waiter returns to that table.

**Why it's needed:** AI workloads are almost always I/O-dominated. Calling GPT-4 takes 500ms. Querying Pinecone takes 20ms. Reading from Postgres takes 5ms. During all that time, your CPU is free. Async I/O lets you serve 1,000 concurrent requests with a single thread, using ~1MB RAM per connection instead of 8MB per thread.

**What would happen without it:** Every LLM-powered product would need massive thread pools or process pools. Memory usage would be orders of magnitude higher. At 10k concurrent users, a thread-per-request server would need 80GB RAM just for thread stacks. With async I/O, the same workload fits in ~1GB.

---

## 5. Basic Architecture

```
Your Code
    │
    ├── async def main():
    │       result = await fetch_llm()   ← suspends here
    │       result2 = await query_db()   ← suspends here
    │
    ▼
┌─────────────────────────────────┐
│         Event Loop              │
│                                 │
│  Ready Queue  │  I/O Watchers   │
│  [task_A]     │  [sock_1→wake_A]│
│  [task_B]     │  [sock_2→wake_B]│
│               │                 │
│  1. Run task until await        │
│  2. Register I/O watcher        │
│  3. Pick next ready task        │
│  4. When I/O ready → wake task  │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────┐
│   OS Kernel     │
│  epoll/kqueue   │  ← actual async I/O at syscall level
└─────────────────┘
```

**Every component explained:**

- **Coroutine** — `async def` function. Defines the logic. Not running until scheduled.
- **Task** — a coroutine wrapped by the event loop. Has a state: pending, running, done, cancelled.
- **Ready Queue** — tasks that have data available and are ready to resume. The loop processes these in order.
- **I/O Watchers** — mappings from file descriptor → task to wake when that FD has data. Registered on `await`.
- **OS epoll/kqueue** — the actual kernel mechanism. The loop calls `select()` or `epoll_wait()` with a timeout to ask the OS: "any of these FDs ready?"

```python
import asyncio

async def fetch_llm(prompt: str) -> str:
    # simulates an LLM API call
    await asyncio.sleep(0.3)  # yields control back to loop
    return f"Response to: {prompt}"

async def main():
    # Sequential — 0.6s total
    r1 = await fetch_llm("question 1")
    r2 = await fetch_llm("question 2")
    
    # Concurrent — 0.3s total (both run at same time)
    r1, r2 = await asyncio.gather(
        fetch_llm("question 1"),
        fetch_llm("question 2")
    )

asyncio.run(main())
```

---

## 6. Intermediate Architecture

Real AI services add three layers beyond the basic loop: concurrency control, error isolation, and background tasks.

```
Request In
    │
    ▼
┌──────────────────────────────────────┐
│           FastAPI / ASGI             │  ← async web framework
└──────────────┬───────────────────────┘
               │
    ▼
┌──────────────────────────────────────┐
│         Semaphore(max=10)            │  ← limits concurrent LLM calls
│  so you don't get rate-limited       │
└──────────────┬───────────────────────┘
               │
    ▼
┌──────────────────────────────────────┐
│         Task Group                   │  ← structured concurrency
│  ┌─────────┐  ┌─────────┐           │
│  │LLM call │  │DB query │  (parallel)│
│  └────┬────┘  └────┬────┘           │
│       └─────┬──────┘                │
└─────────────┼────────────────────────┘
              │
    ▼
┌──────────────────────────────────────┐
│         Result Aggregation           │
└──────────────────────────────────────┘
              │
    ▼
Response Out
```

**Why each component was added:**

- **Semaphore** — without it, 1,000 simultaneous users trigger 1,000 LLM API calls at once, hitting rate limits and memory limits. Semaphore caps active concurrent calls at a safe number.
- **Task Group** — replaces scattered `create_task()` calls. If the DB query fails, the LLM call is automatically cancelled. Errors don't silently vanish.
- **ASGI framework** — interfaces the OS-level async socket accept loop with your Python async handlers. FastAPI/Starlette run on uvicorn which runs on asyncio (or uvloop).

```python
import asyncio
from asyncio import TaskGroup

sem = asyncio.Semaphore(10)  # max 10 concurrent LLM calls

async def safe_llm_call(prompt: str) -> str:
    async with sem:             # blocks if 10 already in flight
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.openai.com/v1/...", ...)
            return resp.json()["choices"][0]["message"]["content"]

async def handle_request(user_query: str):
    async with TaskGroup() as tg:  # Python 3.11+
        llm_task = tg.create_task(safe_llm_call(user_query))
        db_task  = tg.create_task(fetch_context_from_db(user_query))
    # Both done here. If either raised, both are cancelled and error propagates.
    return combine(llm_task.result(), db_task.result())
```

---

## 7. Advanced Production Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Load Balancer (nginx)                   │
└───────────┬─────────────────────────────────────────────┘
            │  (10k concurrent connections)
┌───────────▼─────────────────────────────────────────────┐
│          uvicorn workers  (uvloop backend)               │
│  worker-1       worker-2       worker-3                  │
│  [event loop]   [event loop]   [event loop]              │
└───────────┬─────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────┐
│               Message Queue (Redis Streams)             │  ← backpressure
│  producer → Queue(maxsize=1000) → consumer pool        │
└───────────┬────────────────────────────────────────────┘
            │
   ┌────────┴─────────┬──────────────┬──────────────┐
   ▼                  ▼              ▼               ▼
[LLM API]        [Vector DB]    [SQL async]   [Object Store]
AsyncOpenAI      asyncpg+pgvec  asyncpg       aiobotocore
Semaphore(20)    Semaphore(50)  Pool(10)      Semaphore(30)
   │                  │              │               │
   └──────────────────┴──────────────┴───────────────┘
                       │
            ┌──────────▼──────────┐
            │  Structured Logging │  ← OpenTelemetry traces
            │  + Metrics          │
            └─────────────────────┘
```

**Design decisions at this scale:**

- **Multiple uvicorn workers** — each is a separate OS process with its own event loop, bypassing the GIL for true parallelism across CPU cores. Don't use threads; use processes.
- **uvloop** — installed as a one-liner: `uvicorn app:app --loop uvloop`. 2–5× throughput improvement for free.
- **Redis Streams + Queue(maxsize)** — backpressure at two levels: in-process queue caps memory; Redis provides cross-process backpressure and durability.
- **Per-downstream Semaphores** — each external service gets its own semaphore sized to its rate limit. LLM APIs allow fewer concurrent calls than your DB connection pool.
- **asyncpg connection pool** — unlike synchronous psycopg2, asyncpg is async-native. Pool size = expected concurrent DB queries, not threads.
- **OpenTelemetry traces** — each async task gets a trace span. You can see exactly where latency comes from: LLM? DB? Queue wait?

---

## 8. Internal Working — Data Flow Trace

Trace a single LLM API call through the event loop, step by step:

```
1. asyncio.run(main())
   → creates new event loop
   → schedules main() as Task-0
   → starts loop iteration

2. Loop iteration 1:
   → dequeues Task-0 from ready queue
   → resumes Task-0 at top of main()
   → Task-0 hits: await httpx.get("https://api.openai.com/...")
   → httpx creates socket, calls connect()
   → registers socket fd=7 → "wake Task-0 when writable"
   → Task-0 suspends (returns control to loop)

3. Loop iteration 2:
   → ready queue empty
   → calls epoll_wait(timeout=Inf) — blocks OS thread

4. OS: network stack completes TCP handshake
   → fd=7 becomes writable
   → epoll_wait() returns with [fd=7]

5. Loop iteration 3:
   → fd=7 maps to Task-0 → moves Task-0 to ready queue
   → dequeues Task-0
   → Task-0 resumes inside httpx: writes HTTP request to socket
   → hits await again: waiting for response
   → registers fd=7 → "wake Task-0 when readable"
   → Task-0 suspends again

6. ... (TCP round trip, ~200–500ms passes)

7. OS: response data arrives on fd=7
   → epoll_wait() returns with [fd=7 readable]
   → Task-0 moves to ready queue
   → Task-0 resumes, reads response bytes
   → httpx parses HTTP, returns Response object
   → await resolves with the response

8. Task-0 continues:
   result = response.json()
   print(result)
   → Task-0 finishes, loop finds no more tasks
   → asyncio.run() returns
```

> **Key Insight:** The OS thread never blocks for the 200–500ms round trip. During that gap, other tasks (Task-1, Task-2 etc.) would have been running in the same thread.

---

## 9. Component Deep Dive

### Event Loop

- **Purpose:** Schedule coroutines, manage I/O callbacks, run timers
- **Input:** Registered tasks, I/O events from OS, scheduled callbacks
- **Output:** Resumed coroutines with data, fired callbacks
- **Mechanism:** Single-threaded "select loop" — processes ready queue, calls `epoll_wait` with a timeout equal to the next scheduled timer, wakes FDs, repeats
- **Failure cases:** Any CPU-bound code called directly in a coroutine blocks the entire loop. Every other coroutine freezes. Fix: `asyncio.to_thread()`

### Task

- **Purpose:** Give coroutines independent lifetimes so they can run concurrently
- **Input:** A coroutine object
- **Output:** A Future-like object; call `.result()` to get the return value
- **Mechanism:** Wraps coroutine, schedules it on the loop, stores result/exception when done
- **Failure cases:** Tasks are held by weak references in the loop. If you don't store the task object, the GC may destroy it mid-run ("task vanishing"). Always assign `task = asyncio.create_task(...)` or add to a set.

### Semaphore

- **Purpose:** Cap concurrent operations to avoid rate-limiting or resource exhaustion
- **Input:** Maximum integer count
- **Output:** Context manager that blocks until a slot is available
- **Mechanism:** Internal counter; `acquire()` decrements (waits if 0); `release()` increments and wakes next waiter
- **Failure cases:** Forgetting to release — always use `async with`; setting max too high defeats the purpose

### Task Group (Python 3.11+)

- **Purpose:** Structured concurrency — guarantee no child task outlives its scope
- **Input:** Coroutines added via `tg.create_task()`
- **Output:** All tasks complete (or all cancelled) before exiting `async with` block
- **Mechanism:** Tracks child tasks; if one raises, cancels all others, collects exceptions into `ExceptionGroup`
- **Failure cases:** Python 3.10 and earlier don't have this — use AnyIO's `create_task_group()` for portability

### asyncio.Queue

- **Purpose:** Producer-consumer coordination with optional backpressure
- **Input:** Items from producer coroutines; `maxsize` parameter
- **Output:** Items to consumer coroutines
- **Mechanism:** FIFO deque; `put()` awaits if full (`maxsize > 0`); `get()` awaits if empty
- **Failure cases:** `maxsize=0` means unbounded — queue grows to fill all RAM if consumers are slower than producers

---

## 10. Design Decisions

### Why single-threaded event loop vs thread pool?

No race conditions on shared state. No lock overhead. Lower memory. Cooperative scheduling is explicit — you know exactly where context switches happen (at every `await`). Thread switches are preemptive and unpredictable. For I/O-bound AI workloads, single-threaded async outperforms thread pools both in throughput and latency.

### Why cooperative (not preemptive) scheduling?

You yield control explicitly at `await`. This means: if you never yield, you block the loop. But it also means: between yield points, your data is safe — no other coroutine runs. This eliminates most race conditions that make multithreading hard.

> **Trade-off:** Cooperative scheduling means a misbehaving coroutine (doing CPU work without awaiting) can freeze the entire server. You must be disciplined: any blocking call must use `asyncio.to_thread()`.

### Why Task Groups over create_task()?

With raw `create_task()`, if Task-A fails, Task-B keeps running orphaned. You might not notice Task-B's result is now meaningless. Task Groups are a contract: all tasks in the group live and die together. This matches how you reason about operations — "get LLM result AND DB context; if either fails, the whole operation fails."

### Why asyncio over Trio?

asyncio is in the stdlib — no extra dependencies. The entire async ecosystem (FastAPI, httpx, asyncpg, openai SDK) targets asyncio. Trio is architecturally cleaner (nurseries are more principled than Task Groups) but requires library authors to support it, which most haven't. AnyIO bridges both.

### Why backpressure matters for LLM systems?

LLM API calls are slow (100–2000ms) and expensive. If you fire 10,000 concurrent requests, you burn rate limits, explode memory with pending tasks, and trigger cascading failures. A `Semaphore(20)` caps concurrent calls; a `Queue(maxsize=1000)` stops accepting new work when the backlog is full — giving upstream a chance to slow down.

---

## 11. Alternatives and Competing Approaches

|Approach|Pros|Cons|Best for|
|---|---|---|---|
|**asyncio (Python)**|stdlib, massive ecosystem, readable async/await|GIL blocks CPU tasks; older patterns use create_task unsafely|I/O-bound AI workloads — default choice|
|**Trio**|Strictest structured concurrency, no orphaned tasks ever|Not stdlib, limited ecosystem support|Greenfield projects where correctness > ecosystem|
|**Threading**|Shared memory, familiar API, good for blocking libs|GIL contention, race conditions, 8MB/thread|Wrapping sync C extensions|
|**Multiprocessing**|True CPU parallelism, no GIL issues|High IPC overhead, shared state requires queues|CPU-bound ML work (inference, training)|
|**Node.js**|Lower latency for pure I/O, V8 JIT|No ML ecosystem, can't call PyTorch natively|Pure I/O microservices without ML|
|**Go goroutines**|M:N threading, no GIL, built-in channels|Small AI/ML library set|Infrastructure services adjacent to AI|

> **Rule of thumb:** I/O-bound AI workloads → asyncio. CPU-bound ML → multiprocessing or offload to a GPU server and make async calls to it. Mixed → async for I/O coordination + `to_thread()` for CPU bursts.

---

## 12. Failure Modes

### 1. Blocking the event loop (most common)

**Symptom:** All requests freeze for seconds. CPU usage spikes. Loop latency explodes.

**Cause:** CPU-bound code called directly in a coroutine — running a regex on a 10MB document, computing embeddings in-process, JSON parsing a huge payload.

**Fix:** `await asyncio.to_thread(blocking_fn, args)` or offload to a worker process.

### 2. Task vanishing (silent failure)

**Cause:** The event loop holds only a weak reference to tasks. If you write `asyncio.create_task(coro())` without saving the return value, the GC may destroy it mid-execution. The task silently disappears with no error.

**Fix:** Always save tasks: `task = asyncio.create_task(...)` or add to a persistent set and remove on completion.

### 3. Exception deadlocks

**Cause:** With raw `gather()`, if one coroutine raises, the exception is stored but not immediately propagated. Other coroutines keep running. You only see the error when you `await gather()`. If you never await it — you never see the error.

**Fix:** Use Task Groups — exceptions propagate immediately and cancel siblings.

### 4. Unbounded queue growth

**Cause:** Producer sends work faster than consumer processes it. `Queue(maxsize=0)` (unbounded default) just accumulates items until OOM.

**Fix:** Always set `maxsize`; handle `QueueFull` with backpressure to upstream.

### 5. Cancellation cleanup failures

**Cause:** When a Task is cancelled, a `CancelledError` is raised at the current `await` point. If you catch it and don't re-raise, the task appears to keep running but is in an inconsistent state.

**Fix:** Never `except CancelledError: pass`. Do cleanup and re-raise, or use `asyncio.shield()` for critical cleanup sections.

### 6. Sync library in async context

**Cause:** Using `requests.get()` inside a coroutine blocks the event loop for the entire HTTP round trip. Every other task freezes.

**Fix:** Use `httpx` (has async client), or wrap with `asyncio.to_thread(requests.get, url)`.

---

## 13. Optimization Techniques

### Latency

- **uvloop** — `uvloop.install()` before `asyncio.run()`. 2–5× lower latency at no code cost.
- **Connection pooling** — don't create a new HTTPX client per request. One shared `AsyncClient` with connection pool reuses TCP connections. Eliminates TCP handshake overhead per call.
- **Streaming responses** — for LLM streaming, use `async for chunk in stream:` rather than awaiting the full response. First token arrives faster (time-to-first-token).

### Throughput / Scalability

- **Batch gather()** — instead of 100 sequential awaits, fan out with `asyncio.gather()` and process all 100 concurrently (within Semaphore limits).
- **Multiple event loop processes** — `uvicorn --workers 4` runs 4 independent Python processes, each with its own event loop. Saturates all CPU cores.
- **Chunked Task Groups** — split large job lists into chunks of N; process each chunk as a Task Group; move to next chunk when done. Avoids spawning 10,000 tasks simultaneously.

### Memory

- **Bounded queues** — `asyncio.Queue(maxsize=N)` caps memory usage from backlog.
- **Async generators** — for large result sets, use `async for row in db.cursor():` instead of loading all rows at once.

### Cost (for LLM workloads)

- **Semaphore sizing** — set per-provider rate limit. Prevents wasted retries from 429 errors.
- **Circuit breaker pattern** — if LLM provider fails 5 times in 60s, stop sending for 30s. Implemented as an async state machine. Prevents burning tokens on a failing endpoint.

---

## 14. Production Reality

|Company|Usage|
|---|---|
|**OpenAI**|Ships `AsyncOpenAI` client. Recommends `asyncio.gather()` for bulk parallel completion calls. Their Python SDK is async-first for production usage.|
|**Anthropic**|Claude Code SDK uses event-driven async stream processing. Non-blocking I/O throughout. Async streaming lets clients receive tokens as they're generated without blocking.|
|**AWS/Amazon**|Lambda auto-scales on event volume via EDA. EDA eliminates idle resources — functions only run when events fire, not polling. Standard for serverless AI on AWS.|
|**NVIDIA**|I/O-dedicated threads + double-buffering for deep learning data pipelines. Async I/O ensures the GPU is never starved waiting for data from storage.|
|**AI Startups**|EDA patterns for agentic AI report 70–90% latency reduction vs polling. Central event bus (Kafka/Redis Streams) lets agents react immediately to data changes.|

> **The Standard Stack:** uvicorn (ASGI) + uvloop + FastAPI + AsyncOpenAI + asyncpg + redis-py async. This combination handles ~100k requests/second on modern hardware. All major AI API providers now ship async client libraries as the primary interface.

---

## 15. Topic Connections

```
Async I/O + Event Loop
│
├── LLMs & Inference
│   ├── Async streaming: tokens arrive async; stream to client without blocking
│   ├── Parallel inference: fan out to multiple models simultaneously
│   └── Rate limit management: Semaphore per model provider
│
├── RAG (Retrieval-Augmented Generation)
│   ├── Parallel retrieval: embed query + search vector DB + filter SQL — all concurrent
│   └── Streaming RAG: stream LLM response while context is still being fetched
│
├── Agents & Multi-Agent Systems
│   ├── EDA: agents subscribe to events, react without polling
│   ├── Tool calls: each tool call is an async I/O operation
│   └── Parallel tool execution: multiple tool calls in a Task Group
│
├── Vector Databases
│   ├── asyncpg + pgvector: async Postgres queries with vector similarity
│   └── Async clients: Pinecone, Weaviate, Qdrant all have async Python clients
│
├── Memory Systems
│   ├── Async reads from memory store during agent step
│   └── Background async writes: log memory without blocking main flow
│
├── Embeddings
│   ├── Batch embed: send 100 texts to embedding API concurrently via gather()
│   └── Async embed + store: pipeline embed → insert to vector DB async
│
├── Fine-tuning & Training
│   ├── Async data loading: I/O threads feed GPU without stalling compute
│   └── Double-buffering: NVIDIA pattern for async data pipeline to GPU
│
└── Evaluation & Monitoring
    ├── Parallel eval runs: test N prompts concurrently with gather()
    └── Async metrics: emit OpenTelemetry spans without blocking inference
```

> **Core dependency:** Async I/O is the connective tissue of the AI engineering stack. Every component that does network I/O — LLM calls, embedding APIs, vector DB queries, SQL reads, cache hits — becomes 10–100× more efficient when async. It's not optional at production scale; it's the default assumption.

---

## 16. Current Industry State (2025–2026)

### What is considered best practice today:

- asyncio + async/await is the universal standard for I/O-bound Python AI services — not a trend, it's baseline
- Task Groups (Python 3.11+) are replacing ad-hoc `create_task()` in new code
- uvloop is the default event loop for production servers — 2–5× performance improvement with zero code changes
- `Semaphore` + `Queue(maxsize)` for backpressure — required in any system touching rate-limited APIs
- AnyIO for library authors — write once, run on asyncio or Trio
- EDA (event-driven architecture) for agent orchestration, especially multi-agent systems

### What is changing:

- Structured concurrency becoming the default mental model — Task Groups preferred over raw `gather()`
- Free-threaded Python 3.14 is being watched carefully — still 10–15% slower but removes the GIL ceiling
- Agentic AI driving EDA adoption — polling-based agents being replaced by event-reactive ones

### What companies are moving toward:

- Async-first API clients (all major LLM providers now ship async Python SDKs)
- Subinterpreter parallelism (AnyIO 4.11) as a potential GIL bypass within one process
- 100k RPS patterns with uvloop + asyncio becoming feasible for mid-size companies

---

## 17. Current Problems (Unsolved)

### 1. Debugging async code is hard

Stack traces in async code are often incomplete — they show the current frame but not the chain of coroutines that led there. `asyncio.get_event_loop().set_debug(True)` helps but adds overhead. Python 3.12+ improved async stack frame support but it's not solved.

### 2. Cancellation semantics are complex

`CancelledError` must be re-raised but also needs to allow cleanup. The boundary between "cancel and clean up" vs "cancel and stop immediately" is subtle. Structured concurrency helps but doesn't eliminate the complexity for custom resource management.

### 3. Mixing sync and async libraries

Many useful ML/data libraries (older transformers internals, some database drivers) are synchronous. Wrapping everything with `to_thread()` works but adds thread pool overhead and makes profiling harder. There's no clean universal solution.

### 4. Free-threading regression

Python 3.14's free-threaded mode removes the GIL but currently causes 10–15% single-threaded slowdown due to atomic reference counting overhead on every object. The CPython team is working on biased reference counting to mitigate this.

### 5. Subinterpreter shared state

Subinterpreters (separate Python runtimes in one process, without GIL) can't easily share Python objects. Libraries like NumPy need work to support cross-interpreter sharing. AnyIO 4.11 adds the infrastructure, but ecosystem support is early.

---

## 18. Future Evolution

### 3–5 year outlook:

- **Structured concurrency as default** — Task Groups / nurseries will be how everyone writes concurrent Python, not just async veterans. Tutorials will start with Task Groups, not `create_task()`.
- **Free-threaded Python maturity** — by Python 3.16–3.17, the 10–15% overhead may drop to <5%. This would let CPU-bound asyncio code finally bypass the GIL without multiprocessing.
- **Subinterpreter parallelism** — multiple Python runtimes in one process, communicating via message passing. Could give true parallelism without the forking overhead of multiprocessing. Still experimental.
- **EDA as the standard for agentic AI** — polling-based agent loops will be replaced by event-reactive agents. Kafka/Redis Streams will be standard agent infrastructure, not specialized choices.
- **Async-native ML libraries** — expect transformers, torch serving, and embedding libraries to gain async interfaces as the AI serving layer becomes fully async.

> **What probably won't change:** The event loop + coroutine model is deeply baked into Python's ecosystem. Even if free-threading removes the GIL, async/await will remain the dominant pattern for I/O-bound code because it makes concurrency explicit and composable.

---

## 19. Engineer's Mental Model — If You Remember Only 10 Things

1. **The event loop is a single-threaded scheduler.** It runs one coroutine at a time, switching only at `await` points. No await = no yield = blocked loop.
    
2. **A coroutine is just a function that can pause. A Task is that coroutine scheduled to run concurrently with others.** You need `create_task()` to get actual concurrency — awaiting a coroutine directly is still sequential.
    
3. **CPU-bound work blocks the loop.** Any compute (regex on large text, in-process inference, heavy JSON parsing) must be moved to `asyncio.to_thread()`. This is the #1 production mistake.
    
4. **Always save your Task reference.** `asyncio.create_task(coro())` without saving the result → garbage collector may kill the task silently mid-run.
    
5. **Use Task Groups (Python 3.11+), not raw create_task().** They guarantee child tasks can't outlive their scope and errors propagate cleanly.
    
6. **Backpressure is not optional.** Use `Semaphore(N)` to cap concurrent LLM API calls. Use `Queue(maxsize=N)` to cap work backlog. Unbounded = OOM and rate-limit explosions.
    
7. **uvloop is a free 2–5× speedup.** One line: `uvloop.install()`. Use it in every production service.
    
8. **`asyncio.gather()` runs coroutines concurrently but exceptions don't cancel siblings. Task Group does.** Use gather() only when you want independent tasks that can fail independently.
    
9. **EDA > polling for agents.** An agent that reacts to events instead of polling every N seconds is 70–90% lower latency and uses fewer resources. This is where agentic AI is moving.
    
10. **asyncio is for I/O-bound work.** For true CPU parallelism, you still need multiprocessing (or free-threaded Python 3.14+ when it matures).
    

---

## 20. Knowledge Graph

```
Async I/O & Event Loop
│
├── Core Primitives
│   ├── Event Loop (asyncio/uvloop)
│   │   ├── epoll/kqueue (OS syscall layer)
│   │   ├── Ready Queue (runnable tasks)
│   │   └── I/O Watcher Registry (fd → task mapping)
│   ├── Coroutine (async def / await)
│   ├── Task (scheduled coroutine)
│   └── Future (result placeholder)
│
├── Concurrency Control
│   ├── Structured Concurrency
│   │   ├── Task Group (Python 3.11+)
│   │   ├── Nursery (Trio)
│   │   └── AnyIO TaskGroup (portable)
│   ├── asyncio.gather() (fan-out, no structure)
│   ├── Semaphore (cap concurrent ops)
│   └── Queue(maxsize) (backpressure)
│
├── Integration Patterns
│   ├── to_thread() (sync→async bridge)
│   ├── asyncio.shield() (cancellation protection)
│   └── Async generators (streaming results)
│
├── Performance Layer
│   ├── uvloop (2–5× faster event loop)
│   ├── Connection pools (httpx, asyncpg)
│   └── Streaming responses (TTFT optimization)
│
├── Architecture Patterns
│   ├── EDA (Event-Driven Architecture)
│   │   ├── Redis Streams
│   │   ├── Kafka
│   │   └── AWS Lambda + EventBridge
│   └── ASGI Stack
│       ├── uvicorn (server)
│       ├── FastAPI (framework)
│       └── Multiple workers (process-level parallelism)
│
├── Failure Modes
│   ├── Loop blocking (CPU in coroutine)
│   ├── Task vanishing (weak refs + GC)
│   ├── Exception deadlock (unraised errors)
│   ├── Unbounded queue (OOM)
│   └── Cancellation mishandling
│
├── Alternatives
│   ├── Trio (stricter, not stdlib)
│   ├── Threading (GIL-limited)
│   ├── Multiprocessing (CPU parallelism)
│   └── Node.js (I/O fast, no ML)
│
├── Future Directions
│   ├── Free-threaded Python (PEP 703)
│   ├── Subinterpreters (AnyIO 4.11+)
│   └── Structured concurrency as default
│
└── AI Engineering Connections
    ├── LLM APIs → async clients (AsyncOpenAI)
    ├── RAG → parallel retrieval (gather)
    ├── Agents → EDA, async tool calls
    ├── Vector DBs → async query clients
    ├── Embeddings → batch gather()
    ├── Serving → uvicorn + uvloop
    └── Evaluation → parallel test runs
```

---

_AI Engineering Knowledge Base · Async-IO & Event Loop · June 2026_