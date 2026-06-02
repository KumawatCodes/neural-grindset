# 3. FastText

## Definition
FastText extends Word2Vec by using character n-grams to create embeddings.

### Small Code

```python
from gensim.models import FastText

sentences = [["i","love","nlp"]]

model = FastText(
    sentences,
    vector_size=50,
    min_count=1
)

print(model.wv["nlp"])
```
## Diagram
<img width="2144" height="1046" alt="image" src="https://github.com/user-attachments/assets/7ff8f946-8439-4195-8bd8-fcad2a7e47be" />


### Advantages
- Handles rare words
- Handles unseen words (OOV)

### Example

```text
learning
learned
learner
```

FastText understands similarities because it uses character information.

### Limitation
Larger model size than Word2Vec.

---
