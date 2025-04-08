import os
import re
import html
import pandas as pd

# === CONFIGURATION ===
BASE_DIR = "2_problems"  # your problem root directory
ORIGINAL_FILENAME = "prompt.txt"
CLEANED_FILENAME = "cleaned_prompt.txt"

# === Helper: clean individual constraint line
def parse_constraint_line(line):
    line = re.sub(r"</?(li|code)>", "", line)
    line = re.sub(r"<sup>(\d+)</sup>", r"^\1", line)
    line = html.unescape(line)
    line = re.sub(r"<[^>]+>", "", line)
    return line.strip()

# === Main cleaning logic
def clean_prompt_and_constraints(raw_text):
    # 1. Extract valid constraint lines
    constraint_lines = re.findall(r"<li><code>.*?</code></li>", raw_text)
    parsed_constraints = [parse_constraint_line(line) for line in constraint_lines]

    # 2. Remove broken or duplicated constraint headers
    raw_text = re.sub(r"Constraints:\s*`?.*?\n", "", raw_text)
    raw_text = re.sub(r"Constraints:\s*(\n\s*`?.*`?\s*)*", "", raw_text)

    # 3. General HTML cleanup
    text = html.unescape(raw_text)
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    text = re.sub(r"<pre>(.*?)</pre>", r"```\n\1\n```", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    cleaned_text = text.strip()

    # 4. Append one clean Constraints block
    if parsed_constraints:
        cleaned_text += "\n\nConstraints:\n" + "\n".join(f"- {line}" for line in parsed_constraints)

    # 5. Remove stray lines like "`0", "`10^4", "`1"
    cleaned_text = re.sub(r"\n\s*`[^`\n]+`?\s*\n", "\n", cleaned_text)

    return cleaned_text

# === Batch process all problems
results = []

for level in ["easy", "medium", "hard"]:
    level_path = os.path.join(BASE_DIR, level)
    if not os.path.isdir(level_path):
        continue

    for dp_folder in sorted(os.listdir(level_path)):
        folder_path = os.path.join(level_path, dp_folder)
        prompt_path = os.path.join(folder_path, ORIGINAL_FILENAME)
        cleaned_path = os.path.join(folder_path, CLEANED_FILENAME)

        if not os.path.exists(prompt_path):
            results.append((folder_path, "⚠️ prompt.txt not found"))
            continue

        with open(prompt_path, "r", encoding="utf-8") as f:
            raw = f.read()

        polished = clean_prompt_and_constraints(raw)

        with open(cleaned_path, "w", encoding="utf-8") as f:
            f.write(polished)

        results.append((folder_path, "✅ cleaned_prompt.txt generated"))

# === Summary Output
df = pd.DataFrame(results, columns=["Problem Folder", "Status"])
print(df.to_string(index=False))

try:
    import ace_tools as tools
    tools.display_dataframe_to_user(name="Prompt Cleaning Summary", dataframe=df)
except ImportError:
    pass
