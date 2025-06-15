# zadanie numeryczne 1
import tkinter as tk
from tkinter import messagebox
import math

# metoda bisekcji
def bisection(a,b, func, eps=1e-6, max_iter=10_000):
    if func(a) * func(b) >= 0:
        raise ValueError("brak pierwiastka w tym przedziale")
    for _ in range(max_iter):
        mid = (a+b)/2.0
        if func(a) * func(mid) < 0:
            b = mid
        else:
            a = mid
        if abs(b-a) < eps:
            break
    return (a+b) / 2

# metoda regula falsi
def regula_falsi(a,b, func, eps=1e-6, max_iter=10_000):
    if func(a) * func(b) >= 0:
        raise ValueError("brak pierwiastka w tym przedziale")
    for _ in range(max_iter):
        # punkt przecięcia siecznej z osią OX
        c = a - ((func(a) * (b-a)) / (func(b) - func(a)))
        if func(a) * func(c) < 0:
            b = c
        else:
            a = c
        if abs(b-a) < eps:
            break
    return c

# metoda siecznych
def secant_method(x0,x1,func, eps=1e-6, max_iter = 10_000):
    for _ in range(max_iter):
        if abs(func(x1) - func(x0)) < eps:
            raise ZeroDivisionError("róznica pomiędzy func(x1) a func(x0) zbyt mała")
        x2 = x1 - func(x1) * (x1 - x0) / (func(x1) - func(x0))
        if abs(x2 - x1) < eps:
            return x2
        x0, x1 = x1, x2
    return ValueError("metoda siecznych nie zbiega się")

# funkcja zarządzająca
def run_methods():
    try:
        a = eval(entry_a.get(), {"math": math})
        b = eval(entry_b.get(), {"math": math})
        func_str = entry_func.get()
        func = lambda x: eval(func_str, {"x": x, "math": math})

        result_bis = bisection(a,b,func)
        result_rf = regula_falsi(a,b,func)
        result_sec = secant_method(a,b,func)

        output_text.set(f"Metoda bisekcji: x \u2248 {result_bis:.12f}\n"
                        f"Metoda regula falsi: x \u2248{ result_rf:.12f}\n"
                        f"Metoda siecznych: x \u2248 {result_sec:.12f}\n"
        )
    except Exception as e:
        messagebox.showerror("Błąd", str(e))

# GUI
root = tk.Tk()
root.title("Metody numeryczne znajdowania pierwiastków")
# główna ramka
main_frame = tk.Frame(root, padx=15, pady=15)
main_frame.pack()

# sekcja wprowadzania funkcji
func_frame = tk.LabelFrame(main_frame, text="Funkcja", padx=10, pady=10)
func_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

tk.Label(func_frame, text="f(x) =").grid(row=0, column=0, padx=5)
entry_func = tk.Entry(func_frame, width=30)
entry_func.grid(row=0, column=1)
entry_func.insert(0, "x**2 - 2")  # Przykładowa funkcja

# sekcja przedziału [a, b]
interval_frame = tk.LabelFrame(main_frame, text="Przedział [a, b]", padx=10, pady=10)
interval_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

tk.Label(interval_frame, text="a:").grid(row=0, column=0, padx=5)
entry_a = tk.Entry(interval_frame, width=10)
entry_a.grid(row=0, column=1, padx=5)
entry_a.insert(0, "1")

tk.Label(interval_frame, text="b:").grid(row=0, column=2, padx=5)
entry_b = tk.Entry(interval_frame, width=10)
entry_b.grid(row=0, column=3, padx=5)
entry_b.insert(0, "2")

# przycisk obliczania
button_frame = tk.Frame(main_frame)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(button_frame, text="Oblicz pierwiastki", command=run_methods, padx=10, pady=5).pack()

# wyniki
output_frame = tk.LabelFrame(main_frame, text="Wyniki", padx=10, pady=10)
output_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

output_text = tk.StringVar()
output_text.set("Wprowadź funkcję i przedział, a następnie kliknij 'Oblicz'")
output_label = tk.Label(output_frame, textvariable=output_text, justify="left", wraplength=350)
output_label.pack()

root.mainloop()