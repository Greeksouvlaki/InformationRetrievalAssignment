import json
import matplotlib.pyplot as plt
import numpy as np

# Φόρτωση αποτελεσμάτων
with open('evaluation_results.json', 'r', encoding='utf-8') as file:
    results = json.load(file)

# Λίστα ερωτημάτων
queries = list(results.keys())

# Μέθοδοι αναζήτησης
methods = ["Boolean", "VSM", "BM25"]

# Προετοιμασία δεδομένων για τα γραφήματα
precision_data = {method: [] for method in methods}
recall_data = {method: [] for method in methods}
f1_data = {method: [] for method in methods}

for query in queries:
    for method in methods:
        precision_data[method].append(results[query][method]["Precision"])
        recall_data[method].append(results[query][method]["Recall"])
        f1_data[method].append(results[query][method]["F1-Score"])

# Δημιουργία γραφημάτων Precision και Recall
x = np.arange(len(queries))  # Θέσεις στον άξονα Χ
width = 0.25  # Πλάτος γραμμής

plt.figure(figsize=(12, 6))

# Precision
plt.bar(x - width, precision_data["Boolean"], width, label="Boolean Precision")
plt.bar(x, precision_data["VSM"], width, label="VSM Precision")
plt.bar(x + width, precision_data["BM25"], width, label="BM25 Precision")

plt.title("Precision ανά Ερώτημα και Μέθοδο")
plt.xlabel("Ερωτήματα")
plt.ylabel("Precision")
plt.xticks(x, queries, rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()

# Recall
plt.figure(figsize=(12, 6))
plt.bar(x - width, recall_data["Boolean"], width, label="Boolean Recall")
plt.bar(x, recall_data["VSM"], width, label="VSM Recall")
plt.bar(x + width, recall_data["BM25"], width, label="BM25 Recall")

plt.title("Recall ανά Ερώτημα και Μέθοδο")
plt.xlabel("Ερωτήματα")
plt.ylabel("Recall")
plt.xticks(x, queries, rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()

# F1-Score
plt.figure(figsize=(12, 6))
plt.bar(x - width, f1_data["Boolean"], width, label="Boolean F1-Score")
plt.bar(x, f1_data["VSM"], width, label="VSM F1-Score")
plt.bar(x + width, f1_data["BM25"], width, label="BM25 F1-Score")

plt.title("F1-Score ανά Ερώτημα και Μέθοδο")
plt.xlabel("Ερωτήματα")
plt.ylabel("F1-Score")
plt.xticks(x, queries, rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()
