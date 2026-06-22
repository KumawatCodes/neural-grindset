
# Context Window

The context window (or context length) is the maximum number of tokens a language model can process in a single forward pass. For generative models, this includes **both** the input prompt and the generated response – once the generated tokens reach the limit, the model must stop or truncate the conversation history.

## Why It Matters

- **Long‑form reasoning** – Reads entire documents, books, or codebases in one go.
- **In‑context learning** – More examples in the prompt improve performance (few‑shot learning).
- **Conversational memory** – Chatbots can retain longer dialogue history without forgetting.
- **RAG vs. Long‑Context** – Deciding whether to retrieve (RAG) or just stuff everything into the prompt.

## Attention Complexity: The Bottleneck

In standard Transformer self‑attention, the computational and memory complexity scales **quadratically** with sequence length:

Complexity = O(n² × d)


| Sequence Length (n) | Attention Pairs (n²) | Relative Cost |
|---------------------|----------------------|---------------|
| 512 (BERT)          | 262k                 | 1×            |
| 4,096 (GPT‑3.5)     | 16.8M                | 64×           |
| 32,768              | 1.07B                | 4,096×        |
| 128,000 (GPT‑4 Turbo) | 16.4B              | 62,500×       |
| 1,000,000 (Gemini)  | 1.0T                 | 3.8M×         |

> Doubling the context length **quadruples** the FLOPs and memory required.

## Evolution of Context Windows

| Model Family        | Context Window (tokens) | Year | Notable Technique                         |
|---------------------|-------------------------|------|-------------------------------------------|
| BERT                | 512                     | 2018 | Fixed absolute position                   |
| GPT‑2               | 1,024                   | 2019 | Absolute positional encoding              |
| GPT‑3               | 2,048                   | 2020 | Dense attention                           |
| Llama 1             | 2,048                   | 2023 | RoPE (Rotary Positional Embedding)        |
| GPT‑3.5             | 4,096                   | 2022 | –                                         |
| Claude 2            | 100,000                 | 2023 | –                                         |
| GPT‑4 (8K/32K)      | 8,192 / 32,768          | 2023 | –                                         |
| Llama 2             | 4,096                   | 2023 | RoPE                                      |
| GPT‑4 Turbo         | 128,000                 | 2023 | FlashAttention, grouped‑query attention   |
| Claude 3 Opus       | 200,000                 | 2024 | –                                         |
| Gemini 1.5 Pro      | 2,000,000               | 2024 | Ring Attention, MoE                       |
| Llama 3             | 8,192 (base) / 128K (instruct) | 2024 | RoPE + positional interpolation     |
| Grok‑1              | 8,192                   | 2024 | –                                         |
| Qwen 2.5            | 128,000                 | 2024 | Dense + FlashAttention                    |
| DeepSeek‑V3         | 128,000                 | 2024 | MLA (Multi‑head Latent Attention)         |

## The "Lost in the Middle" Phenomenon

Research shows that LLMs exhibit **U‑shaped performance** across context windows:
- **Beginning** – Best remembered (primacy effect).
- **End** – Second best (recency effect).
- **Middle** – Worst forgotten.

### Visualisation

```text
Relevance
  │
  │  ██████                    ██████
  │  ██████                    ██████
  │  ██████  ██  ██  ██  ██   ██████
  │  ██████  ██  ██  ██  ██   ██████
  │  ██████  ██  ██  ██  ██   ██████
  │  ██████  ██  ██  ██  ██   ██████
  └─────────────────────────────────────────── Position
     Start    │     Middle     │      End
              (Lowest recall)
