def calculate_map(results, ground_truth):
    """
    Υπολογισμός MAP για όλα τα ερωτήματα.
    
    results: Dictionary με αποτελέσματα ανά μέθοδο και ερώτημα.
    ground_truth: Dictionary με τα σχετικά έγγραφα ανά ερώτημα.
    """
    def average_precision(retrieved, relevant):
        retrieved = list(retrieved)
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

    map_scores = {method: [] for method in results[next(iter(results))].keys()}
    
    for query, query_results in results.items():
        relevant_docs = ground_truth.get(query, [])
        for method, method_results in query_results.items():
            retrieved_docs = method_results.get("retrieved_docs", [])
            ap = average_precision(retrieved_docs, relevant_docs)
            map_scores[method].append(ap)
    
    return {method: sum(scores) / len(scores) for method, scores in map_scores.items()}

