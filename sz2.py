import joblib
import json
import numpy as np

model = joblib.load("real_model.pkl")


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


features = extract_features("unknown_real_s.json")
prediction = model.predict([features])[0]

if prediction == 0:
    print("Normal movement")
else:
    print("Seizure detected")
