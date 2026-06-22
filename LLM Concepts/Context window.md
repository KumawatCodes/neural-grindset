
# Context Window

The context window (or context length) is the maximum number of tokens a language model can process in a single forward pass. For generative models, this includes **both** the input prompt and the generated response – once the generated tokens reach the limit, the model must stop or truncate the conversation history.

## Why It Matters

- **Long‑form reasoning** – Reads entire documents, books, or codebases in one go.
- **In‑context learning** – More examples in the prompt improve performance (few‑shot learning).
- **Conversational memory** – Chatbots can retain longer dialogue history without forgetting.
- **RAG vs. Long‑Context** – Deciding whether to retrieve (RAG) or just stuff everything into the prompt.

## Attention Complexity: The Bottleneck

In standard Transformer self‑attention, the computational and memory complexity scales **quadratically** with sequence length:
