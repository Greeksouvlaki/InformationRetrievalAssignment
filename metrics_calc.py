import json
from search_interface import boolean_search, vsm_search, bm25_search, load_data

# Υπολογισμός Precision, Recall, F1-Score
def evaluate_metrics(retrieved, relevant):
    retrieved = set(retrieved)
    relevant = set(relevant)
    
    precision = len(retrieved & relevant) / len(retrieved) if retrieved else 0
    recall = len(retrieved & relevant) / len(relevant) if relevant else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    
    return precision, recall, f1

# Υπολογισμός Average Precision (AP)
def average_precision(retrieved, relevant):
    relevant = set(relevant)
    if not relevant:
        return 0.0
    
    ap = 0.0
    correct_hits = 0
    
    for i, doc_id in enumerate(retrieved):
        if doc_id in relevant:
            correct_hits += 1
            precision_at_k = correct_hits / (i + 1)
            ap += precision_at_k
    
    return ap / len(relevant)

# Υπολογισμός MAP
def calculate_map(results, ground_truth):
    map_scores = {method: [] for method in results[next(iter(results))].keys()}
    
    for query, query_results in results.items():
        relevant_docs = ground_truth.get(query, [])
        for method, method_results in query_results.items():
            retrieved_docs = method_results.get("retrieved_docs", [])
            ap = average_precision(retrieved_docs, relevant_docs)
            map_scores[method].append(ap)
    
    return {method: sum(scores) / len(scores) for method, scores in map_scores.items()}

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
    results[query]["Boolean"] = {
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "retrieved_docs": list(boolean_results)
    }

    # VSM Search
    vsm_results = vsm_search(query, inverted_index, processed_articles)
    retrieved_docs_vsm = [doc_id for doc_id, _ in vsm_results[:10]]  # Top 10 αποτελέσματα
    precision, recall, f1 = evaluate_metrics(retrieved_docs_vsm, relevant_docs)
    results[query]["VSM"] = {
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "retrieved_docs": retrieved_docs_vsm
    }

    # BM25 Search
    bm25_results = bm25_search(query, processed_articles)
    retrieved_docs_bm25 = [doc_id for doc_id, _ in bm25_results[:10]]  # Top 10 αποτελέσματα
    precision, recall, f1 = evaluate_metrics(retrieved_docs_bm25, relevant_docs)
    results[query]["BM25"] = {
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "retrieved_docs": retrieved_docs_bm25
    }

# Υπολογισμός MAP
map_scores = calculate_map(results, ground_truth)

# Εμφάνιση αποτελεσμάτων
for query, query_results in results.items():
    print(f"Query: {query}")
    for method, metrics in query_results.items():
        print(f"  Method: {method}")
        for metric, value in metrics.items():
            if metric != "retrieved_docs":  # Skip detailed doc lists
                print(f"    {metric}: {value:.2f}")
    print()

print("MAP Scores:")
for method, score in map_scores.items():
    print(f"  {method}: {score:.2f}")

# Αποθήκευση αποτελεσμάτων σε αρχείο JSON
with open('evaluation_results_with_map.json', 'w', encoding='utf-8') as file:
    json.dump({"results": results, "map_scores": map_scores}, file, indent=4, ensure_ascii=False)

print("Evaluation with MAP completed and saved as 'evaluation_results_with_map.json'.")
