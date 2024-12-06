import tkinter as tk
from tkinter import messagebox
import random
import json
import sqlite3
import os
import pygame
import sys

# Modul untuk mengelola database
class Database:
    def __init__(self, db_name="flashcards.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            description TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

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
        self.root.title("Flashcard Digital Berwarna")
        self.database = Database()
        self.flashcards = {keyword: description for keyword, description in self.database.get_flashcards()}
        self.colors = ["#FFDDC1", "#FFABAB", "#FFC3A0", "#FF677D", "#D4A5A5"]
        self.quiz = Quiz(self.flashcards)

        # Frame utama
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Input kata kunci dan penjelasan
        self.keyword_label = tk.Label(self.main_frame, text="Kata Kunci:")
        self.keyword_label.grid(row=0, column=0, pady=5)
        self.keyword_entry = tk.Entry(self.main_frame)
        self.keyword_entry.grid(row=0, column=1, pady=5)

        self.description_label = tk.Label(self.main_frame, text="Penjelasan:")
        self.description_label.grid(row=1, column=0, pady=5)
        self.description_entry = tk.Entry(self.main_frame)
        self.description_entry.grid(row=1, column=1, pady=5)

        # Tombol untuk menambah dan menghapus flashcard serta mereview materi
        self.add_button = tk.Button(self.main_frame, text="Tambah Flashcard", command=self.add_flashcard)
        self.add_button.grid(row=2, column=0, pady=5)

        self.delete_button = tk.Button(self.main_frame, text="Hapus Flashcard", command=self.delete_flashcard)
        self.delete_button.grid(row=2, column=1, pady=5)

        self.review_button = tk.Button(self.main_frame, text="Review Materi", command=self.review_flashcards)
        self.review_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Kontainer untuk menampilkan flashcard
        self.flashcard_container = tk.Frame(self.main_frame)
        self.flashcard_container.grid(row=4, column=0, columnspan=2, pady=10)
        self.display_flashcards()

        # Frame untuk review materi
        self.review_frame = tk.Frame(self.root)
        self.question_label = tk.Label(self.review_frame, text="", font=('Helvetica', 16))
        self.question_label.pack(pady=20)
        self.answer_entry = tk.Entry(self.review_frame, font=('Helvetica', 14))
        self.answer_entry.pack(pady=5)
        self.check_button = tk.Button(self.review_frame, text="Cek Jawaban", command=self.check_answer)
        self.check_button.pack(pady=10)
        self.result_label = tk.Label(self.review_frame, text="", font=('Helvetica', 12))
        self.result_label.pack(pady=10)

        self.current_keyword = None

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
            self.keyword_entry.delete(0, tk.END)
            self.display_flashcards()
        else:
            messagebox.showwarning("Peringatan", "Flashcard dengan kata kunci tersebut tidak ditemukan!")

    def display_flashcards(self):
        for widget in self.flashcard_container.winfo_children():
            widget.destroy()

        for idx, (keyword, description) in enumerate(self.flashcards.items()):
            color = self.colors[idx % len(self.colors)]
            card_frame = tk.Frame(self.flashcard_container, bg=color, padx=10, pady=10, height=200, width=200)
            card_frame.pack_propagate(False)  # Prevent frame from resizing to fit content
            card_frame.pack(side="left", padx=10, pady=10)
            card_label = tk.Label(card_frame, text=f"{keyword}\n{description}", bg=color, font=('Helvetica', 12), wraplength=180, justify="center")
            card_label.pack(expand=True)

    def review_flashcards(self):
        if self.flashcards:
            self.main_frame.pack_forget()
            self.review_frame.pack(padx=10, pady=10)
            self.ask_question()
        else:
            messagebox.showwarning("Peringatan", "Tidak ada flashcard untuk direview!")

    def ask_question(self):
        self.current_keyword, partial_description = self.quiz.get_random_question()
        self.question_label.config(text=f"Apa penjelasan dari '{self.current_keyword}'?")
        self.answer_entry.delete(0, tk.END)
        self.result_label.config(text="")

    def check_answer(self):
        answer = self.answer_entry.get()
        if self.quiz.check_answer(answer):
            self.result_label.config(text="Jawaban Anda benar!", fg="green")
        else:
            correct_answer = self.flashcards[self.current_keyword]
            self.result_label.config(text=f"Jawaban salah. Jawaban yang benar adalah: {correct_answer}", fg="red")
        self.ask_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()

# Inisialisasi Pygame
pygame.init()

# Ukuran layar dan warna
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (240, 240, 240)
CARD_COLOR_FRONT = (100, 150, 200)
CARD_COLOR_BACK = (200, 100, 150)
TEXT_COLOR = (255, 255, 255)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flashcard Animation")
clock = pygame.time.Clock()

# Dimensi flashcard
CARD_WIDTH, CARD_HEIGHT = 300, 200
card_rect = pygame.Rect((WIDTH - CARD_WIDTH) // 2, (HEIGHT - CARD_HEIGHT) // 2, CARD_WIDTH, CARD_HEIGHT)

# Variabel animasi
is_flipping = False
flip_angle = 0
show_front = True

# Font
font = pygame.font.Font(None, 40)

# Fungsi untuk menggambar flashcard
def draw_card():
    if flip_angle < 90:
        color = CARD_COLOR_FRONT if show_front else CARD_COLOR_BACK
        text = "FRONT" if show_front else "BACK"
    else:
        color = CARD_COLOR_BACK if show_front else CARD_COLOR_FRONT
        text = "BACK" if show_front else "FRONT"

    # Gambar kartu
    pygame.draw.rect(screen, color, card_rect)
    
    # Tambahkan teks
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=card_rect.center)
    screen.blit(text_surface, text_rect)

# Loop utama
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Klik mouse untuk memulai flip
        if event.type == pygame.MOUSEBUTTONDOWN:
            if card_rect.collidepoint(event.pos) and not is_flipping:
                is_flipping = True
    
    if is_flipping:
        flip_angle += 10
        if flip_angle >= 180:
            flip_angle = 0
            is_flipping = False
            show_front = not show_front

    # Gambar latar belakang
    screen.fill(BACKGROUND_COLOR)
    
    # Gambar kartu
    draw_card()
    
    # Refresh layar
    pygame.display.flip()
    
    # Batasi kecepatan frame
    clock.tick(30)