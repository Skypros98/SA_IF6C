import pandas as pd
import re
import tkinter as tk
from tkinter import ttk, messagebox

df = pd.read_csv("coursera_data.csv")

def convert_enrollment(enrollment_str):
    if isinstance(enrollment_str, str):
        num = float(re.findall(r"\d+\.?\d*", enrollment_str)[0])
        if 'k' in enrollment_str.lower():
            return int(num * 1_000)
        elif 'm' in enrollment_str.lower():
            return int(num * 1_000_000)
        else:
            return int(num)
    return 0

df['course_students_enrolled_num'] = df['course_students_enrolled'].apply(convert_enrollment)

# --- Sorting Algorithms ---
def merge_sort(data, key):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)
    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][key] >= right[j][key]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def quick_sort(data, key):
    if len(data) <= 1:
        return data
    pivot = data[0]
    less = [item for item in data[1:] if item[key] > pivot[key]]
    greater = [item for item in data[1:] if item[key] <= pivot[key]]
    return quick_sort(less, key) + [pivot] + quick_sort(greater, key)

def format_enrollment(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}k"
    return str(num)

# --- GUI Functions ---
def sort_courses():
    try:
        top_n = int(top_n_var.get())
        if top_n <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Masukkan jumlah hasil yang valid (angka > 0).")
        return

    key = "course_rating" if criteria_var.get() == "Rating" else "course_students_enrolled_num"
    data_to_sort = df[['course_title', 'course_rating', 'course_students_enrolled_num']].to_dict(orient='records')

    if algorithm_var.get() == "Merge Sort":
        result = merge_sort(data_to_sort, key)
    else:
        result = quick_sort(data_to_sort, key)

    top_result = result[:top_n]

    # Tampilkan di tabel
    for row in tree.get_children():
        tree.delete(row)
    for course in top_result:
        tree.insert("", tk.END, values=(
            course['course_title'],
            course['course_rating'],
            format_enrollment(course['course_students_enrolled_num'])
        ))

    # Simpan ke CSV
    df_sorted = pd.DataFrame(top_result)
    df_sorted.to_csv("sorted_courses.csv", index=False)
    messagebox.showinfo("Berhasil", f"Hasil disimpan ke file 'sorted_courses.csv'.")

# --- GUI Layout ---
root = tk.Tk()
root.title("Pengurutan Kursus Coursera")

# Dropdown algoritma
algorithm_var = tk.StringVar(value="Merge Sort")
ttk.Label(root, text="Algoritma:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
ttk.OptionMenu(root, algorithm_var, "Merge Sort", "Merge Sort", "QuickSort").grid(row=0, column=1, padx=5, pady=5)

# Dropdown kriteria
criteria_var = tk.StringVar(value="Rating")
ttk.Label(root, text="Urut berdasarkan:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
ttk.OptionMenu(root, criteria_var, "Rating", "Rating", "Jumlah Pendaftar").grid(row=1, column=1, padx=5, pady=5)

# Input jumlah hasil
top_n_var = tk.StringVar(value="10")
ttk.Label(root, text="Jumlah hasil (Top N):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
ttk.Entry(root, textvariable=top_n_var).grid(row=2, column=1, padx=5, pady=5)

# Tombol sort
ttk.Button(root, text="Urutkan & Simpan", command=sort_courses).grid(row=3, column=0, columnspan=2, pady=10)

# Tabel hasil
tree = ttk.Treeview(root, columns=("Title", "Rating", "Enrolled"), show="headings")
tree.heading("Title", text="Judul Kursus")
tree.heading("Rating", text="Rating")
tree.heading("Enrolled", text="Pendaftar")
tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Scrollbar tabel
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=4, column=2, sticky='ns')

root.mainloop()
