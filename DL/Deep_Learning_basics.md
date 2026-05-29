
# Deep Learning Basics

## 1. Neural Networks
### Definition
Neural Networks are computational models inspired by the human brain. They consist of interconnected layers of neurons that process and learn patterns from data.

### Structure of a Neural Network
- **Input Layer** → Receives input data
- **Hidden Layers** → Perform computations and feature extraction
- **Output Layer** → Produces final prediction

### Working
Each neuron receives inputs, applies weights and activation functions, and passes the output to the next layer.

### Use
Used in:
- Image Recognition
- NLP
- Recommendation Systems
- Speech Recognition

---

## 2. Backpropagation
### Definition
Backpropagation is a learning algorithm used to train neural networks by updating weights based on prediction errors.

### Working Process
1. Forward pass generates predictions
2. Error is calculated using a loss function
3. Error is propagated backward
4. Weights are updated to minimize loss

### Key Idea
Helps the network learn by reducing prediction errors over time.

### Use
Essential for training deep learning models.

---

## 3. Gradient Descent
### Definition
Gradient Descent is an optimization algorithm used to minimize the loss function by adjusting model parameters.

### Working
The algorithm moves weights in the direction where loss decreases the fastest.

### Formula
```text
New Weight = Old Weight - Learning Rate × Gradient
```

### Types
- Batch Gradient Descent
- Stochastic Gradient Descent (SGD)
- Mini-Batch Gradient Descent

### Use
Used to optimize neural network training.

---

## 4. CNN (Convolutional Neural Network)
### Definition
CNN is a deep learning architecture mainly designed for processing image and visual data.

### Main Components
- Convolution Layer
- Pooling Layer
- Fully Connected Layer

### Features
- Automatically extracts image features
- Detects patterns like edges, shapes, and textures

### Applications
- Image Classification
- Face Recognition
- Medical Imaging
- Object Detection

---

## 5. RNN (Recurrent Neural Network)
### Definition
RNN is a neural network designed for sequential data where previous information influences current output.

### Key Feature
Contains memory that helps process sequences step by step.

### Applications
- Text Generation
- Language Translation
- Speech Recognition
- Time Series Prediction

### Limitation
Struggles with long-term dependencies due to vanishing gradient problems.

---

## 6. LSTM (Long Short-Term Memory)
### Definition
LSTM is an advanced type of RNN designed to remember information for long periods.

### Main Components
- Forget Gate
- Input Gate
- Output Gate

### Advantages
- Handles long-term dependencies better
- Reduces vanishing gradient issues

### Applications
- Chatbots
- Machine Translation
- Speech Processing
- Text Prediction

---

## 7. Attention Mechanism
### Definition
Attention Mechanism allows models to focus on the most important parts of the input while making predictions.

### Key Idea
Instead of treating all input equally, the model gives higher importance to relevant words or features.

### Benefits
- Improves context understanding
- Handles long sequences effectively
- Enhances model performance

### Applications
- Transformers
- Machine Translation
- Summarization
- Large Language Models (LLMs)

### Example
In the sentence:
```text
"The cat sat on the mat because it was tired"
```

Attention helps the model understand that **"it"** refers to **"the cat"**.
