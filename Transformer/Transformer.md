
# Transformer Architecture

## Introduction
### Definition
Transformer is a deep learning architecture introduced in the paper **"Attention Is All You Need" (2017)**. Unlike RNNs and LSTMs, Transformers process all input tokens in parallel using attention mechanisms, making them faster and more effective for handling long sequences.

### Why Transformers?
Traditional RNNs process words sequentially, making training slow and limiting long-range context understanding. Transformers solve this problem using **self-attention**.

### Applications
- Large Language Models (GPT, Llama, Claude)
- Machine Translation
- Text Summarization
- Question Answering
- Chatbots



<img width="631" height="868" alt="Screenshot 2026-05-30 at 5 50 53 pm" src="https://github.com/user-attachments/assets/f0d16ef6-2c18-4162-964f-9947d3c69207" />
---

## 1. Encoder and Decoder

### Encoder
The encoder processes the input sequence and generates contextual representations for each token.

### Decoder
The decoder uses encoder outputs and previously generated tokens to produce the final output sequence.

### Architecture

```text
Input Sentence
      ↓
   Encoder
      ↓
 Context Vector
      ↓
   Decoder
      ↓
Output Sentence
```

### Example
Input:
```text
English: "I love AI"
```

Output:
```text
French: "J'aime l'IA"
```

---

## 2. Self-Attention

### Definition
Self-attention allows each word in a sentence to focus on other relevant words in the same sentence.

### Example

Sentence:
```text
"The animal didn't cross the street because it was tired."
```

Self-attention helps determine that **"it"** refers to **"animal"**.

### Benefits
- Captures long-range dependencies
- Understands context effectively
- Enables parallel processing

---
<img width="357" height="388" alt="Screenshot 2026-05-30 at 5 52 36 pm" src="https://github.com/user-attachments/assets/545a0db4-735d-4822-85da-e7a92027ebb0" />

## 3. Cross-Attention

### Definition
Cross-attention allows the decoder to focus on encoder outputs while generating responses.

### Example

Input:
```text
"I love AI"
```

While generating the translation, the decoder attends to relevant encoder tokens.

### Use
Important in:
- Machine Translation
- Encoder-Decoder Models
- T5 and BART architectures

---

## 4. Query (Q), Key (K), and Value (V)

### Definition
Every token is transformed into three vectors:

- **Query (Q)** → What information am I looking for?
- **Key (K)** → What information do I contain?
- **Value (V)** → The actual information to share.

### Attention Formula

```text
Attention(Q,K,V) = Softmax(QKᵀ / √d) × V
```

### Intuition

Imagine a student asking questions:

- Query → Question
- Key → Topic labels
- Value → Actual notes

The student matches questions with relevant notes.

<img width="325" height="352" alt="Screenshot 2026-05-30 at 5 56 20 pm" src="https://github.com/user-attachments/assets/30065965-67ff-4708-abe5-61a6c45a16ff" />

---

## 5. Positional Encoding

### Definition
Transformers process words simultaneously, so they need positional information to understand word order.

### Example

Without positions:

```text
"I love AI"
"AI love I"
```

would appear identical.

### Solution
Positional encodings are added to word embeddings.

### Use
Helps preserve sequence order information.

<img width="463" height="426" alt="Screenshot 2026-05-30 at 5 57 46 pm" src="https://github.com/user-attachments/assets/bfda545e-dcb5-417c-9e79-0560fa2ce86b" />

---

## 6. Layer Normalization

### Definition
Layer normalization standardizes activations within a layer to stabilize training.

### Benefits
- Faster convergence
- Stable training
- Better gradient flow

### Use
Applied after attention and feedforward layers.

---

## 7. Residual Connections

### Definition
Residual connections allow information to bypass layers directly.

### Formula

```text
Output = Layer(x) + x
```

### Benefits
- Prevents information loss
- Reduces vanishing gradients
- Enables deeper networks

### Use
Used throughout Transformer blocks.

---

## 8. Feedforward Layers

### Definition
After attention, each token passes through a fully connected neural network.

### Structure

```text
Linear
   ↓
Activation (ReLU/GELU)
   ↓
Linear
```

### Purpose
- Learns complex patterns
- Adds non-linearity
- Enhances feature representation

---

## 9. Masked Attention

### Definition
Masked attention prevents the decoder from seeing future tokens during training.

### Example

Sentence:
```text
I love AI
```

When predicting **"love"**, the model cannot look at **"AI"**.

### Purpose
Ensures autoregressive generation.

### Used In
- GPT
- Decoder-only architectures

---

## 10. Multi-Head Attention

### Definition
Instead of using a single attention mechanism, Transformers use multiple attention heads.

### Working

```text
Input
  ↓
Head 1 Attention
Head 2 Attention
Head 3 Attention
...
Head N Attention
  ↓
Concatenate
  ↓
Final Output
```

### Benefits
Different heads learn different relationships:

- Grammar
- Context
- Entity relationships
- Long-distance dependencies

### Example

Sentence:
```text
"The cat sat on the mat."
```

One head may focus on:
```text
cat ↔ sat
```

Another head may focus on:
```text
cat ↔ mat
```

### Use
Core component of modern Transformers and LLMs.

---

# Complete Transformer Block

```text
Input Embeddings
        +
Positional Encoding
        ↓
Multi-Head Self-Attention
        ↓
Add & Layer Normalization
        ↓
Feedforward Network
        ↓
Add & Layer Normalization
        ↓
Output
```

For Decoder:

```text
Masked Multi-Head Attention
        ↓
Cross-Attention
        ↓
Feedforward Network
        ↓
Output
```

---

# Key Takeaways

- Transformers rely on **attention mechanisms** instead of recurrence.
- **Self-attention** captures relationships between words.
- **Cross-attention** connects encoder and decoder.
- **Q, K, V** form the foundation of attention computation.
- **Positional Encoding** preserves word order.
- **Residual Connections** and **Layer Normalization** improve training stability.
- **Feedforward Layers** enhance representation learning.
- **Masked Attention** enables autoregressive text generation.
- **Multi-Head Attention** learns multiple contextual relationships simultaneously.
- Transformers power modern LLMs such as **GPT, BERT, Claude, Gemini, and Llama**.



## Query-Key-Value Attention

![QKV Attention](images/qkv.png)

## Multi-Head Attention

![Multi Head Attention](images/multi-head-attention.png)

## Positional Encoding

![Positional Encoding](images/positional-encoding.png)


