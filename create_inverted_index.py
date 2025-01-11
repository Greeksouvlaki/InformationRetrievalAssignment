import json
from collections import defaultdict

# Φόρτωση των προεπεξεργασμένων άρθρων
with open('processed_articles.json', 'r', encoding='utf-8') as file:
    processed_articles = json.load(file)

# Δημιουργία του ανεστραμμένου ευρετηρίου
inverted_index = defaultdict(list)

for article_id, article in enumerate(processed_articles):
    for token in set(article['tokens']):
        inverted_index[token].append(article_id)

# Αποθήκευση του ευρετηρίου σε αρχείο
with open('inverted_index.json', 'w', encoding='utf-8') as file:
    json.dump(inverted_index, file, indent=4, ensure_ascii=False)

print("Inverted index created and saved successfully.")
