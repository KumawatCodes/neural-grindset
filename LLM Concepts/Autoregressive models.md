
# Autoregressive Models

Autoregressive (AR) models generate sequences **one element at a time**, conditioning each new element on the previously generated ones. They are the foundation of modern large language models (LLMs) like GPT‑4, Llama, and Gemini.

## Core Idea

Given a sequence `x₁, x₂, ..., xₜ`, an autoregressive model learns the conditional probability distribution:
