import tkinter as tk
from tkinter import messagebox
from math import comb

def compute_probability(N, p, l, m):
    q = 1 - p
    k = (N + m) / 2

    if k != int(k) or k < 0 or k > N:
        return 0.0

    k = int(k)
    probability = comb(N, k) * (p ** k) * (q ** (N - k))
    return probability

def calculate():
    try:
        N = int(entry_N.get())
        p = float(entry_p.get())
        l = float(entry_l.get())
        m = int(entry_m.get())

        if not (0 <= p <= 1):
            raise ValueError("p musi być w zakresie [0, 1]")

        result = compute_probability(N, p, l, m)
        result_label.config(text=f"Prawdopodobieństwo: {result:.6f}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nieprawidłowe dane wejściowe: {e}")

# GUI
root = tk.Tk()
root.title("Problem pijaka")

tk.Label(root, text="Liczba kroków (N):").grid(row=0, column=0, sticky="e")
entry_N = tk.Entry(root)
entry_N.grid(row=0, column=1)

tk.Label(root, text="Prawdopodobieństwo w lewo (p):").grid(row=1, column=0, sticky="e")
entry_p = tk.Entry(root)
entry_p.grid(row=1, column=1)

tk.Label(root, text="Długość kroku (l):").grid(row=2, column=0, sticky="e")
entry_l = tk.Entry(root)
entry_l.grid(row=2, column=1)

tk.Label(root, text="Liczba kroków w lewo (m):").grid(row=3, column=0, sticky="e")
entry_m = tk.Entry(root)
entry_m.grid(row=3, column=1)

tk.Button(root, text="Oblicz", command=calculate).grid(row=4, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Prawdopodobieństwo: ")
result_label.grid(row=5, column=0, columnspan=2)

root.mainloop()