
# Tokenization

Tokenization is the process of splitting raw text into smaller units called **tokens** (words, subwords, or characters) that a language model can process. It is the first step in any NLP pipeline – mapping from human‑readable text to model‑digestible integers.

## Why Tokenization Matters

- **Vocabulary size** – Tokens balance between expressiveness (too many unique words) and efficiency (too few tokens lose meaning).
- **Out‑of‑vocabulary (OOV)** – Subword tokenization handles unseen words gracefully.
- **Model architecture** – Transformer models have a fixed vocabulary and maximum sequence length (in tokens, not characters).

## Types of Tokenization

| Strategy          | Example                                      | Pros                              | Cons                               |
|-------------------|----------------------------------------------|-----------------------------------|------------------------------------|
| **Word**          | `"I love NLP"` → `["I", "love", "NLP"]`      | Intuitive, fast                   | Huge vocab (>500k), OOV on typos   |
| **Character**     | `"cat"` → `["c", "a", "t"]`                  | No OOV, tiny vocab                | Long sequences, loses word meaning |
| **Subword**       | `"unhappiness"` → `["un", "happiness"]`      | Balances vocab & OOV, state‑of‑the‑art | Slightly complex to implement |

Most modern LLMs (GPT, BERT, Llama) use **subword tokenization**.

## Popular Subword Algorithms

### 1. Byte Pair Encoding (BPE)

**Used by:** GPT‑2, GPT‑4, RoBERTa, Llama

**How it works:**
1. Start with character vocabulary (bytes in GPT‑4).
2. Repeatedly merge the most frequent adjacent pair of tokens.
3. Stop when vocabulary reaches target size.

```text
Initial:  c a t s   c a t   (spaces as special token)
Freq pairs: ("c","a"):2, ("a","t"):2, ("t","s"):1, ...
Merge "c"+"a" → "ca"
Now: ca t s   ca t
Merge "ca"+"t" → "cat"
Now: cat s   cat
Merge "cat"+"s" → "cats"
Final vocab: c, a, t, s, ca, cat, cats, ...
