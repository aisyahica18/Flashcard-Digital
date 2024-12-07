from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
import os

class ResumeManager:
    def __init__(self, flashcard_manager):
        self.flashcard_manager = flashcard_manager

    def download_resume(self):
        pdf_filename = "resume_flashcards.pdf"
        c = pdf_canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, 750, "Resume Flashcards")
        c.setFont("Helvetica", 18)
        y_position = 720

        for keyword, explanation in self.flashcard_manager.flashcards.items():
            if y_position <= 100:
                c.showPage()
                c.setFont("Helvetica-Bold", 24)
                c.drawString(100, 750, "Resume Flashcards")
                c.setFont("Helvetica", 18)
                y_position = 720

            c.drawString(100, y_position, f"Kata Kunci: {keyword}")
            y_position -= 20
            c.drawString(100, y_position, f"Penjelasan: {explanation}")
            y_position -= 40

        c.save()
        if os.path.exists(pdf_filename):
            print("PDF successfully saved!")
        else:
            print("Error saving PDF.")
