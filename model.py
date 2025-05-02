import os
import json
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report

# === CONFIG ===
EMBEDDINGS_PATH = "embeddings.npy"
LABELS_PATH = "labels.npy"
EMBEDDER_NAME = "all-MiniLM-L6-v2"
MODEL_PATH = "model_calibrated.pkl"
EMBEDDER_SAVE_DIR = "embedder"
DATA_FILE = "articles.json"

# === LOAD DATA ===
def load_data(file_path):
    texts, labels = [], []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            texts.append(data['text'])
            labels.append(int(data['label']))  #make sure we use 0 not '0
    return texts, np.array(labels)


def get_embeddings(texts, labels):
    if os.path.exists(EMBEDDINGS_PATH) and os.path.exists(LABELS_PATH):
        print("🔄 Loading cached embeddings...")
        X = np.load(EMBEDDINGS_PATH)
        y = np.load(LABELS_PATH)
    else:
        print("⚙️  Generating new embeddings...")
        embedder = SentenceTransformer(EMBEDDER_NAME)
        X = embedder.encode(texts, show_progress_bar=True)
        y = np.array(labels)
        np.save(EMBEDDINGS_PATH, X)
        np.save(LABELS_PATH, y)
        embedder.save(EMBEDDER_SAVE_DIR)
    return X, y



if __name__ == "__main__":
    texts, labels = load_data(DATA_FILE)
    X, y = get_embeddings(texts, labels)

    # Split data into train/calib/test
    X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_calib, y_train, y_calib = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)

    # Train base logistic regression model
    base_model = LogisticRegression(max_iter=1000)
    base_model.fit(X_train, y_train)

    # Calibrate using isotonic regression
    calibrated_model = CalibratedClassifierCV(estimator=base_model, method='isotonic', cv='prefit')
    calibrated_model.fit(X_calib, y_calib)

    # Evaluate on test set
    y_pred = calibrated_model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=["AI", "HUMAN"]))

    # Save calibrated model
    joblib.dump(calibrated_model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
