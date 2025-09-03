# live_app.py
import tkinter as tk
from tkinter import messagebox, ttk
import os
import re
import json
import joblib
import numpy as np
import threading
import time

# ---------------- Feature Extraction ----------------
def extract_features(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    x = [d["x"] for d in data]
    y = [d["y"] for d in data]
    z = [d["z"] for d in data]

    features = [
        np.mean(x), np.std(x), np.max(x)-np.min(x),
        np.mean(y), np.std(y), np.max(y)-np.min(y),
        np.mean(z), np.std(z), np.max(z)-np.min(z),
    ]
    return features

# ---------------- Parse Accelerometer Data ----------------
def parse():
    os.system("tools\\adb shell dumpsys sensorservice > file.txt")
    input_file = "file.txt"
    pattern = re.compile(r"\(ts=(\d+\.\d+).*?\)\s+([-\d.]+),\s+([-\d.]+),\s+([-\d.]+)")
    data = []
    with open(input_file, "r") as f:
        inside_accel = False
        for line in f:
            if line.strip().startswith("ACCELEROMETER:"):
                inside_accel = True
                continue
            if inside_accel and line.strip() == "":
                break
            if inside_accel:
                match = pattern.search(line)
                if match:
                    ts, x, y, z = match.groups()
                    time_val = round(float(ts), 2) * 100
                    entry = {
                        "time": int(time_val),
                        "x": float(x),
                        "y": float(y),
                        "z": float(z)
                    }
                    data.append(entry)
    return data

# ---------------- Main App ----------------
class SeizureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seizure Detection ML (Live Mode)")
        self.root.geometry("650x400")
        self.root.configure(bg="#1e1e2e")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 12), padding=6, background="#44475a", foreground="white")
        style.configure("TLabel", background="#1e1e2e", foreground="white", font=("Arial", 12))
        style.configure("TFrame", background="#1e1e2e")

        title = tk.Label(root, text="🧠 Live Seizure Detection ML", font=("Arial", 20, "bold"), bg="#1e1e2e", fg="#ffb86c")
        title.pack(pady=20)

        frame = ttk.Frame(root)
        frame.pack(pady=10)

        # Train + Start Buttons
        train_btn = ttk.Button(frame, text="📚 Train Model", command=self.train_model)
        train_btn.grid(row=0, column=0, padx=10, pady=10)

        start_btn = ttk.Button(frame, text="▶ Start Live Detection", command=self.start_live_detection)
        start_btn.grid(row=0, column=1, padx=10, pady=10)

        stop_btn = ttk.Button(frame, text="⏹ Stop", command=self.stop_live_detection)
        stop_btn.grid(row=0, column=2, padx=10, pady=10)

        # Prediction Label
        self.result_label = tk.Label(root, text="Awaiting action...", font=("Arial", 16), bg="#1e1e2e", fg="white")
        self.result_label.pack(pady=30)

        self.running = False
        self.model = None

    # Train the model
    def train_model(self):
        try:
            if not os.path.exists("norm_real.json") or not os.path.exists("seiz_real.json"):
                messagebox.showerror("Error", "Training files 'norm_real.json' and 'seiz_real.json' are required.")
                return

            X = []
            y = []

            X.append(extract_features("norm_real.json"))
            y.append(0)

            X.append(extract_features("seiz_real.json"))
            y.append(1)

            X = np.array(X)
            y = np.array(y)

            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier()
            model.fit(X, y)

            joblib.dump(model, "real_model.pkl")
            self.model = model

            messagebox.showinfo("Success", "Model trained and saved as 'real_model.pkl'.")
            self.result_label.config(text="✅ Model trained successfully", fg="#50fa7b")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Start live detection
    def start_live_detection(self):
        if not os.path.exists("real_model.pkl"):
            messagebox.showerror("Error", "Train the model first.")
            return
        if self.running:
            return

        self.model = joblib.load("real_model.pkl")
        self.running = True
        threading.Thread(target=self.live_loop, daemon=True).start()
        self.result_label.config(text="🔄 Live detection running...", fg="#f1fa8c")

    # Stop live detection
    def stop_live_detection(self):
        self.running = False
        self.result_label.config(text="⏹ Detection stopped", fg="white")

    # Continuous loop for seizure detection
    def live_loop(self):
        while self.running:
            try:
                d = []
                for _ in range(5):  # collect multiple samples
                    d += parse()
                    time.sleep(1)

                with open("unknown.json", "w") as f:
                    json.dump(d, f, indent=2)

                features = extract_features("unknown.json")
                prediction = self.model.predict([features])[0]

                if prediction == 0:
                    self.update_result("🟢 Normal Movement", "#50fa7b")
                else:
                    self.update_result("🔴 Seizure Detected", "#ff5555")

            except Exception as e:
                self.update_result(f"⚠ Error: {str(e)}", "#ffb86c")

    # Thread-safe UI updates
    def update_result(self, text, color):
        self.result_label.after(0, lambda: self.result_label.config(text=text, fg=color))


# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SeizureApp(root)
    root.mainloop()
