#seperate the label from the data
import pandas as pd
import numpy as np
import os
import json

import re

def clean(text):
    text = re.sub(r'\s+', ' ', text)  # collapse whitespace
    text = re.sub(r'[^\w\s.,!?]', '', text)  # remove junk chars
    text = re.sub(r'[\d]', '', text)  # remove numbers
    text = re.sub(r'[\n\r]', ' ', text)  # remove new lines
    return text.lower().strip()



#Label PD 0 - AI 1 - Human
def create_dataframe(ai_articles, human_articles):
    min_len = min(len(ai_articles), len(human_articles))
    ai_articles = ai_articles[:min_len]
    human_articles = human_articles[:min_len]

    if len(ai_articles) != len(human_articles):
        print("AI ARTICLES AND HUMAN ARTICLES DO NOT MATCH IN LENGTH")
        return None
    
    print(f"Using {min_len} AI and {min_len} human articles.")

    data = []
    for i in range(len(ai_articles)):
        data.append({'text': ai_articles[i],'label': 0})
        data.append({'text': human_articles[i],'label': 1})
    df = pd.DataFrame(data)
    return df


def load_articles_from_folder(folder):
    articles = []
    for root, _, files in os.walk(folder):
        for file in files:
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                text = f.read()
                articles.append(clean(text))
    return articles

def save_dataframe_to_json(df, output_path):
    df.to_json(output_path, orient='records', lines=True)
    print(f"📝 Dataframe saved to {output_path}")

def main():
    ai_articles = load_articles_from_folder("ai_articles")
    human_articles = load_articles_from_folder("human_articles")

    if len(ai_articles) != len(human_articles):
        print(f"Mismatch: AI = {len(ai_articles)}, Human = {len(human_articles)} → truncating to match.")

    df = create_dataframe(ai_articles, human_articles)
    save_dataframe_to_json(df, "articles.json")
    print(df.head())

if __name__ == "__main__":
    main()



