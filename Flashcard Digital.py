import tkinter as tk
from tkinter import messagebox
import random
import sqlite3

# Modul untuk mengelola database
class Database:
    def __init__(self, db_name="flashcards.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Tabel flashcards
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            description TEXT NOT NULL
        )
        """)
        # Tabel users
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.conn.commit()

    def insert_user(self, username, password):
        try:
            self.conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    def validate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor = self.conn.execute(query, (username, password))
        return cursor.fetchone() is not None

    def insert_flashcard(self, keyword, description):
        query = "INSERT INTO flashcards (keyword, description) VALUES (?, ?)"
        self.conn.execute(query, (keyword, description))
        self.conn.commit()

    def delete_flashcard(self, keyword):
        query = "DELETE FROM flashcards WHERE keyword = ?"
        self.conn.execute(query, (keyword,))
        self.conn.commit()

    def get_flashcards(self):
        query = "SELECT keyword, description FROM flashcards"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

# Modul untuk logika quiz
class Quiz:
    def __init__(self, flashcards):
        self.flashcards = flashcards

    def get_random_question(self):
        self.current_keyword, self.current_description = random.choice(list(self.flashcards.items()))
        partial_description = " ".join(self.current_description.split()[:3]) + "..."
        return self.current_keyword, partial_description

    def check_answer(self, user_answer):
        correct_answer = self.flashcards[self.current_keyword]
        return user_answer.lower() == correct_answer.lower()

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Digital dengan Login")
        self.database = Database()
        self.flashcards = {}

        # Halaman login
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, pady=5)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1, pady=5)

        # Halaman utama (hanya terlihat setelah login berhasil)
        self.main_frame = tk.Frame(self.root)

        # Input kata kunci dan penjelasan
        self.keyword_label = tk.Label(self.main_frame, text="Kata Kunci:")
        self.keyword_label.grid(row=0, column=0, pady=5)
        self.keyword_entry = tk.Entry(self.main_frame)
        self.keyword_entry.grid(row=0, column=1, pady=5)

        self.description_label = tk.Label(self.main_frame, text="Penjelasan:")
        self.description_label.grid(row=1, column=0, pady=5)
        self.description_entry = tk.Entry(self.main_frame)
        self.description_entry.grid(row=1, column=1, pady=5)

        # Tombol untuk menambah, menghapus, dan mereview flashcard
        self.add_button = tk.Button(self.main_frame, text="Tambah Flashcard", command=self.add_flashcard)
        self.add_button.grid(row=2, column=0, pady=5)

        self.delete_button = tk.Button(self.main_frame, text="Hapus Flashcard", command=self.delete_flashcard)
        self.delete_button.grid(row=2, column=1, pady=5)

        self.review_button = tk.Button(self.main_frame, text="Review Materi", command=self.review_flashcards)
        self.review_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Kontainer untuk menampilkan flashcard
        self.flashcard_container = tk.Frame(self.main_frame)
        self.flashcard_container.grid(row=4, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.database.validate_user(username, password):
            self.flashcards = {k: d for k, d in self.database.get_flashcards()}
            self.login_frame.pack_forget()
            self.main_frame.pack(padx=10, pady=10)
        else:
            messagebox.showwarning("Gagal Login", "Username atau password salah!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.database.insert_user(username, password):
            messagebox.showinfo("Registrasi Berhasil", "Akun berhasil dibuat. Silakan login.")
        else:
            messagebox.showwarning("Registrasi Gagal", "Username sudah digunakan!")

    def add_flashcard(self):
        keyword = self.keyword_entry.get()
        description = self.description_entry.get()
        if keyword and description:
            self.flashcards[keyword] = description
            self.database.insert_flashcard(keyword, description)
            self.keyword_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.display_flashcards()
        else:
            messagebox.showwarning("Peringatan", "Kata kunci dan penjelasan tidak boleh kosong!")

    def delete_flashcard(self):
        keyword = self.keyword_entry.get()
        if keyword in self.flashcards:
            del self.flashcards[keyword]
            self.database.delete_flashcard(keyword)
            self.display_flashcards()
        else:
            messagebox.showwarning("Peringatan", "Flashcard dengan kata kunci tersebut tidak ditemukan!")

    def display_flashcards(self):
        for widget in self.flashcard_container.winfo_children():
            widget.destroy()
        for idx, (keyword, description) in enumerate(self.flashcards.items()):
            card_frame = tk.Frame(self.flashcard_container, bg="#FFDDC1", padx=10, pady=10)
            card_frame.pack(side="left", padx=10, pady=10)
            tk.Label(card_frame, text=keyword, font=("Helvetica", 14, "bold"), bg="#FFDDC1").pack(pady=5)
            tk.Label(card_frame, text=description, font=("Helvetica", 12), bg="#FFDDC1", wraplength=180).pack(pady=5)

    def review_flashcards(self):
        messagebox.showinfo("Review", "Fitur review flashcards masih dalam pengembangan!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()