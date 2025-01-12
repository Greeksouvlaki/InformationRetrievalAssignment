import json

with open('processed_articles.json', 'r', encoding='utf-8') as file:
    processed_articles = json.load(file)

# Λίστα ερωτημάτων
queries = {
    "hulk": [],
    "iron man": [],
    "thor": [],
    "avengers": [],
    "captain america": [],
    "black panther": [],
    "infinity stones": [],
    "guardians of the galaxy": [],
    "loki": [],
    "multiverse": []
}

# Δημιουργία του ground truth χειροκίνητα
for query in queries.keys():
    for article_id, article in enumerate(processed_articles):
        if query in article['title'].lower() or query in " ".join(article['tokens']).lower():
            queries[query].append(article_id)

# Αποθήκευση του ground truth
with open('ground_truth.json', 'w', encoding='utf-8') as file:
    json.dump(queries, file, indent=4, ensure_ascii=False)

print("Ground truth created and saved as 'ground_truth.json'.")
