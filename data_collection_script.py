import requests
from bs4 import BeautifulSoup
import json

# Λίστα URLs για συλλογή άρθρων από Wikipedia
wikipedia_urls = [
    "https://en.wikipedia.org/wiki/Web_scraping",
    "https://en.wikipedia.org/wiki/Data_mining",
    "https://en.wikipedia.org/wiki/Natural_language_processing"
]

# Συνάρτηση για συλλογή δεδομένων από άρθρο Wikipedia
def fetch_wikipedia_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Έλεγχος αν η σελίδα είναι προσβάσιμη

        soup = BeautifulSoup(response.content, 'html.parser')

        # Τίτλος άρθρου
        title = soup.find('h1').text

        # Περιεχόμενο άρθρου (παράγραφοι)
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.text for p in paragraphs if p.text])

        return {'title': title, 'url': url, 'content': content}

    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
        return None

# Συλλογή δεδομένων από τα URLs
collected_articles = []

for url in wikipedia_urls:
    article = fetch_wikipedia_article(url)
    if article:
        collected_articles.append(article)

# Αποθήκευση δεδομένων σε JSON αρχείο
output_file = 'wikipedia_articles.json'
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(collected_articles, file, indent=4, ensure_ascii=False)

print(f"Articles saved successfully to {output_file}")
