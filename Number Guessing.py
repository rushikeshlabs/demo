
import random
import tkinter as tk
from tkinter import messagebox

class NumberGuessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("400x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Game State Variables
        self.max_range = 100
        self.secret_number = 0
        self.attempts = 0
        self.game_over = False

        # Title Label
        title_label = tk.Label(
            root, 
            text="Number Guessing Game", 
            font=("Arial", 16, "bold"), 
            bg="#1e1e2e", 
            fg="#cdd6f4"
        )
        title_label.pack(pady=(20, 10))

        # Difficulty Selector Frame
        diff_frame = tk.Frame(root, bg="#1e1e2e")
        diff_frame.pack(fill="x", padx=25, pady=5)

        tk.Label(
            diff_frame, 
            text="Select Range:", 
            font=("Arial", 10, "bold"), 
            bg="#1e1e2e", 
            fg="#a6adc8"
        ).pack(side="left")

        self.diff_var = tk.StringVar(value="1-100")
        diff_options = ["1-50", "1-100", "1-500"]
        
        diff_menu = tk.OptionMenu(
            diff_frame, 
            self.diff_var, 
            *diff_options, 
            command=self.change_difficulty
        )
        diff_menu.config(
            bg="#313244", 
            fg="#cdd6f4", 
            activebackground="#45475a", 
            activeforeground="#cdd6f4", 
            bd=0, 
            highlightthickness=0,
            font=("Arial", 9, "bold")
        )
        diff_menu["menu"].config(bg="#313244", fg="#cdd6f4")
        diff_menu.pack(side="right")

        # Hint & Feedback Banner
        self.feedback_label = tk.Label(
            root,
            text="Enter a number to start!",
            font=("Arial", 12, "bold"),
            bg="#181825",
            fg="#89b4fa",
            height=2,
            relief="flat"
        )
        self.feedback_label.pack(fill="x", padx=25, pady=10)

        # Input Frame
        input_frame = tk.Frame(root, bg="#1e1e2e")
        input_frame.pack(fill="x", padx=25, pady=5)

        self.guess_entry = tk.Entry(
            input_frame,
            font=("Consolas", 18, "bold"),
            bg="#181825",
            fg="#a6e3a1",
            bd=0,
            justify="center",
            insertbackground="#cdd6f4"
        )
        self.guess_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        submit_btn = tk.Button(
            input_frame,
            text="Guess",
            font=("Arial", 11, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            activebackground="#94e2d5",
            bd=0,
            cursor="hand2",
            command=self.check_guess
        )
        submit_btn.pack(side="right", ipady=8, padx=10)

        # Attempt Counter Label
        self.attempts_label = tk.Label(
            root,
            text="Attempts: 0",
            font=("Arial", 10, "bold"),
            bg="#1e1e2e",
            fg="#fab387"
        )
        self.attempts_label.pack(pady=5)

        # Guess History Log Box
        tk.Label(
            root,
            text="Guess History:",
            font=("Arial", 9, "bold"),
            bg="#1e1e2e",
            fg="#a6adc8"
        ).pack(anchor="w", padx=25, pady=(10, 2))

        self.history_box = tk.Text(
            root,
            height=6,
            font=("Consolas", 10),
            bg="#181825",
            fg="#cdd6f4",
            bd=0,
            state="disabled",
            relief="flat"
        )
        self.history_box.pack(fill="x", padx=25, pady=(0, 10))

        # Reset / New Game Button
        reset_btn = tk.Button(
            root,
            text="New Game",
            font=("Arial", 11, "bold"),
            bg="#313244",
            fg="#cdd6f4",
            activebackground="#45475a",
            bd=0,
            cursor="hand2",
            command=self.reset_game
        )
        reset_btn.pack(fill="x", padx=25, pady=10, ipady=8)

        # Start game logic
        self.reset_game()

    def change_difficulty(self, choice):
        if choice == "1-50":
            self.max_range = 50
        elif choice == "1-100":
            self.max_range = 100
        elif choice == "1-500":
            self.max_range = 500
        self.reset_game()

    def reset_game(self):
        self.secret_number = random.randint(1, self.max_range)
        self.attempts = 0
        self.game_over = False
        self.feedback_label.config(
            text=f"Guess a number from 1 to {self.max_range}!", 
            fg="#89b4fa"
        )
        self.attempts_label.config(text="Attempts: 0")
        self.guess_entry.delete(0, tk.END)
        
        # Clear history log
        self.history_box.config(state="normal")
        self.history_box.delete("1.0", tk.END)
        self.history_box.config(state="disabled")

    def check_guess(self):
        if self.game_over:
            messagebox.showinfo("Game Over", "Click 'New Game' to play again!")
            return

        guess_str = self.guess_entry.get().strip()
        if not guess_str.isdigit():
            messagebox.showwarning("Invalid Input", f"Please enter a valid whole number between 1 and {self.max_range}!")
            return

        guess = int(guess_str)
        if guess < 1 or guess > self.max_range:
            messagebox.showwarning("Out of Range", f"Your guess must be between 1 and {self.max_range}!")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        # Determine result logic
        if guess < self.secret_number:
            result_text = f"Too LOW! ({guess})"
            self.feedback_label.config(text=f"{guess} is Too Low!", fg="#f38ba8")
        elif guess > self.secret_number:
            result_text = f"Too HIGH! ({guess})"
            self.feedback_label.config(text=f"{guess} is Too High!", fg="#f38ba8")
        else:
            result_text = f"CORRECT! ({guess})"
            self.feedback_label.config(
                text=f"Correct! You won in {self.attempts} attempts!", 
                fg="#a6e3a1"
            )
            self.game_over = True
            messagebox.showinfo("Congratulations!", f"You guessed number {self.secret_number} in {self.attempts} attempts!")

        # Log history
        self.history_box.config(state="normal")
        self.history_box.insert(tk.END, f"Attempt #{self.attempts}: {result_text}\n")
        self.history_box.see(tk.END)
        self.history_box.config(state="disabled")

        # Clear input field
        self.guess_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingApp(root)
    root.mainloop()
