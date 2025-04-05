import json
import os
import random

# === Configuration ===
INPUT_FILE = "dataset_with_difficulty_and_algorithm.json"
OUTPUT_FILE = "3_data\selected_dp_problems.json"
MAX_PER_LEVEL = 10

# === Step 1: Load the dataset ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# === Step 2: Filter for dynamic programming problems ===
dp_problems = [
    prob for prob in dataset
    if "algorithms" in prob and isinstance(prob["algorithms"], list)
    and "dynamic_programming" in [a.lower().replace(" ", "_") for a in prob["algorithms"]]
]

# === Step 3: Group by difficulty ===
grouped = {
    "Easy": [p for p in dp_problems if p.get("difficulty") == "Easy"],
    "Medium": [p for p in dp_problems if p.get("difficulty") == "Medium"],
    "Hard": [p for p in dp_problems if p.get("difficulty") == "Hard"]
}

# === Step 4: Select up to 10 problems from each level ===
selected = {
    level: random.sample(probs, min(len(probs), MAX_PER_LEVEL))
    for level, probs in grouped.items()
}

# === Step 5: Save to output file ===
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(selected, f, indent=2)

# === Step 6: Print Summary ===
print("✅ Selected DP Problems by Difficulty:")
for level in ["Easy", "Medium", "Hard"]:
    print(f"  - {level}: {len(selected[level])} problems selected")
