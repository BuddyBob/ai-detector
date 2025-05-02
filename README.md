# AI vs Human Text Classification

Uses mmachine learning pipeline for distinguishing between AI-generated and human-written text. It utilizes sentence embeddings, logistic regression, and calibrated probability outputs.


## Primar Goal
The primary goal of this project is to create a machine learning model that can accurately classify text as either AI-generated or human-written. The model should be able to handle various types of text and provide reliable predictions with calibrated probabilities. This is achieved by combining modern embedding techniques with a lightweight and explainable classification algorithm.

I wanted to stay away from using LLMS for this task, one because thats entirely too easy, and two they arent very reliable or always available. I wanted to create a model that could be used in production without relying on external APIs or services. This is why I chose to use sentence embeddings and logistic regression, which are both lightweight and easy to interpret.


## Model Architecture

### Embedding Layer

- **Model**: [`sentence-transformers/all-MiniLM-L6-v2`](https://www.sbert.net/docs/pretrained_models.html)
- **Purpose**: Converts each input text into a dense 384-dimensional vector representation.
- **Efficiency**: Fast enough for large-scale datasets; balances speed and semantic accuracy.

### Classifier

- **Algorithm**: Logistic Regression
- **Justification**: A linear model was selected for its transparency, simplicity, and ability to produce well-calibrated probabilities when combined with post-hoc calibration.
- **Training Data**: Balanced set of AI-generated and human-written essays (~20,000 samples total).

### Calibration

- **Method**: Isotonic Regression via `CalibratedClassifierCV`
- **Why**: Calibrated probability outputs improve interpretability and reduce overconfidence, which is common when distinguishing subtle writing style differences between AI and human texts.


## File Structure


```text
.
├── articles.json             # Input dataset in JSON lines format
├── model.py                  # Training script (embedding + model + calibration)
├── predict.py                # Script for classifying new examples
├── model_calibrated.pkl      # Trained and calibrated logistic regression model
├── embedder/                 # Saved sentence-transformer model directory
├── embeddings.npy            # Cached text embeddings (speeds up training)
├── labels.npy                # Binary labels (0: AI, 1: Human)
└── .gitattributes            # LFS tracking configuration for large files
```


## Running the Model

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python model.py
```

**This will:**

-  Encode all text inputs using the sentence transformer
-  Cache embeddings to embeddings.npy and labels.npy
-  Train and calibrate the logistic regression model
-  Save the final model to model_calibrated.pkl

### 3. Make Predictions
```bash
python predict.py --text "Your text here"
```

## Thresholding Strategy
The prediction logic supports a configurable threshold for classifying AI text. By default:
```python
AI if prob_AI > 0.60 else HUMAN
```
This threshold can be adjusted in predict.py. Higher means if model wants to predict AI, it has to be more confident. Lower means it can be more lenient.

## Limitations

- The model can misclassify highly edited or formal human writing as AI due to stylistic similarities.

- Generated text that mimics human imperfections or conversational tone may evade detection.

- Performance on out-of-distribution text (e.g., poetry, technical documentation, or code) may be lower depending on training data scope.

## Acknowledgments
Hugging Face Sentence Transformers

Scikit-learn for modeling and calibration tools

Contributors to open datasets of AI and human-authored texts