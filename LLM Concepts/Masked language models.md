
# Masked Language Models (MLMs)

Masked language models are a class of **bidirectional** transformer models trained to predict randomly masked tokens in a sequence. Unlike autoregressive models (which predict the next token left‑to‑right), MLMs see **both left and right context** simultaneously. BERT (Bidirectional Encoder Representations from Transformers) is the canonical example.

## Core Idea

Given an input sequence, a percentage of tokens (typically 15%) are replaced with a special `[MASK]` token. The model learns to predict the original vocabulary IDs of those masked positions using **all surrounding tokens** (both left and right).

**Training objective:**  
`L = - Σ_{i ∈ masked_positions} log P(x_i | x_{unmasked})`

## How It Works (BERT‑style)

### Input Representation

```text
Input:     [CLS]  The   cat   [MASK]  on   the   mat  [SEP]
Masked:          ✗     ✗      ✔      ✗    ✗     ✗     ✗
Target:          –     –     sat     –    –     –      –
```
[CLS] – Special token for classification tasks (aggregated output).

[SEP] – Separator for sentence pairs.

Masked positions (15% of tokens) are predicted using the final hidden states.


Training Procedure (Masking Strategy)
For each masked position with probability 15%:

Action	Probability	Rationale
Replace with [MASK]	80%	Standard masking
Replace with a random token	10%	Reduces mismatch with fine‑tuning
Keep unchanged	10%	Biases representation towards true token
This prevents the model from relying solely on [MASK] as a signal and forces it to learn general token representations.

Architecture (Transformer Encoder)
Unlike autoregressive models (decoder‑only), MLMs use the encoder‑only stack – full bidirectional attention without a causal mask.
