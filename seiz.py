import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Function to extract features from accelerometer JSON
def extract_features(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    x = [d["x"] for d in data]
    y = [d["y"] for d in data]
    z = [d["z"] for d in data]

    # Features: mean, std, max-min for each axis
    features = [
        np.mean(x), np.std(x), np.max(x)-np.min(x),
        np.mean(y), np.std(y), np.max(y)-np.min(y),
        np.mean(z), np.std(z), np.max(z)-np.min(z),
    ]
    return features

# Load data
X = []
y = []

# Normal data → label 0
X.append(extract_features("norm_real.json"))
y.append(0)

# Seizure data → label 1
X.append(extract_features("seiz_real.json"))
y.append(1)

# Convert to arrays
X = np.array(X)
y = np.array(y)

# Train classifier
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, "Seizure_detector.pkl")

