#given csv withheader style essay_id,full_text,score write text to human_articles folder
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
    os.makedirs("human_articles", exist_ok=True)
    with open(os.path.join("human_articles", filename), "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved: {filename}")

def main():
    # Load the CSV file
    #OOPS downloads way too many files definetly add a limit

    df = pd.read_csv("human_essays.csv")
    for index, row in df.iterrows():
        essay_id = row['essay_id']
        full_text = row['full_text']
        cleaned_text = clean(full_text)
        filename = f"{essay_id}.txt"
        save_text_to_file(cleaned_text, filename)

        if index >= 10000:
            break


if __name__ == "__main__":
    main()
    