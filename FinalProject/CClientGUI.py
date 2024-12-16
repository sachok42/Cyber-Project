import tkinter as tk
from tkinter import messagebox, simpledialog
from CClientBL import Client


class CharadesGameGUI:
    def __init__(self, client):
        self.client = client
        self.root = tk.Tk()
        self.root.title("Charades Game")
        self.root.geometry("800x600")
        self.username = None
        self.is_leader = False

        self.init_login_screen()

    def init_login_screen(self):
        """Set up the login screen."""
        self.clear_screen()

        tk.Label(self.root, text="Welcome to Charades!", font=("Helvetica", 18)).pack(pady=20)
        tk.Label(self.root, text="Enter your username:").pack(pady=10)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=10)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        """Send login data to the server."""
        self.username = self.username_entry.get()
        if not self.username:
            messagebox.showerror("Error", "Username is required!")
            return

        self.client.send_data(f"LOGIN {self.username}")
        response = self.client.receive_data()

        if response == "LOGIN_SUCCESS":
            messagebox.showinfo("Success", f"Welcome, {self.username}!")
            self.switch_to_game_screen()
        else:
            messagebox.showerror("Error", "Login failed. Try again.")

    def switch_to_game_screen(self):
        """Switch to the main game screen."""
        self.clear_screen()

        # Leader info
        self.role_label = tk.Label(self.root, text="Role: Waiting for game to start...", font=("Helvetica", 14))
        self.role_label.pack(pady=10)

        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(pady=20)

        # Input for guessing
        self.guess_entry = tk.Entry(self.root, width=50)
        self.guess_entry.pack(pady=10)
        tk.Button(self.root, text="Submit Guess", command=self.submit_guess).pack(pady=5)

        # Display scores
        self.scores_label = tk.Label(self.root, text="Scores will appear here.", font=("Helvetica", 12))
        self.scores_label.pack(pady=20)

        # Start listening for server messages
        self.listen_to_server()

    def clear_screen(self):
        """Remove all widgets from the screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def submit_guess(self):
        """Send the guess to the server."""
        guess = self.guess_entry.get()
        if not guess:
            messagebox.showerror("Error", "Please enter a guess!")
            return

        self.client.send_data(f"GUESS {guess}")
        self.guess_entry.delete(0, tk.END)

    def listen_to_server(self):
        """Continuously listen to server messages and update the GUI."""
        def handle_server_messages():
            while True:
                try:
                    message = self.client.receive_data()
                    self.process_server_message(message)
                except ConnectionError:
                    messagebox.showerror("Error", "Lost connection to the server.")
                    break

        import threading
        threading.Thre
