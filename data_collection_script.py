import requests
from bs4 import BeautifulSoup
import json

# Λίστα URLs για συλλογή άρθρων από Wikipedia
wikipedia_urls = [
    # Γενικά άρθρα
    "https://en.wikipedia.org/wiki/Marvel_Cinematic_Universe",
    "https://en.wikipedia.org/wiki/Marvel_Studios",
    
    # Ταινίες MCU
    "https://en.wikipedia.org/wiki/Iron_Man_(2008_film)",
    "https://en.wikipedia.org/wiki/The_Incredible_Hulk_(film)",
    "https://en.wikipedia.org/wiki/Iron_Man_2",
    "https://en.wikipedia.org/wiki/Thor_(film)",
    "https://en.wikipedia.org/wiki/Captain_America:_The_First_Avenger",
    "https://en.wikipedia.org/wiki/The_Avengers_(2012_film)",
    "https://en.wikipedia.org/wiki/Iron_Man_3",
    "https://en.wikipedia.org/wiki/Thor:_The_Dark_World",
    "https://en.wikipedia.org/wiki/Captain_America:_The_Winter_Soldier",
    "https://en.wikipedia.org/wiki/Guardians_of_the_Galaxy_(film)",
    "https://en.wikipedia.org/wiki/Avengers:_Age_of_Ultron",
    "https://en.wikipedia.org/wiki/Ant-Man_(film)",
    "https://en.wikipedia.org/wiki/Captain_America:_Civil_War",
    "https://en.wikipedia.org/wiki/Doctor_Strange_(2016_film)",
    "https://en.wikipedia.org/wiki/Guardians_of_the_Galaxy_Vol._2",
    "https://en.wikipedia.org/wiki/Spider-Man:_Homecoming",
    "https://en.wikipedia.org/wiki/Thor:_Ragnarok",
    "https://en.wikipedia.org/wiki/Black_Panther_(film)",
    "https://en.wikipedia.org/wiki/Avengers:_Infinity_War",
    "https://en.wikipedia.org/wiki/Ant-Man_and_the_Wasp",
    "https://en.wikipedia.org/wiki/Captain_Marvel_(film)",
    "https://en.wikipedia.org/wiki/Avengers:_Endgame",
    "https://en.wikipedia.org/wiki/Spider-Man:_Far_From_Home",
    "https://en.wikipedia.org/wiki/Black_Widow_(2021_film)",
    "https://en.wikipedia.org/wiki/Shang-Chi_and_the_Legend_of_the_Ten_Rings",
    "https://en.wikipedia.org/wiki/Eternals_(film)",
    "https://en.wikipedia.org/wiki/Spider-Man:_No_Way_Home",
    "https://en.wikipedia.org/wiki/Doctor_Strange_in_the_Multiverse_of_Madness",
    "https://en.wikipedia.org/wiki/Thor:_Love_and_Thunder",
    "https://en.wikipedia.org/wiki/Black_Panther:_Wakanda_Forever",
    "https://en.wikipedia.org/wiki/Ant-Man_and_the_Wasp:_Quantumania",
    "https://en.wikipedia.org/wiki/Guardians_of_the_Galaxy_Vol._3",
    
    # Σειρές MCU
    "https://en.wikipedia.org/wiki/WandaVision",
    "https://en.wikipedia.org/wiki/The_Falcon_and_the_Winter_Soldier",
    "https://en.wikipedia.org/wiki/Loki_(TV_series)",
    "https://en.wikipedia.org/wiki/What_If...%3F_(TV_series)",
    "https://en.wikipedia.org/wiki/Hawkeye_(TV_series)",
    "https://en.wikipedia.org/wiki/Moon_Knight_(TV_series)",
    "https://en.wikipedia.org/wiki/Ms._Marvel_(TV_series)",
    "https://en.wikipedia.org/wiki/She-Hulk:_Attorney_at_Law",
    "https://en.wikipedia.org/wiki/Secret_Invasion_(TV_series)",
    "https://en.wikipedia.org/wiki/Echo_(TV_series)",
    "https://en.wikipedia.org/wiki/Ironheart_(TV_series)",
    "https://en.wikipedia.org/wiki/Agatha:_Darkhold_Diaries"
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
