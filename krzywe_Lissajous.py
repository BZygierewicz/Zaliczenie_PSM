import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

class LissajousApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Krzywe Lissajous")
        self.root.configure(bg="white")

        self.a = tk.DoubleVar(value=3)
        self.b = tk.DoubleVar(value=2)
        self.delta = tk.DoubleVar(value=np.pi / 2)

        self.anim = None
        self.line = None
        self.paused = False
        self.current_frame = 0

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use()
        style.configure("TLabel", font=("Segoe UI", 11), background="white")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TEntry", font=("Segoe UI", 10))

        # wykres
        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=(10, 0))

        #panel sterowania
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.grid(row=1, column=0, sticky="ew")

        # Parametry wejściowe
        ttk.Label(control_frame, text="a:").grid(row=0, column=0, padx=(0, 5), sticky="e")
        ttk.Entry(control_frame, textvariable=self.a, width=6).grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="b:").grid(row=0, column=2, padx=(15, 5), sticky="e")
        ttk.Entry(control_frame, textvariable=self.b, width=6).grid(row=0, column=3, padx=5)

        ttk.Label(control_frame, text="delta (rad):").grid(row=0, column=4, padx=(15, 5), sticky="e")
        ttk.Entry(control_frame, textvariable=self.delta, width=8).grid(row=0, column=5, padx=5)

        # Przyciski
        ttk.Button(control_frame, text="Start / Wznów", command=self.start_or_resume_animation).grid(row=1, column=0, columnspan=3, pady=10, sticky="ew", padx=5)
        ttk.Button(control_frame, text="Pauza", command=self.pause_animation).grid(row=1, column=3, columnspan=3, pady=10, sticky="ew", padx=5)

        # Rozciąganie kolumn
        for i in range(6):
            control_frame.columnconfigure(i, weight=1)

    def start_or_resume_animation(self):
        if self.anim and self.paused:
            self.anim.event_source.start()
            self.paused = False
            return

        self.ax.clear()
        self.ax.set_xlim(-1.1, 1.1)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_aspect('equal')
        self.ax.grid(True)

        self.line, = self.ax.plot([], [], lw=2, color="blue")
        self.t = np.linspace(0, 2 * np.pi, 1000)
        self.x_data = []
        self.y_data = []
        self.current_frame = 0

        self.a_val = self.a.get()
        self.b_val = self.b.get()
        self.delta_val = self.delta.get()

        self.anim = FuncAnimation(
            self.figure,
            self.update_plot,
            frames=len(self.t),
            init_func=self.init_anim,
            interval=5,
            blit=True,
            repeat=False
        )
        self.canvas.draw()

    def pause_animation(self):
        if self.anim:
            self.anim.event_source.stop()
            self.paused = True

    def init_anim(self):
        self.line.set_data([], [])
        return self.line,

    def update_plot(self, i):
        if self.paused:
            return self.line,

        i = self.current_frame
        if i >= len(self.t):
            return self.line,

        t_i = self.t[i]
        x_i = np.sin(self.a_val * t_i + self.delta_val)
        y_i = np.sin(self.b_val * t_i)

        self.x_data.append(x_i)
        self.y_data.append(y_i)

        self.line.set_data(self.x_data, self.y_data)
        self.current_frame += 1
        return self.line,

if __name__ == "__main__":
    root = tk.Tk()
    app = LissajousApp(root)
    root.mainloop()