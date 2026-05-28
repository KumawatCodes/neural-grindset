# NLP Fundamentals

## 1. Text Normalization
### Definition
Text normalization converts raw text into a clean and consistent format.

### Common Techniques
- Lowercasing
- Removing punctuation
- Removing extra spaces
- Expanding contractions
- Removing special characters

### Example
`"Hello!!! I’m HAPPY :)"` → `"hello i am happy"`

### Use
Improves consistency and model performance.

---

## 2. Tokenization
### Definition
Tokenization splits text into smaller units called tokens.

### Types of Tokenization
- Word Tokenization
- Sentence Tokenization
- Subword Tokenization

### Example
`"I love NLP"` → `["I", "love", "NLP"]`

### Use
Converts text into machine-readable form.

---

## 3. Stopword Removal
### Definition
Removes commonly used words that carry little meaning.

### Examples of Stopwords
`is, am, the, in, and, of`

### Example
`"The cat is on the mat"` → `"cat mat"`

### Use
Reduces noise in text processing.

---

## 4. Stemming
### Definition
Stemming reduces words to their root form by removing suffixes.

### Example
- `playing → play`
- `studies → studi`

### Advantages
- Fast
- Simple preprocessing technique

### Limitations
May produce invalid root words.

### Use
Used for faster text processing and search systems.

---

## 5. Lemmatization
### Definition
Lemmatization converts words into meaningful dictionary base forms.

### Example
- `running → run`
- `better → good`

### Advantages
- More accurate than stemming
- Preserves actual meaning

### Limitations
Slightly slower than stemming.

### Use
Used when meaning preservation is important.

---

## 6. N-grams
### Definition
N-grams are continuous sequences of N words or characters.

### Types of N-grams
- Unigram → Single word
- Bigram → Two-word sequence
- Trigram → Three-word sequence

### Example
Sentence: `"I love NLP"`

- Unigram → `["I", "love", "NLP"]`
- Bigram → `["I love", "love NLP"]`
- Trigram → `["I love NLP"]`

### Use
Captures context and word relationships.

---

## 7. Bag of Words (BoW)
### Definition
Bag of Words represents text using word frequency without considering order.

### Example

| Word | Count |
|------|------|
| I | 1 |
| love | 1 |
| NLP | 1 |

### Characteristics
- Simple representation
- Ignores grammar and word order

### Use
Used in basic NLP and text classification tasks.

---

## 8. TF-IDF
### Full Form
Term Frequency - Inverse Document Frequency

### Definition
Measures how important a word is in a document relative to a collection of documents.

### Components
- TF → Frequency of term in document
- IDF → Rarity of term across documents

### Use
Highlights important words while reducing common words.

---

## 9. POS Tagging
### Full Form
Part-of-Speech Tagging

### Definition
Assigns grammatical labels to words.

### Common POS Tags
- Noun
- Verb
- Adjective
- Adverb

### Example
`"Dogs bark loudly"`

- Dogs → Noun
- bark → Verb
- loudly → Adverb

### Use
Helps understand sentence structure.

---

## 10. Named Entity Recognition (NER)
### Definition
NER identifies important entities in text.

### Common Entity Types
- Person
- Location
- Organization
- Date

### Example
`"Elon Musk founded SpaceX in the USA"`

- Elon Musk → Person
- SpaceX → Organization
- USA → Location

### Use
Used in chatbots, search engines, and information extraction.

---

## 11. Dependency Parsing
### Definition
Dependency parsing identifies grammatical relationships between words.

### Example
`"She eats pizza"`

- eats → Main verb
- She → Subject
- pizza → Object

### Use
Helps understand sentence meaning and structure.

---

## 12. Semantic Similarity
### Definition
Measures how similar two texts are in meaning.

### Example
- `"I like AI"`
- `"I enjoy artificial intelligence"`

These sentences are semantically similar.

### Use
Used in:
- Search engines
- Recommendation systems
- Chatbots

---

## 13. BM25
### Definition
BM25 is a ranking algorithm used in search engines to retrieve relevant documents.

### Features
- Based on TF-IDF
- Considers document length
- Generates relevance scores

### Use
Widely used in:
- Information Retrieval
- Search Engines
- RAG Systems

---

# Evaluation Metrics

## 14. Precision
### Definition
Measures how many retrieved results are actually relevant.

### Formula
```text
Precision = Relevant Retrieved / Total Retrieved
```

### Focus
Correctness of retrieved results.

---

## 15. Recall
### Definition
Measures how many relevant results were successfully retrieved.

### Formula
```text
Recall = Relevant Retrieved / Total Relevant
```

### Focus
Completeness of retrieval.

---

## 16. F1 Score
### Definition
Harmonic mean of Precision and Recall.

### Formula
```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

### Use
Balances precision and recall.

---

## 17. MAP
### Full Form
Mean Average Precision

### Definition
Measures average precision across multiple queries.

### Use
Evaluates ranking quality in search systems.

---

## 18. MRR
### Full Form
Mean Reciprocal Rank

### Definition
Measures how quickly the first correct result appears.

### Formula
```text
MRR = 1 / Rank of first relevant result
```

### Use
Common in question-answering systems.

---

## 19. NDCG
### Full Form
Normalized Discounted Cumulative Gain

### Definition
Evaluates ranking quality by considering relevance and position.

### Key Idea
Higher-ranked relevant documents receive more importance.

### Use
Widely used in:
- Recommendation Systems
- Search Engines
- Retrieval Systems
