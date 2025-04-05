import json
import os

# === Configuration ===
INPUT_FILE = "3_data\selected_dp_problems.json"
BASE_OUTPUT_DIR = "2_problems"

# === Helper: Save text to file ===
def save_to_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() if content else "")

# === Load selected problems ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    selected = json.load(f)

# === Process each difficulty level ===
for level in ["Easy", "Medium", "Hard"]:
    problems = selected.get(level, [])
    for i, prob in enumerate(problems, 1):
        # Create folder: problems/easy/dp_001
        folder = os.path.join(BASE_OUTPUT_DIR, level.lower(), f"dp_{i:03}")
        os.makedirs(folder, exist_ok=True)

        # Save prompt.txt
        prompt_path = os.path.join(folder, "prompt.txt")
        save_to_file(prompt_path, prob.get("description", ""))

        # Prepare solution with problem name as comment
        problem_name = prob.get("task_name", "Unknown Problem")
        canonical_solution = prob.get("canonical_solution", "")
        full_solution = f"# Problem: {problem_name}\n\n{canonical_solution}"

        # Save human.py
        solution_path = os.path.join(folder, "human.py")
        save_to_file(solution_path, full_solution)

print("✅ Problem folders with prompt.txt and human.py created (with problem name in comments).")

