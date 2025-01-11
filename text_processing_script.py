import json
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Προεπεξεργασία κειμένου
def preprocess_text(content):
    content = content.lower()
    content = re.sub(r'[^a-z\s]', '', content)
    tokens = word_tokenize(content)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

# Φόρτωση δεδομένων από το αρχείο JSON που δημιουργήθηκε στο Βήμα 1
input_file = 'wikipedia_articles.json'
with open(input_file, 'r', encoding='utf-8') as file:
    wikipedia_articles = json.load(file)

processed_articles = []
metadata = []

# Εφαρμογή προεπεξεργασίας σε κάθε άρθρο
for article in wikipedia_articles:
    processed_content = preprocess_text(article['content'])
    processed_articles.append({
        'title': article['title'],
        'url': article['url'],
        'tokens': processed_content
    })
    metadata.append({
        'title': article['title'],
        'url': article['url'],
        'token_count': len(processed_content),
        'unique_token_count': len(set(processed_content))
    })

# Αποθήκευση καθαρισμένων δεδομένων σε JSON
output_file = 'processed_articles.json'
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(processed_articles, file, indent=4, ensure_ascii=False)

# Αποθήκευση μεταδεδομένων σε JSON
metadata_file = 'articles_metadata.json'
with open(metadata_file, 'w', encoding='utf-8') as file:
    json.dump(metadata, file, indent=4, ensure_ascii=False)

print("Data processing complete. Processed articles and metadata saved.")
