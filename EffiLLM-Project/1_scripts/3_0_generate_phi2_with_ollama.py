import os
import subprocess
import re

# === CONFIGURATION ===
BASE_DIR = "2_problems"
LEVELS = ["easy", "medium", "hard"]
MODEL = "phi"
TEMPERATURE = 0.2

# === Extract function name from human.py
def extract_method_name(human_code):
    match = re.search(r"def (\w+)\s*\(", human_code)
    return match.group(1) if match else None

# === Wrap function in class Solution
def wrap_in_class(function_code, method_name):
    lines = function_code.strip().split("\n")
    if lines[0].strip().startswith("class Solution"):
        return function_code  # Already wrapped

    indented = ["    " + line if line.strip() else "" for line in lines]
    return f"class Solution:\n" + "\n".join(indented)

# === Main Phi-2 Generator Function
def generate_code(prompt, method_name):
    system_prompt = (
        "You are an expert competitive programmer. Generate only the Python code that solves the problem, "
        "using the same function name as shown, wrapped inside `class Solution`. "
        "Do not output explanations, comments, or alternative languages."
    )

    full_prompt = f"{system_prompt}\n\n{prompt}\n\nReturn only Python code."

    try:
        result = subprocess.run(
            ["ollama", "run", MODEL],
            input=full_prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=240
        )
        output = result.stdout.decode("utf-8")

        # Strip non-code blocks
        code_match = re.findall(r"```(?:python)?\s*(.*?)```", output, re.DOTALL)
        code = code_match[0] if code_match else output

        # Ensure wrapping in class
        final_code = wrap_in_class(code, method_name)

        return final_code.strip()

    except Exception as e:
        return f"# ⚠️ Generation error: {e}"

# === Process All Problems
for level in LEVELS:
    level_path = os.path.join(BASE_DIR, level)
    if not os.path.isdir(level_path):
        continue

    for dp_folder in sorted(os.listdir(level_path)):
        problem_path = os.path.join(level_path, dp_folder)
        cleaned_prompt_path = os.path.join(problem_path, "cleaned_prompt.txt")
        human_code_path = os.path.join(problem_path, "human.py")
        phi2_code_path = os.path.join(problem_path, "phi2.py")

        if not os.path.exists(cleaned_prompt_path) or not os.path.exists(human_code_path):
            print(f"⚠️ Skipping {dp_folder} — prompt or human.py missing")
            continue

        with open(cleaned_prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()

        with open(human_code_path, "r", encoding="utf-8") as f:
            human_code = f.read()

        method_name = extract_method_name(human_code)
        if not method_name:
            print(f"❌ Could not extract method name from {dp_folder}")
            continue

        print(f"🚀 Generating for {dp_folder} → method: `{method_name}`")

        solution = generate_code(prompt, method_name)

        with open(phi2_code_path, "w", encoding="utf-8") as f:
            f.write(f"# Generated by Phi-2 via Ollama\n\n{solution}\n")

        print(f"✅ Saved to {phi2_code_path}")
