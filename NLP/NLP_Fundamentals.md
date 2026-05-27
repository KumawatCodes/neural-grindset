# NLP Fundamentals

## 1. Tokenization
**Definition:**  
Tokenization is the process of breaking text into smaller units called **tokens** such as words, sentences, or subwords.

**Example:**  
Text: `"I love learning NLP!"`  
Tokens: `["I", "love", "learning", "NLP"]`

**Types:**  
- Word Tokenization  
- Sentence Tokenization  
- Subword Tokenization

**Why it is used:**  
Converts raw text into a machine-readable format.

---

## 2. Stemming
**Definition:**  
Stemming reduces words to their root form by removing prefixes or suffixes.

**Example:**  
- `playing → play`  
- `studies → studi`  
- `connected → connect`

**Why it is used:**  
Useful for search engines and text preprocessing.

---

## 3. Lemmatization
**Definition:**  
Lemmatization converts words into their meaningful dictionary base form.

**Example:**  
- `running → run`  
- `better → good`  
- `studies → study`

**Why it is used:**  
Used when preserving word meaning is important.

---

## 4. Stopword Removal
**Definition:**  
Removes commonly used words that add little meaning.

**Examples:**  
`is, am, the, in, and, of, to`

**Example:**  
"The cat is sitting on the mat" → "cat sitting mat"

**Why it is used:**  
Reduces noise and improves efficiency.

---

## 5. Text Normalization
**Definition:**  
Standardizes text into a clean format.

**Techniques:**  
- Lowercasing  
- Removing punctuation  
- Removing extra spaces  
- Expanding contractions  
- Removing special characters

**Example:**  
"Hello!!! I’m HAPPY :)" → "hello i am happy"

**Why it is used:**  
Improves NLP model performance.
