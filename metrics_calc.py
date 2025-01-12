import json
from search_interface import boolean_search, vsm_search, bm25_search, load_data

# Υπολογισμός Precision, Recall και F1-Score
def evaluate_metrics(retrieved, relevant):
    retrieved = set(retrieved)
    relevant = set(relevant)
    
    precision = len(retrieved & relevant) / len(retrieved) if retrieved else 0
    recall = len(retrieved & relevant) / len(relevant) if relevant else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    
    return precision, recall, f1

# Φόρτωση δεδομένων
with open('ground_truth.json', 'r', encoding='utf-8') as file:
    ground_truth = json.load(file)

with open('processed_articles.json', 'r', encoding='utf-8') as file:
    processed_articles = json.load(file)

inverted_index, _ = load_data()

# Αξιολόγηση με όλους τους αλγορίθμους
results = {}

for query, relevant_docs in ground_truth.items():
    results[query] = {}
    
    # Boolean Search
    boolean_results = boolean_search(query, inverted_index, operation="AND")
    precision, recall, f1 = evaluate_metrics(boolean_results, relevant_docs)
    results[query]["Boolean"] = {"Precision": precision, "Recall": recall, "F1-Score": f1}

    # VSM Search
    vsm_results = vsm_search(query, inverted_index, processed_articles)
    retrieved_docs_vsm = [doc_id for doc_id, _ in vsm_results[:10]]  # Top 10 αποτελέσματα
    precision, recall, f1 = evaluate_metrics(retrieved_docs_vsm, relevant_docs)
    results[query]["VSM"] = {"Precision": precision, "Recall": recall, "F1-Score": f1}

    # BM25 Search
    bm25_results = bm25_search(query, processed_articles)
    retrieved_docs_bm25 = [doc_id for doc_id, _ in bm25_results[:10]]  # Top 10 αποτελέσματα
    precision, recall, f1 = evaluate_metrics(retrieved_docs_bm25, relevant_docs)
    results[query]["BM25"] = {"Precision": precision, "Recall": recall, "F1-Score": f1}

# Εμφάνιση αποτελεσμάτων
for query, metrics in results.items():
    print(f"Query: {query}")
    for method, scores in metrics.items():
        print(f"  Method: {method}")
        for metric, value in scores.items():
            print(f"    {metric}: {value:.2f}")
    print()

# Αποθήκευση αποτελεσμάτων σε αρχείο JSON
with open('evaluation_results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("Evaluation completed and saved as 'evaluation_results.json'.")
