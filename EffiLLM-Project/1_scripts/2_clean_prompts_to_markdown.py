import os
import re

# === CONFIGURATION ===
BASE_DIR = "2_problems"

# === HTML TAG STRIPPER ===
def strip_html_tags(text):
    # Replace <code> with backticks
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL)
    # Replace <pre> blocks with triple backticks
    text = re.sub(r"<pre>(.*?)</pre>", r"```\n\1\n```", text, flags=re.DOTALL)
    # Strip all other tags (like <p>, <strong>)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()

# === Walk through problems folders ===
for level in ["easy", "medium", "hard"]:
    level_path = os.path.join(BASE_DIR, level)
    if not os.path.isdir(level_path):
        continue

    for dp_folder in os.listdir(level_path):
        folder_path = os.path.join(level_path, dp_folder)
        prompt_path = os.path.join(folder_path, "prompt.txt")
        cleaned_path = os.path.join(folder_path, "cleaned_prompt.txt")

        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                raw = f.read()
            cleaned = strip_html_tags(raw)

            with open(cleaned_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            print(f"✅ Cleaned prompt saved: {cleaned_path}")
        else:
            print(f"⚠️ prompt.txt not found in: {folder_path}")
