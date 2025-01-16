import tkinter as tk
from tkinter import ttk, messagebox
from search_interface import boolean_search, vsm_search, bm25_search, compute_tfidf, load_data

# Φόρτωση δεδομένων
inverted_index, processed_articles = load_data()

# Χρωματική παλέτα Marvel
PRIMARY_COLOR = "#ED1D24"  # Κόκκινο της Marvel
SECONDARY_COLOR = "#FFFFFF"  # Λευκό
ACCENT_COLOR = "#FFCC00"  # Κίτρινο
BG_COLOR = "#1B1B1B"  # Μαύρο φόντο

# Συνάρτηση για αναζήτηση
def perform_search(query, retrieval_method, operation=None):
    if not query.strip():
        messagebox.showerror("Error", "Please enter a query.")
        return

    if retrieval_method == "Boolean":
        if operation not in {"AND", "OR", "NOT"}:
            messagebox.showerror("Error", "Invalid Boolean operation. Choose AND, OR, or NOT.")
            return
        results = boolean_search(query, inverted_index, operation)
    elif retrieval_method == "VSM":
        results = vsm_search(query, inverted_index, processed_articles)
    elif retrieval_method == "BM25":
        results = bm25_search(query, processed_articles)
    elif retrieval_method == "TF-IDF":
        results = compute_tfidf(query, inverted_index, processed_articles)
    else:
        messagebox.showerror("Error", "Invalid retrieval method selected.")
        return

    display_results(results, retrieval_method)

# Εμφάνιση αποτελεσμάτων
def display_results(results, method):
    results_window = tk.Toplevel(root)
    results_window.title(f"Results - {method}")
    results_window.configure(bg=BG_COLOR)

    tk.Label(results_window, text=f"Results for {method} Retrieval", bg=BG_COLOR, fg=SECONDARY_COLOR,
             font=("Helvetica", 16, "bold")).pack(pady=10)

    result_list = tk.Listbox(results_window, bg=BG_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 12), width=80)
    result_list.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    if isinstance(results, set):  # Boolean results
        for doc_id in results:
            result_list.insert(tk.END, processed_articles[doc_id]['title'])
    else:  # Ranked results
        for doc_id, score in results[:10]:  # Show top 10 results
            result_list.insert(tk.END, f"{processed_articles[doc_id]['title']} (Score: {score:.4f})")

    tk.Button(results_window, text="Close", bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 12, "bold"),
              command=results_window.destroy).pack(pady=10)

# Δημιουργία κύριου παραθύρου
root = tk.Tk()
root.title("Marvel Search Engine")
root.geometry("800x600")
root.configure(bg=BG_COLOR)

# Επικεφαλίδα
header = tk.Label(root, text="Marvel Search Engine", bg=PRIMARY_COLOR, fg=SECONDARY_COLOR,
                   font=("Helvetica", 24, "bold"), pady=10)
header.pack(fill=tk.X)

# Πεδίο εισαγωγής ερωτήματος
query_label = tk.Label(root, text="Enter your search query:", bg=BG_COLOR, fg=SECONDARY_COLOR,
                        font=("Helvetica", 14))
query_label.pack(pady=10)

query_entry = tk.Entry(root, font=("Helvetica", 14), width=50)
query_entry.pack(pady=5)

# Επιλογές μεθόδου ανάκτησης
method_label = tk.Label(root, text="Choose retrieval method:", bg=BG_COLOR, fg=SECONDARY_COLOR,
                         font=("Helvetica", 14))
method_label.pack(pady=10)

method_var = tk.StringVar(value="Boolean")
methods = ["Boolean", "VSM", "BM25", "TF-IDF"]
method_menu = ttk.Combobox(root, textvariable=method_var, values=methods, state="readonly", font=("Helvetica", 12))
method_menu.pack(pady=5)

# Επιλογή Boolean λειτουργίας
boolean_label = tk.Label(root, text="Boolean Operation (for Boolean Retrieval):", bg=BG_COLOR, fg=SECONDARY_COLOR,
                          font=("Helvetica", 14))
boolean_label.pack(pady=10)

boolean_var = tk.StringVar(value="AND")
boolean_menu = ttk.Combobox(root, textvariable=boolean_var, values=["AND", "OR", "NOT"], state="readonly",
                             font=("Helvetica", 12))
boolean_menu.pack(pady=5)

# Κουμπί αναζήτησης
search_button = tk.Button(root, text="Search", bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=("Helvetica", 14, "bold"),
                           command=lambda: perform_search(query_entry.get(), method_var.get(), boolean_var.get()))
search_button.pack(pady=20)

# Πληροφορίες
info_label = tk.Label(root, text="Powered by the Marvel Universe", bg=BG_COLOR, fg=ACCENT_COLOR,
                       font=("Helvetica", 12, "italic"))
info_label.pack(side=tk.BOTTOM, pady=10)

# Εκκίνηση της εφαρμογής
root.mainloop()
