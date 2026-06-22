
# Hallucination (in Generative AI)

Hallucination refers to the phenomenon where a generative model produces content that is **factually incorrect, contradictory, or entirely fabricated** – yet presents it with high confidence and fluency. Unlike a simple mistake, hallucinations are often *plausible-sounding* nonsense, making them particularly dangerous in high‑stakes applications (medicine, law, finance).

## Why Hallucinations Are Dangerous

- **Trust erosion** – Users lose confidence when models confidently state falsehoods.
- **Misinformation spread** – Generated content can be mistaken for ground truth.
- **Legal & compliance risks** – Incorrect legal citations or medical advice can have real consequences.
- **Hidden cost of verification** – Humans must fact‑check every output, negating productivity gains.

## Types of Hallucinations

| Type                  | Description                                                          | Example                                                               |
|-----------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|
| **Factual**           | Contradicts established world knowledge.                             | *"The capital of Australia is Sydney."* (actually Canberra)           |
| **Faithfulness**      | Contradicts the user's provided context (RAG, summarisation).        | *Given a document about cats, the model says "Dogs are mentioned."*   |
| **Logical**           | Reasoning error leading to an absurd or contradictory conclusion.    | *"If A > B and B > C, then C > A."*                                  |
| **Extrinsic**         | Introduces new information not in the prompt or source, unverifiable. | *Inventing a study that doesn't exist to support a claim.*            |
| **Intrinsic**         | Contradicts the provided source or prompt (direct violation).        | *Prompt: "The sky is blue." → Output: "The sky is green."*            |

## Why Hallucinations Happen

### 1. Training Data Issues
- **Incomplete coverage** – Model lacks knowledge about niche topics.
- **Contradictions** – Conflicting facts in training data (e.g., outdated information).
- **Sycophancy** – Model learns to agree with false user premises.

### 2. Training Objective (Teacher Forcing)
Autoregressive models are trained to minimise cross‑entropy loss on **next‑token prediction**. This encourages:
- **Short‑term coherence** over long‑term factual accuracy.
- **Maximum likelihood** – The model learns the *most probable* continuation, not necessarily the *correct* one.

### 3. Exposure Bias (Train‑Inference Mismatch)
During training, the model sees the true previous tokens (teacher forcing). During inference, it sees its **own predictions** – errors accumulate and amplify.

```text
Training:  [The] [capital] [of] [France] → [is] [Paris] (true)
Inference: [The] [capital] [of] [France] → [is] [London?] (drifts)
