# find how many files are in each folder of ai_articles
import os


for root, dirs, files in os.walk("human_articles"):
        print(f"Number of files: {len(files)}")


for root, dirs, files in os.walk("ai_articles"):
        print(f"Number of files: {len(files)}")

