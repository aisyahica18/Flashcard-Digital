import json
import os
import random
from tkinter import messagebox

class FlashcardManager:
    def __init__(self):
        self.flashcards_file = "flashcards.json"
        self.flashcards = self.load_flashcards()

    def load_flashcards(self):
        if os.path.exists(self.flashcards_file):
            with open(self.flashcards_file, "r") as f:
                return json.load(f)
        return {}

    def save_flashcards(self):
        with open(self.flashcards_file, "w") as f:
            json.dump(self.flashcards, f, indent=4)

    def add_flashcard(self, keyword, description):
        if keyword and description:
            self.flashcards[keyword] = description
            self.save_flashcards()
            messagebox.showinfo("Success", "Flashcard added successfully!")
        else:
            messagebox.showerror("Error", "All columns must be filled in")

    def get_random_flashcards(self, count):
        if count > len(self.flashcards): 
            count = len(self.flashcards)
        return random.sample(list(self.flashcards.items()), count)

    def delete_flashcard(self, keyword):
        if keyword in self.flashcards:
            del self.flashcards[keyword]
            self.save_flashcards()
            messagebox.showinfo("Success", "Flashcard successfully deleted!")
        else:
            messagebox.showerror("Error", "Flashcard not found")
