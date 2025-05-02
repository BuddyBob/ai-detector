from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")

PROMPTS = [
    "Impact of AI on jobs",
    "How to start a business",
    "Benefits of meditation",
    "Gun control debate in the US",
    "Is college worth it?",
    "What is happiness?",
    "Is nuclear power sustainable?",
    "Is capitalism flawed?"
]

def search_articles(query, start, num_results=10):
    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY,
        "num": num_results,
        "start": start
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return [r['link'] for r in results.get('organic_results', [])]

def collect_all_links():
    seen_links = set()

    with open("human_article_links.txt", "a", encoding="utf-8") as f:
        for prompt in PROMPTS:
            print(f"Searching: {prompt}")
            for i in range(0, 50, 10):  # 5 pages = ~50 results per prompt
                try:
                    links = search_articles(prompt, start=i)
                    new_links = [link for link in links if link not in seen_links]

                    for link in new_links:
                        seen_links.add(link)
                        f.write(link + "\n")
                        print(f"  [+] {link}")
                    
                    time.sleep(1) 
                except Exception as e:
                    print(f"Failed on '{prompt}' page {i//10 + 1}: {e}")
                    time.sleep(2)

    print(f"Total unique links collected: {len(seen_links)}")

if __name__ == "__main__":
    collect_all_links()
