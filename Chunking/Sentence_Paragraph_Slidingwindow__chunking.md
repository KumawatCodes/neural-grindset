# neural-grindset / LLM Concepts / ChunkingStrategies.md

# Chunking Strategies: Sentence, Paragraph & Sliding Window

Following the foundational strategies (Fixed, Recursive, Semantic), this guide covers three additional approaches that prioritize **linguistic boundaries** and **contextual continuity**. These strategies are essential when you need to preserve grammatical structure, topical integrity, or maintain a rolling awareness of surrounding text.

---

## Chunking Strategy Comparison (Complete Reference)

| Strategy | Best For | Granularity | Context Preservation | Overlap Support | Implementation Complexity |
|----------|----------|-------------|----------------------|-----------------|---------------------------|
| **Fixed-Size** | Log files, prototyping | Token/Character | Low | Yes (sliding) | Very Low |
| **Recursive** | General articles, default | Hierarchical | Medium | Yes | Low |
| **Semantic** | Research papers, tech docs | Topic-bound | Very High | Implicit | High |
| **Sentence** | NER, sentiment, short QA | Grammatical (per sentence) | Very Low (isolated) | No (inherent) | Low |
| **Paragraph** | Topic-based retrieval, summarisation | Topical (paragraph) | High | No (inherent) | Very Low |
| **Sliding Window** | Context-heavy QA, long-form reasoning | Rolling context | Very High | Yes (overlap) | Medium |

---

## 4. Sentence Chunking

Splits documents at **sentence boundaries** using punctuation (`.`, `?`, `!`) and NLP-aware sentence segmentation (e.g., NLTK, spaCy, or Hugging Face tokenizers).

### How It Works

Each sentence becomes its own chunk (or group of sentences if you combine them). This is ideal for tasks where each unit of meaning is complete.

Document: "The quick brown fox jumps over the lazy dog. The dog slept. It was a peaceful afternoon."
│ │ │ │
▼ ▼ ▼ ▼
Chunk 1: "The quick brown fox jumps over the lazy dog."
Chunk 2: "The dog slept."
Chunk 3: "It was a peaceful afternoon."

### Implementation (spaCy)

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def sentence_chunking_spacy(text: str) -> list[str]:
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

text = "Hello world. This is a test. How are you?"
chunks = sentence_chunking_spacy(text)
print(chunks)
# ['Hello world.', 'This is a test.', 'How are you?']
```

Implementation (NLTK)
```
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import sent_tokenize

def sentence_chunking_nltk(text: str) -> list[str]:
    return sent_tokenize(text)

# You can also group sentences to avoid overly small chunks
def sentence_chunking_grouped(text: str, sentences_per_chunk: int = 2) -> list[str]:
    sents = sent_tokenize(text)
    return [' '.join(sents[i:i+sentences_per_chunk]) 
            for i in range(0, len(sents), sentences_per_chunk)]
```
