class QuizManager:
    def __init__(self, flashcard_manager):
        self.flashcard_manager = flashcard_manager
        self.score = 0
        self.current_question = 0
        self.questions = list(self.flashcard_manager.flashcards.items())

    def ask_question(self):
        if self.current_question < len(self.questions):
            keyword, explanation = self.questions[self.current_question]
            self.current_question += 1
            return keyword, explanation
        else:
            return None  

    def check_answer(self, user_answer, correct_answer):
        if user_answer.strip().lower() == correct_answer.lower():
            self.score += 1

        if self.current_question < len(self.questions):
            return self.ask_question()
        else:
            return None  
      
    def show_result(self):
        return self.score, len(self.questions)