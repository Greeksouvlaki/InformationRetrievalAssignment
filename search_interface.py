import json
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re

# Φόρτωση δεδομένων
def load_data():
    with open('inverted_index.json', 'r', encoding='utf-8') as file:
        inverted_index = json.load(file)

    with open('processed_articles.json', 'r', encoding='utf-8') as file:
        processed_articles = json.load(file)
    
    return inverted_index, processed_articles

# Προεπεξεργασία ερωτήματος
def preprocess_query(query):
    query = query.lower()
    query = re.sub(r'[^a-z\s]', '', query)
    tokens = word_tokenize(query)
    stop_words = set(stopwords.words('english'))
    return [word for word in tokens if word not in stop_words]

# Boolean αναζήτηση με υποστήριξη AND, OR, NOT
def boolean_search(query, index, operation="AND"):
    tokens = preprocess_query(query)
    print(f"Query Tokens: {tokens}")
    
    if not tokens:
        return set()

    if operation == "AND":
        results = set(index.get(tokens[0], []))
        for token in tokens[1:]:
            results = results.intersection(set(index.get(token, [])))
    elif operation == "OR":
        results = set()
        for token in tokens:
            results = results.union(set(index.get(token, [])))
    elif operation == "NOT":
        results = set(range(len(processed_articles)))
        for token in tokens:
            results = results.difference(set(index.get(token, [])))
    else:
        raise ValueError("Unsupported operation. Use 'AND', 'OR', or 'NOT'.")
    
    return results

def compute_tfidf(query, index, documents, threshold=0.01):
    query_tokens = preprocess_query(query)
    print(f"TF-IDF Query Tokens: {query_tokens}")
    N = len(documents)
    scores = {doc_id: 0 for doc_id in range(N)}
    
    for token in query_tokens:
        if token in index:
            doc_ids = index[token]
            idf = math.log((N + 1) / (len(doc_ids) + 1)) + 1
            print(f"Token: {token}, IDF: {idf}, Document IDs: {doc_ids}")
            
            for doc_id in doc_ids:
                tf = documents[doc_id]['tokens'].count(token) / len(documents[doc_id]['tokens'])
                print(f"Token: {token}, Doc ID: {doc_id}, TF: {tf}")
                scores[doc_id] += tf * idf
                print(f"Doc ID: {doc_id}, Current Score: {scores[doc_id]}")
        else:
            print(f"Token: {token} not found in the index.")
    
    ranked_scores = [(doc_id, score) for doc_id, score in scores.items() if score > threshold]
    return sorted(ranked_scores, key=lambda item: item[1], reverse=True)

# ενσωμάτωση Vector Space Model (VSM) για την ανάκτηση των κορυφαίων αποτελεσμάτων

import numpy as np

# Υπολογισμός cosine similarity για VSM
def vsm_search(query, index, documents):
    query_tokens = preprocess_query(query)
    print(f"VSM Query Tokens: {query_tokens}")

    # Υπολογισμός IDF
    N = len(documents)
    idf = {token: math.log((N + 1) / (len(index.get(token, [])) + 1)) + 1 for token in query_tokens}

    # Δημιουργία διανυσμάτων για κάθε έγγραφο
    document_vectors = []
    for doc_id, doc in enumerate(documents):
        doc_vector = [doc['tokens'].count(token) * idf.get(token, 0) for token in query_tokens]
        document_vectors.append(doc_vector)

    # Δημιουργία διανύσματος ερωτήματος
    query_vector = [idf.get(token, 0) for token in query_tokens]

    # Υπολογισμός cosine similarity
    similarities = []
    for doc_id, doc_vector in enumerate(document_vectors):
        dot_product = np.dot(query_vector, doc_vector)
        norm_query = np.linalg.norm(query_vector)
        norm_doc = np.linalg.norm(doc_vector)
        similarity = dot_product / (norm_query * norm_doc) if norm_query and norm_doc else 0
        similarities.append((doc_id, similarity))

    return sorted(similarities, key=lambda x: x[1], reverse=True)

# okabi BM25 για την ανάκτηση των κορυφαίων αποτελεσμάτων

from rank_bm25 import BM25Okapi

# Επεξεργασία δεδομένων για BM25
def prepare_bm25_data(documents):
    return [doc['tokens'] for doc in documents]

# Αναζήτηση με Okapi BM25
def bm25_search(query, documents):
    tokenized_docs = prepare_bm25_data(documents)
    bm25 = BM25Okapi(tokenized_docs)
    query_tokens = preprocess_query(query)
    print(f"BM25 Query Tokens: {query_tokens}")
    scores = bm25.get_scores(query_tokens)
    return sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

# Διεπαφή αναζήτησης
def search_interface():
    inverted_index, processed_articles = load_data()
    print("Welcome to the Search Engine!")
    print("Enter your query (or type 'exit' to quit):")

    while True:
        query = input("\n> ").strip()
        if query.lower() == 'exit':
            print("Exiting the search engine. Goodbye!")
            break

        print("\nChoose retrieval method:")
        print("1. Boolean Retrieval (AND, OR, NOT)")
        print("2. Vector Space Model (VSM)")
        print("3. Okapi BM25")
        choice = input("\nEnter your choice (1/2/3): ").strip()

        if choice == "1":
            print("\nAvailable Boolean operations: AND, OR, NOT")
            operation = input("Enter Boolean operation: ").strip().upper()
            if operation not in {"AND", "OR", "NOT"}:
                print("Invalid operation. Please try again.")
                continue
            results = boolean_search(query, inverted_index, operation)
        elif choice == "2":
            results = vsm_search(query, inverted_index, processed_articles)
        elif choice == "3":
            results = bm25_search(query, processed_articles)
        else:
            print("Invalid choice. Please try again.")
            continue

        print("\nTop Results:")
        if isinstance(results, set):  # Boolean results
            for doc_id in results:
                print(f"- {processed_articles[doc_id]['title']}")
        else:  # Ranked results
            for doc_id, score in results[:5]:  # Display top 5
                print(f"- {processed_articles[doc_id]['title']} (Score: {score:.4f})")


# Εκκίνηση διεπαφής
if __name__ == "__main__":
    search_interface()
