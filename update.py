import re
import json
import time
import os
import joblib
import numpy as np
from datetime import datetime


def parse():
	os.system("tools\\adb shell dumpsys sensorservice > file.txt")
	input_file = "file.txt"
	# output_file = "accelerometer.json"
	pattern = re.compile(r"\(ts=(\d+\.\d+).*?\)\s+([-\d.]+),\s+([-\d.]+),\s+([-\d.]+)")
	data = []
	with open(input_file, "r") as f:
		inside_accel = False
		for line in f:
			if line.strip().startswith("ACCELEROMETER:"):
				inside_accel = True
				continue
			if inside_accel and line.strip() == "":  # blank line ends section
				break
			if inside_accel:
				match = pattern.search(line)
				if match:
					ts, x, y, z = match.groups()
					# Convert time: round to 2 decimals, then multiply by 100
					time_val = round(float(ts), 2) * 100
					entry = {
						"time": int(time_val),
						"x": float(x),
						"y": float(y),
						"z": float(z)
					}
					data.append(entry)
	return data

while True:
	d = []
	for x in range(5):
		d = d+parse()
		# time.sleep(2)

	with open("unknown.json", "w") as f:
		json.dump(d, f, indent=2)

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


	features = extract_features("unknown.json")
	prediction = model.predict([features])[0]

	if prediction == 0:
	    print("Normal movement")
	else:
	    print("Seizure detected -", datetime.now().strftime("%H:%M:%S"))
