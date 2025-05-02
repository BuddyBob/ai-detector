import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""

    # Check for <p> tags and extract
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    if not paragraphs:
        return ' '.join(soup.stripped_strings)

    return ' '.join([p.get_text(strip=True) for p in paragraphs])



# Clean url to be file name friendly
def clean_url(url):
    if url.endswith('/'):
        url = url[:-1]

    url = url[::-1]
    url = url[0:url.find('/')]
    url = url[::-1]
    return url


def main():
    article_links = []
    with open("human_article_links.txt", "r") as f:
        article_links = f.readlines()
    article_links = [link.strip() for link in article_links]

    for link in article_links:
        text = extract_text_from_url(link)
        if text:
            print(f"Extracted text from {link}")
            filename = clean_url(link)
            with open(f"../human_articles/{filename}.txt", "a") as f:
                f.write(text + "\n")
        else:
            print(f"Failed to extract text from {link}")
    


# Example usage
if __name__ == "__main__":
    main()