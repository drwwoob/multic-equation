import tkinter as tk
from tkinter import ttk
import random
import os
import struct

# File to store game statistics
STATS_FILE = "game_stats.bin"

def initialize_stats():
    """Initialize the statistics file if it doesn't exist."""
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, "wb") as f:
            # total_games, total_correct, correct_first_try
            f.write(struct.pack("iii", 0, 0, 0))

def read_stats():
    """Read game statistics from the file."""
    with open(STATS_FILE, "rb") as f:
        return struct.unpack("iii", f.read())

def update_stats(total_games, total_correct, correct_first_try):
    """Update the game statistics."""
    with open(STATS_FILE, "wb") as f:
        f.write(struct.pack("iii", total_games, total_correct, correct_first_try))

def generate_quadratic():
    """Generate a quadratic equation with integer coefficients and solutions."""
    while True:
        x1 = random.randint(-20, 20)
        x2 = random.randint(-20, 20)
        a = random.randint(1, 10) * random.choice([-1, 1])
        b = -a * (x1 + x2)
        c = a * x1 * x2
        if -100 <= a <= 100 and -100 <= b <= 100 and -100 <= c <= 100:
            return a, b, c, x1, x2

class QuadraticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quadratic Equation Quiz")
        self.root.geometry("600x400")
        self.root.configure(bg="black")

        self.current_mode = tk.StringVar(value="mode1")
        self.a, self.b, self.c, self.x1, self.x2 = generate_quadratic()
        self.first_try = True

        # Initialize stats
        initialize_stats()
        self.stats = read_stats()

        # Mode selection
        self.mode_frame = ttk.Frame(self.root, padding=10, style="TFrame")
        self.mode_frame.pack(fill=tk.X)
        ttk.Label(self.mode_frame, text="Select Mode:", style="TLabel").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.mode_frame, text="Guess Roots", variable=self.current_mode, value="mode1", command=self.switch_mode, style="TRadiobutton").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.mode_frame, text="Guess Coefficients", variable=self.current_mode, value="mode2", command=self.switch_mode, style="TRadiobutton").pack(side=tk.LEFT, padx=5)

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=10, style="TFrame")
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.display_mode1()

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="black")
        style.configure("TLabel", background="black", foreground="white", font=("Arial", 16))
        style.configure("TRadiobutton", background="black", foreground="white", font=("Arial", 14))
        style.configure("TButton", background="black", foreground="white", font=("Arial", 14))
        style.map("TButton",
                  background=[('active', 'black'), ('!disabled', 'black')],
                  foreground=[('active', 'white')])
        
    def show_records(self):
        """Display game statistics in a popup window."""
        total_games, total_correct, correct_first_try = self.stats
        popup = tk.Toplevel(self.root)
        popup.title("Game Records")
        popup.geometry("300x200")
        popup.configure(bg="black")
        ttk.Label(popup, text="Game Records", style="TLabel").pack(pady=10)
        ttk.Label(popup, text=f"Total Games Played: {total_games}", style="TLabel").pack(pady=5)
        ttk.Label(popup, text=f"Correct Answers: {total_correct}", style="TLabel").pack(pady=5)
        ttk.Label(popup, text=f"Correct on First Try: {correct_first_try}", style="TLabel").pack(pady=5)
        ttk.Button(popup, text="Close", command=popup.destroy, style="TButton").pack(pady=10)
        
    def display_mode1(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"Equation: {self.a}x² + {self.b}x + {self.c} = 0", style="TLabel").pack(pady=10)
        ttk.Label(self.main_frame, text="Enter roots:", style="TLabel").pack(pady=5)
        self.root1_entry = ttk.Entry(self.main_frame, font=("Arial", 14))
        self.root1_entry.pack(pady=5)
        self.root2_entry = ttk.Entry(self.main_frame, font=("Arial", 14))
        self.root2_entry.pack(pady=5)
        ttk.Button(self.main_frame, text="Submit", command=self.check_roots, style="TButton").pack(pady=10)
        ttk.Button(self.main_frame, text="Show Records", command=self.show_records, style="TButton").pack(pady=5)
        self.result_label = ttk.Label(self.main_frame, text="", style="TLabel")
        self.result_label.pack(pady=5)

    def display_mode2(self):
        self.clear_frame()
        ttk.Label(self.main_frame, text=f"Roots: x₁ = {self.x1}, x₂ = {self.x2}", style="TLabel").pack(pady=10)
        ttk.Label(self.main_frame, text="Enter coefficients (a, b, c):", style="TLabel").pack(pady=5)
        self.coeff_a_entry = ttk.Entry(self.main_frame, font=("Arial", 14))
        self.coeff_a_entry.pack(pady=5)
        self.coeff_b_entry = ttk.Entry(self.main_frame, font=("Arial", 14))
        self.coeff_b_entry.pack(pady=5)
        self.coeff_c_entry = ttk.Entry(self.main_frame, font=("Arial", 14))
        self.coeff_c_entry.pack(pady=5)
        ttk.Button(self.main_frame, text="Submit", command=self.check_coefficients, style="TButton").pack(pady=10)
        ttk.Button(self.main_frame, text="Show Records", command=self.show_records, style="TButton").pack(pady=5)
        self.result_label = ttk.Label(self.main_frame, text="", style="TLabel")
        self.result_label.pack(pady=5)


    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def check_roots(self):
        try:
            root1 = int(self.root1_entry.get())
            root2 = int(self.root2_entry.get())
            if {root1, root2} == {self.x1, self.x2}:
                self.result_label.config(text="Correct!", foreground="green")
                self.update_game_stats(correct=True)
                self.next_question()
            else:
                self.result_label.config(text="Incorrect. Try again.", foreground="red")
                self.first_try = False
        except ValueError:
            self.result_label.config(text="Please enter valid integers.", foreground="red")

    def check_coefficients(self):
        try:
            a = int(self.coeff_a_entry.get())
            b = int(self.coeff_b_entry.get())
            c = int(self.coeff_c_entry.get())
            if a == self.a and b == self.b and c == self.c:
                self.result_label.config(text="Correct!", foreground="green")
                self.update_game_stats(correct=True)
                self.next_question()
            else:
                self.result_label.config(text="Incorrect. Try again.", foreground="red")
                self.first_try = False
        except ValueError:
            self.result_label.config(text="Please enter valid integers.", foreground="red")

    def update_game_stats(self, correct=False):
        total_games, total_correct, correct_first_try = self.stats
        total_games += 1
        if correct:
            total_correct += 1
            if self.first_try:
                correct_first_try += 1
        self.stats = (total_games, total_correct, correct_first_try)
        update_stats(total_games, total_correct, correct_first_try)

    def next_question(self):
        self.a, self.b, self.c, self.x1, self.x2 = generate_quadratic()
        self.first_try = True
        self.switch_mode()

    def switch_mode(self):
        if self.current_mode.get() == "mode1":
            self.display_mode1()
        else:
            self.display_mode2()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuadraticApp(root)
    root.mainloop()
