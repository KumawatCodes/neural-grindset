# neural-grindset / LLM Concepts / Prompting.md

## Edit

# Prompting & Decoding Parameters (Temperature, Top‑k, Top‑p)

This guide covers two essential aspects of working with LLMs:
1. **Prompting** – How to structure inputs to get the desired output.
2. **Decoding Parameters** – How to control randomness, diversity, and coherence during generation.

---

## Part 1: Prompting

Prompting is the art and science of crafting input text to guide a language model toward a specific output. The model doesn't "understand" intent – it predicts the most probable continuation based on the prompt.

### Basic Prompt Structure

[System] → [User] → [Assistant] → (generation)

System: Sets the behaviour, tone, and persona.
User: The actual question or instruction.
Assistant: The model's response (or start of it).


### Types of Prompting

| Technique               | Description                                                                 | Example                                                           |
|-------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------|
| **Zero‑shot**           | No examples; just instruction.                                             | *"Classify this text as positive or negative: 'I love this!'"*    |
| **Few‑shot**            | Provide 1–5 examples before the actual query.                              | *"Positive: 'Great!'\nNegative: 'Terrible.'\nClassify: 'Okay.'"*   |
| **Chain‑of‑Thought (CoT)** | Force the model to reason step‑by‑step before answering.                 | *"Let's think step by step. First, ... Therefore, the answer is..."* |
| **Role‑based**          | Assign a persona / role to the model.                                     | *"You are a senior Python developer. Review this code..."*        |
| **System Prompt**       | Permanent instructions that override user behaviour (API, e.g., OpenAI).  | *"You are a helpful assistant that only speaks in haikus."*      |
| **Instruction (ChatML)** | Clear, imperative statements. Very effective with instruction‑tuned models. | *"Summarise the following text in two sentences:"*              |

### Prompt Engineering Best Practices

- **Be specific** – Vague prompts yield vague outputs.
- **Use delimiters** – `---`, `###`, or triple backticks to separate instructions from data.
- **Assign a role** – "You are an expert historian..." improves factual grounding.
- **Ask for citations** – "Cite the relevant paragraph" reduces hallucination.
- **Specify output format** – JSON, Markdown, bullet points, etc.

---

## Part 2: Decoding / Sampling Parameters

After the model computes logits (raw scores) for each token in the vocabulary, **decoding** converts these logits into a selected token. The parameters below control this conversion.

### The Generation Pipeline (ASCII)
