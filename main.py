import tkinter as tk
from tkinter import ttk
import random
from math import gcd

def generate_quadratic():
    """Generate a quadratic equation with integer coefficients and solutions."""
    while True:
        # Generate random integer solutions
        x1 = random.randint(-10, 10)
        x2 = random.randint(-10, 10)

        # Generate coefficients a, b, and c
        a = random.randint(1, 100) * random.choice([-1, 1])
        b = -a * (x1 + x2)
        c = a * x1 * x2

        # Check if coefficients are in range
        if -100 <= a <= 100 and -100 <= b <= 100 and -100 <= c <= 100:
            return a, b, c, x1, x2

class QuadraticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quadratic Equation Generator")
        self.root.geometry("400x300")

        # Frame for display
        self.display_frame = ttk.Frame(self.root, padding=10)
        self.display_frame.pack(expand=True, fill=tk.BOTH)

        # Equation label
        self.equation_label = ttk.Label(self.display_frame, text="", font=("Arial", 16))
        self.equation_label.pack(pady=10)

        # Solution label
        self.solution_label = ttk.Label(self.display_frame, text="", font=("Arial", 14), foreground="blue")
        self.solution_label.pack(pady=10)

        # Generate button
        self.generate_button = ttk.Button(
            self.display_frame, text="Generate Quadratic Equation", command=self.generate_and_display
        )
        self.generate_button.pack(pady=20)

        # Quit button
        self.quit_button = ttk.Button(self.display_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack()

    def generate_and_display(self):
        # Generate a valid quadratic equation
        a, b, c, x1, x2 = generate_quadratic()

        # Format and display the equation
        equation_text = f"{a}x² + {b}x + {c} = 0"
        self.equation_label.config(text=equation_text)

        # Display the solutions
        solution_text = f"Solutions: x₁ = {x1}, x₂ = {x2}"
        self.solution_label.config(text=solution_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraticApp(root)
    root.mainloop()
