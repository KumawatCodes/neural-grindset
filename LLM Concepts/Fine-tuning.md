# neural-grindset / LLM Concepts / FineTuning.md

## Edit

# Fine‑Tuning

Fine‑tuning is the process of taking a pre‑trained language model and continuing its training on a smaller, task‑specific dataset. It adapts the model's general knowledge to a particular domain, style, or instruction‑following format, producing a specialised version of the base model.

## Pre‑training vs. Fine‑tuning

| Aspect               | Pre‑training                                | Fine‑tuning                                   |
|----------------------|---------------------------------------------|-----------------------------------------------|
| **Data**             | Massive, general corpus (web, books, code)  | Small, task‑specific dataset                  |
| **Objective**        | Next‑token prediction (autoregressive) or MLM | Task‑specific loss (chat, classification, summarisation) |
| **Compute**          | Extremely expensive (millions of GPU hours) | Relatively cheap (hours to days on 1–8 GPUs)  |
| **Output**           | Base model (e.g., GPT‑4 base, Llama base)   | Domain‑specific model (e.g., CodeLlama, medical‑chat) |
| **Frequency**        | Once per model generation                   | Repeatedly per use case / dataset             |

## Why Fine‑tune?

| Reason                                | Explanation                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------|
| **Domain adaptation**                 | General models struggle with niche terminology (legal, medical, finance).   |
| **Style / tone control**              | Teach the model to respond in a specific voice or format (e.g., Shakespearean, concise). |
| **Instruction following (SFT)**       | Turn a base model into a helpful chatbot (chat‑tuned models).               |
| **Task specialisation**               | Improve performance on a specific task (sentiment, NER, translation).       |
| **Efficiency / latency**              | A fine‑tuned smaller model can outperform a larger generic model on your task. |
| **Cost reduction**                    | Fine‑tuned smaller models (7B) can replace prompting giant models (100B+) for specific use cases. |

## Types of Fine‑tuning

### 1. Full Fine‑tuning (FFT)

**Process:** Update **all** parameters of the model on the new dataset.

```text
Pre‑trained weights:  W₀ (size = 7B)
After FFT:            W₀ → W₁ (all 7B params updated)
