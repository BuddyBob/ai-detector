from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
GEMENI_API_KEY = os.getenv("GEMENI_API_KEY")
client = genai.Client(api_key=GEMENI_API_KEY)

topics = [
    "The pros and cons of remote work",
    "Why startups fail and what to learn from them",
    "Should you pursue an MBA in 2025?",
    "The gig economy and worker rights",
    "The impact of automation on small businesses",
    "What makes a great product manager?",
    "How to build emotional resilience",
    "Why do people self-sabotage?",
    "How journaling changes your brain",
    "The science behind procrastination",
    "Can happiness be measured?",
    "The psychology of motivation",
    "How to overcome imposter syndrome",
    "The ethics of universal basic income",
    "Can democracy survive the digital age?",
    "Should voting be mandatory?",
    "How misinformation spreads on social media",
    "Are we too dependent on technology?",
    "Is free speech under threat?",
    "The future of work in a post-capitalist world",
    "Is nuclear fusion the future of energy?",
    "Why biodiversity matters more than you think",
    "The risks and benefits of gene editing",
    "How climate change affects mental health",
    "Are electric vehicles truly sustainable?",
    "The race to colonize Mars",
    "What happens if the bees disappear?",
    "Should college be free for everyone?",
    "Is the traditional school model outdated?",
    "How AI tutors are reshaping education",
    "The benefits of learning a second language",
    "How to cultivate a love for reading",
    "The case for coding in elementary schools",
    "The downsides of standardized testing",
    "Do we have free will?",
    "Can AI be conscious?",
    "What does it mean to live a meaningful life?",
    "Is morality relative or universal?",
    "Should we trust our intuition?",
    "What is the value of suffering?",
    "Can machines be creative?"
]

# Article generation logic
def generate_article(topic):
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-04-17",
        contents=f"Write a 500-word article on '{topic}' as if you were a human journalist or blogger. Make it sound natural and authentic, like a Medium or Quora post. Avoid repeating phrases or using too-perfect grammar.",
        config=types.GenerateContentConfig(
            system_instruction="You are a human journalist or blogger. You write for an online audience. Keep it authentic and natural. Avoid robotic tone and excessive repetition."
        )
    )
    return response.text.strip()

# Save to file
def write_to_file(filename, text):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✓ Saved: {filename}")

# Main generation loop
def main(topic):
    for i in range(1): # Could generate more than one per topic
        print(f"→ Generating Article for: {topic}")
        article_text = generate_article(topic)
        cleaned_text = article_text.replace("\n", " ").replace("\r", " ").strip()
        filename = f"../ai_articles/{topic.replace(' ', '_').replace('?', '')}_{i}.txt"
        write_to_file(filename, cleaned_text)

if __name__ == "__main__":
    for topic in topics:
        main(topic)
