import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
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
            messagebox.showerror("Error", "Invalid Boolean operation. Choose AND, OR, NOT.")
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

    display_results(results)

# Εμφάνιση αποτελεσμάτων στο ίδιο παράθυρο
def display_results(results):
    result_list.delete(0, tk.END)  # Καθαρισμός προηγούμενων αποτελεσμάτων

    if isinstance(results, set):  # Boolean results
        for doc_id in results:
            result_list.insert(tk.END, processed_articles[doc_id]['title'])
    else:  # Ranked results
        for doc_id, score in results[:10]:  # Show top 10 results
            result_list.insert(tk.END, f"{processed_articles[doc_id]['title']} (Score: {score:.4f})")

# Δημιουργία κύριου παραθύρου
root = tk.Tk()
root.title("Marvel Search Engine")
root.geometry("800x700")
root.configure(bg=BG_COLOR)

# Στυλ για μοντέρνα widgets
style = ttk.Style()
style.configure("TButton", background=PRIMARY_COLOR, foreground=SECONDARY_COLOR, font=("Helvetica", 12, "bold"))
style.configure("TLabel", background=BG_COLOR, foreground=SECONDARY_COLOR, font=("Helvetica", 14))
style.configure("TCombobox", background=PRIMARY_COLOR, foreground=SECONDARY_COLOR, font=("Helvetica", 12))

# Επικεφαλίδα με λογότυπο
header_frame = tk.Frame(root, bg=BG_COLOR)
header_frame.pack(fill=tk.X, pady=10)

# Προσθήκη λογότυπου
logo_image = Image.open("marvel_logo.png")  # Το λογότυπο πρέπει να υπάρχει στο φάκελο
logo_image = logo_image.resize((200, 50), Image.Resampling.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(header_frame, image=logo_photo, bg=BG_COLOR)
logo_label.pack(side=tk.LEFT, padx=10)

header_label = tk.Label(header_frame, text="Marvel Search Engine", bg=BG_COLOR, fg=SECONDARY_COLOR,
                        font=("Helvetica", 24, "bold"))
header_label.pack(side=tk.LEFT)

# Πεδίο εισαγωγής ερωτήματος
query_label = ttk.Label(root, text="Enter your search query:")
query_label.pack(pady=10)

query_entry = tk.Entry(root, font=("Helvetica", 14), width=50)
query_entry.pack(pady=5)

# Επιλογές μεθόδου ανάκτησης
method_label = ttk.Label(root, text="Choose retrieval method:")
method_label.pack(pady=10)

method_var = tk.StringVar(value="Boolean")
methods = ["Boolean", "VSM", "BM25", "TF-IDF"]
method_menu = ttk.Combobox(root, textvariable=method_var, values=methods, state="readonly")
method_menu.pack(pady=5)

# Επιλογή Boolean λειτουργίας
boolean_label = ttk.Label(root, text="Boolean Operation (for Boolean Retrieval):")
boolean_label.pack(pady=10)

boolean_var = tk.StringVar(value="AND")
boolean_menu = ttk.Combobox(root, textvariable=boolean_var, values=["AND", "OR", "NOT"], state="readonly")
boolean_menu.pack(pady=5)

# Κουμπί αναζήτησης
search_button = ttk.Button(root, text="Search",
                           command=lambda: perform_search(query_entry.get(), method_var.get(), boolean_var.get()))
search_button.pack(pady=20)

# Πεδίο εμφάνισης αποτελεσμάτων
result_label = ttk.Label(root, text="Results:")
result_label.pack(pady=10)

result_list = tk.Listbox(root, font=("Helvetica", 12), bg=BG_COLOR, fg=SECONDARY_COLOR, width=80, height=20)
result_list.pack(pady=10)

# Πληροφορίες
info_label = tk.Label(root, text="Powered by the Marvel Universe", bg=BG_COLOR, fg=ACCENT_COLOR,
                      font=("Helvetica", 12, "italic"))
info_label.pack(side=tk.BOTTOM, pady=10)

# Εκκίνηση της εφαρμογής
root.mainloop()
