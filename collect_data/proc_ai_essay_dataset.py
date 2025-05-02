#given csv AI_essays get text and create file to ai_articles folder

import pandas as pd
import os
import re
import csv

def clean(text):
    text = re.sub(r'\s+', ' ', text)  # collapse whitespace
    text = re.sub(r'[^\w\s.,!?]', '', text)  # remove junk chars
    text = re.sub(r'[\d]', '', text)  # remove numbers
    text = re.sub(r'[\n\r]', ' ', text)  # remove new lines
    return text.lower().strip()
def save_text_to_file(text, filename):
    
    with open(os.path.join("./ai_articles", filename), "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved: {filename}")

def main():
    df = pd.read_csv("./collect_data/ai_essays.csv")
    for index, row in df.iterrows():
        full_text = row['text']
        cleaned_text = clean(full_text)

        # Limit the number of files to process
        if index >= 10000:
            break

        filename = f"ai_essay_{index}.txt"
        save_text_to_file(cleaned_text, filename)
    
if __name__ == "__main__":
    main()
