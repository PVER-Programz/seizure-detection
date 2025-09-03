#with open("file.txt") as f:
#	con = f.read()


#print(con[con.find("ACCELEROMETER:"):con.find("AMD:")])
import re
import json
import time
import os


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

d = []
for x in range(5):
	d = d+parse()
	time.sleep(2)
print(d)
print(len(d))


with open("unknown_real.json", "w") as f:
	json.dump(d, f, indent=2)

# print(f"Extracted {len(data)} accelerometer readings into {output_file}")

# while True:
# 	p=parse()
# 	try:
# 		for x in p:
# 			d = {"time": x['time'], 'x':x['x'], 'y': x['y'], 'z': x['z']}
# 			with open("seiz_real.json", "a") as f:
# 				json.dump(d, f, indent=4)
# 				f.write(",")
# 	except:
# 		pass