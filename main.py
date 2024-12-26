import tkinter as tk
from tkinter import ttk
import random
import os
import struct
import pickle

# File to store game statistics
STATS_FILE = "game_stats.pkl"

def initialize_stats():
    """Initialize the statistics file if it doesn't exist."""
    if not os.path.exists(STATS_FILE):
        # Initialize with default values
        stats = {
            "r_total_games": 0,
            "r_total_correct": 0,
            "r_correct_first_try": 0,
            "c_total_games": 0,
            "c_total_correct": 0,
            "c_correct_first_try": 0
        }
        with open(STATS_FILE, "wb") as f:
            pickle.dump(stats, f)

def read_stats():
    """Read the statistics from the PKL file."""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "rb") as f:
            stats = pickle.load(f)
    else:
        # Default stats if the file does not exist
        stats = {
            "r_total_games": 0,
            "r_total_correct": 0,
            "r_correct_first_try": 0,
            "c_total_games": 0,
            "c_total_correct": 0,
            "c_correct_first_try": 0
        }
    return stats
def update_stats(stats):
    """Update the statistics in the PKL file."""
    with open(STATS_FILE, "wb") as f:
        pickle.dump(stats, f)

# def update_game_stats(self, correct=False):
#     total_games, total_correct, correct_first_try = self.stats
#     total_games += 1
#     if correct:
#         total_correct += 1
#         if self.first_try:
#             correct_first_try += 1
#     self.stats = (total_games, total_correct, correct_first_try)
#     update_stats(total_games, total_correct, correct_first_try)

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

        # Records frame (Initially hidden)
        self.records_frame = ttk.Frame(self.root, padding=10, style="TFrame", relief="solid", borderwidth=2, width=300)
        self.records_frame.pack_forget()  # Hide the records frame initially

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

        # Bind click event to close records frame when clicking outside
        self.root.bind("<Button-1>", self.close_records_if_clicked_outside)

    def show_records(self):
        """Display game statistics in the main window."""
        r_total_games, r_total_correct, r_correct_first_try, c_total_games, c_total_correct, c_correct_first_try = self.stats

        # Clear previous records
        for widget in self.records_frame.winfo_children():
            widget.destroy()

        # Display new records in the records frame
        ttk.Label(self.records_frame, text="Game Records", style="TLabel").pack(pady=10)
        if (self.current_mode.get() == "mode1"):
            ttk.Label(self.records_frame, text=f"Total Games Played: {self.stats[r_total_games]}", style="TLabel").pack(pady=5)
            ttk.Label(self.records_frame, text=f"Correct Answers: {self.stats[r_total_correct]}", style="TLabel").pack(pady=5)
            ttk.Label(self.records_frame, text=f"Correct on First Try: {self.stats[r_correct_first_try]}", style="TLabel").pack(pady=5)
        elif (self.current_mode.get() == "mode2"):
            ttk.Label(self.records_frame, text=f"Total Games Played: {self.stats[c_total_games]}", style="TLabel").pack(pady=5)
            ttk.Label(self.records_frame, text=f"Correct Answers: {self.stats[c_total_correct]}", style="TLabel").pack(pady=5)
            ttk.Label(self.records_frame, text=f"Correct on First Try: {self.stats[c_correct_first_try]}", style="TLabel").pack(pady=5)
        ttk.Button(self.records_frame, text="Close", command=self.hide_records, style="TButton").pack(pady=10)

        # Clear any previous placements and re-center the records frame
        self.records_frame.place_forget()  # Make sure to clear any previous position
        self.records_frame.place(relx=0.5, rely=0.5, anchor="center")  # Re-place the frame at center
        self.records_frame.lift()  # Make sure the records frame is on top

        # Force tkinter to update the layout
        self.records_frame.update_idletasks()  # Force a layout update
        self.root.update()  # Force the window to update

    def hide_records(self):
        """Hide the records frame and re-render the main content."""
        self.records_frame.place_forget()  # Completely remove it from the layout
        self.root.unbind("<Button-1>")  # Unbind the click event after closing

        # Re-render the main content by switching mode again
        self.switch_mode()  # This will call display_mode1 or display_mode2 depending on the current mode

    def close_records_if_clicked_outside(self, event):
        """Close the records frame if the user clicks outside of it."""
        # Get the coordinates of the records_frame
        x1 = self.records_frame.winfo_rootx()
        y1 = self.records_frame.winfo_rooty()
        x2 = x1 + self.records_frame.winfo_width()
        y2 = y1 + self.records_frame.winfo_height()

        # Check if the click is outside the frame and hide the records
        if self.records_frame.winfo_ismapped() and (event.x_root < x1 or event.x_root > x2 or event.y_root < y1 or event.y_root > y2):
            self.hide_records()
            self.root.unbind("<Button-1>")  # Unbind click event after closing

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
            b = int(self.coeff_b_entry.get()) / a
            c = int(self.coeff_c_entry.get()) / a
            if b == self.b / self.a and c == self.c / self.a:
                self.result_label.config(text="Correct!", foreground="green")
                self.update_game_stats(correct=True)
                self.next_question()
            else:
                self.result_label.config(text="Incorrect. Try again.", foreground="red")
                self.first_try = False
        except ValueError:
            self.result_label.config(text="Please enter valid integers.", foreground="red")

    def update_game_stats(self, correct=False):
        if self.current_mode.get() == "mode1":
            self.stats["r_total_games"] += 1
            if correct:
                self.stats["r_total_correct"] += 1
                if self.first_try:
                    self.stats["r_correct_first_try"] += 1
        elif self.current_mode.get() == "mode2":
            self.stats["c_total_games"] += 1
            if correct:
                self.stats["c_total_correct"] += 1
                if self.first_try:
                    self.stats["c_correct_first_try"] += 1

        # Save updated stats
        update_stats(self.stats)

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
