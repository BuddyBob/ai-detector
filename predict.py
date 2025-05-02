import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
#arguments 
import sys
import os


#Config
MODEL_PATH = "model_calibrated.pkl"
EXAMPLE_ESSAY_PATH = "example_essay.txt"
EMBEDDER_DIR = "embedder"
AI_THRESHOLD = 0.60 

# loadin MODEL + EMBEDDER
model = joblib.load(MODEL_PATH)
embedder = SentenceTransformer(EMBEDDER_DIR)


def predict_text(text):
    embedding = embedder.encode([text])
    proba = model.predict_proba(embedding)[0]  # [AI, HUMAN]

    ai_confidence = proba[0]
    label = "AI" if ai_confidence > AI_THRESHOLD else "HUMAN"

    return {
        "label": label,
        "confidence_AI": round(ai_confidence, 4),
        "confidence_HUMAN": round(proba[1], 4)
    }

def load_example_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text



if __name__ == "__main__":
    #get argument --text
    if len(sys.argv) > 1:
        sample = sys.argv[1]
    else:
        sample = load_example_text("example_essay.txt")

    result = predict_text(sample)
    print("\nPrediction:", result["label"])
    print("Confidence → AI:", result["confidence_AI"], "| HUMAN:", result["confidence_HUMAN"])
    

