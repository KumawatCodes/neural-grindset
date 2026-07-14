# RAG (Retrieval-Augmented Generation)

RAG (Retrieval-Augmented Generation) is an architecture that enhances large language models by **retrieving relevant information from an external knowledge base** and incorporating it into the prompt before generation. Instead of relying solely on the model's internal (and often outdated) parameters, RAG grounds the response in real, factual, and up-to-date data.

## Core Idea

Retrieve → Augment → Generate
↓ ↓ ↓
Search Inject LLM produces
external retrieved answer with
data context citations


Instead of asking the model: *"What is the answer?"*  
RAG asks: *"What is the answer, based on these specific documents I just found?"*

## Why RAG? (The Three Core Problems It Solves)

LLMs, despite their power, have fundamental limitations that RAG directly addresses:

### 1. Knowledge Cutoff (Stale Information)

LLMs are frozen at their training date. A model trained in 2023 has **zero knowledge** of:

- Recent news, events, or discoveries (e.g., "Who won the 2026 World Cup?")
- New product releases or API updates
- Latest research papers or regulations

**RAG fix:** Point the retriever to a freshly updated database (news feeds, company wikis, live APIs) – the model instantly becomes "current" without retraining.

### 2. Hallucinations (Confident Falsehoods)

LLMs are next-token predictors, not fact-checkers. When unsure, they **generate plausible-sounding but incorrect information** – complete with convincing citations that don't exist.

**Example:**

User: "What was Acme Corp's revenue in Q3 2025?"
LLM: "Acme Corp reported $12.4 billion in Q3 2025." (Completely fabricated)


**RAG fix:** The model never invents numbers – it reads them directly from the retrieved financial report. If the report doesn't exist, the model can say "I don't know" instead of hallucinating.

### 3. No Traceability (Black Box)

Without RAG, you cannot verify *why* the model gave a particular answer. In regulated industries (healthcare, finance, law), **auditability is non-negotiable**.

**RAG fix:** Every claim can be traced back to a specific source document, paragraph, or even sentence.

---

## How RAG Works (The Pipeline)

### Step 1: Indexing (Offline / Pre-processing)

Before users ask questions, you must prepare your knowledge base:

Raw Documents (PDFs, Wikis, DBs)
│
▼
Split into chunks
(e.g., 500 tokens each)
│
▼
Generate Embeddings
(vector representations)
│
▼
Store in Vector Database
(e.g., Pinecone, Weaviate, FAISS)

### Step 2: Retrieval (Online / Query Time)

When a user asks a question:

User Question: "What is LoRA?"
│
▼
Generate query embedding
│
▼
Search vector database for
most similar document chunks
(using cosine similarity)
│
▼
Return Top‑k chunks (e.g., top 5)
(most relevant context)

text

### Step 3: Augmentation & Generation

Original Prompt: "What is LoRA?"
Retrieved Context:

"LoRA is Low-Rank Adaptation..."

"It reduces trainable parameters..."

"Commonly used with QLoRA..."

Augmented Prompt:
"Based on the following context, answer the question.
Context: [retrieved chunks]
Question: What is LoRA?
Answer:"

LLM generates a grounded, cited answer.


---

## RAG vs. Fine‑tuning (The Critical Decision)

| Aspect               | RAG                                          | Fine‑tuning / LoRA                          |
|----------------------|----------------------------------------------|---------------------------------------------|
| **Knowledge freshness** | Instant – update the vector DB              | Slow – must retrain the model               |
| **Data required**    | Documents (PDFs, wikis, text)                | 1k–100k+ labelled examples                  |
| **Training cost**    | Zero (no training)                          | High (GPU hours to days)                    |
| **Inference cost**   | Higher (DB lookup + LLM)                    | Lower (just LLM)                            |
| **Traceability**     | Excellent (cites specific sources)          | Poor (model is a black box)                 |
| **Hallucinations**   | Low (grounded in retrieved data)            | Moderate (still can hallucinate)            |
| **Latency**          | Higher (search + generation)                | Lower (generation only)                     |
| **Domain adaptation**| Good (if docs exist)                        | Excellent (learns style/vocabulary)         |
| **Updating**         | Trivial (add/remove documents)              | Difficult (must retrain)                    |
| **Use case**         | Factual Q&A, customer support, research     | Tone/style adaptation, code generation, chat |

**Best strategy (Industry Standard):**
- **RAG** for facts, latest news, private data.
- **Fine‑tuning** for tone, format, persona, and behaviour.
- **Both together** – fine‑tune the model to cite sources well, then use RAG for data.

---

## Code Example: Basic RAG with LangChain

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# 1. Load documents
loader = TextLoader("knowledge_base.txt")
documents = loader.load()

# 2. Chunk documents
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# 3. Embed and store in vector DB
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

# 4. Create retriever
retriever = db.as_retriever(search_kwargs={"k": 4})

# 5. Build RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 6. Query
result = qa_chain({"query": "What is LoRA?"})
print(result["result"])
print("Sources:", [doc.metadata for doc in result["source_documents"]])
```

Code Example: RAG from Scratch (Minimal)
```python
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Sample documents
docs = [
    "LoRA is Low-Rank Adaptation for efficient fine-tuning.",
    "RAG stands for Retrieval-Augmented Generation.",
    "QLoRA combines 4-bit quantization with LoRA.",
    "Fine-tuning updates all model weights."
]

# 1. Embed
embedder = SentenceTransformer('all-MiniLM-L6-v2')
doc_embeddings = embedder.encode(docs)

# 2. Query
query = "What is LoRA?"
query_emb = embedder.encode([query])

# 3. Retrieve
similarities = cosine_similarity(query_emb, doc_embeddings)[0]
top_k_idx = np.argsort(similarities)[-2:][::-1]  # top 2

retrieved_docs = [docs[i] for i in top_k_idx]

# 4. Augment + Generate (simulate)
context = "\n".join(retrieved_docs)
prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer based only on context:"

# In reality, you'd call an LLM here:
# response = llm.generate(prompt)
print(prompt)
