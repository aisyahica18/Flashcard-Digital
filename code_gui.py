import tkinter as tk
from tkinter import Canvas, Button, Label, Entry, messagebox
import random
from PIL import Image, ImageTk
from code_user_management import UserManager
from code_flashcard_management import FlashcardManager
from code_quiz import QuizManager
from code_resume import ResumeManager

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Digital")
        self.root.state('zoomed')
        self.root.configure(bg="#f0f8ff")
        self.user_manager = UserManager()
        self.flashcard_manager = FlashcardManager()
        self.quiz_manager = QuizManager(self.flashcard_manager)
        self.resume_manager = ResumeManager(self.flashcard_manager)
        self.start_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_page(self):
        self.clear_screen()
        canvas = Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanUtama.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280,720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        start_button = Button( self.root, text="Start", font=("Gliker", 24, "bold"),
            bg="#eae4d2", fg="#17726d", command=self.registerlogin_page
        )
        canvas.create_window(600, 550, window=start_button)

    def registerlogin_page(self):
        self.clear_screen()

        canvas = Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanRegisterLogin.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        email_label = Label(self.root, text="Email", font=("Gliker", 14), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 297, window=email_label)
        email_entry = Entry(self.root, font=("Gliker", 16), width=30, bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 320, window=email_entry)

        password_label = Label(self.root, text="Password", font=("Gliker", 14), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 405, window=password_label)
        password_entry = Entry(self.root, font=("Gliker", 16), width=30, bg="#eae4d2", fg="#17726d", show="*")
        canvas.create_window(640, 430, window=password_entry)

        login_button = Button(
            self.root, text="Login", font=("Gliker", 16, "bold"), bg="#b5cfa1", fg="#17726d",
            command=lambda: self.authenticate_login(email_entry.get(), password_entry.get()),
        )
        canvas.create_window(640, 530, window=login_button)

        register_link = Label(
            self.root, text="Don't have an account? Sign up here!", font=("Gliker", 14), bg="#ffffff", fg="#17726d", cursor="hand2",
        )
        register_link.bind("<Button-1>", lambda e: self.register_page())
        canvas.create_window(640, 665, window=register_link)

        forgotpassword_link = Label(
            self.root, text="Forgot Password?", font=("Gliker", 12), bg="#17726d", fg="#ffffff", cursor="hand2",
        )
        forgotpassword_link.bind("<Button-1>", lambda e: self.forgotpassword_page())
        canvas.create_window(640, 605, window=forgotpassword_link)

    def authenticate_login(self, email, password):
        if email in self.user_manager.users and self.user_manager.users[email] == password:
            messagebox.showinfo("Login Success!", "Login Success!")
            self.menu_page()
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password")

    def register_page(self):
        self.clear_screen()

        canvas = Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanRegister.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        email_label = Label(self.root, text="Email", font=("Gliker", 14), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 300, window=email_label)
        self.email_entry = Entry(self.root, font=("Gliker", 14), width=30, bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 328, window=self.email_entry)

        password_label = Label(self.root, text="Password", font=("Gliker", 14), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 377, window=password_label)
        self.password_entry = Entry(self.root, font=("Gliker", 14), width=30, bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 406, window=self.password_entry)

        confirm_password_label = Label(self.root, text="Confirm Password", font=("Gliker", 14), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 460, window=confirm_password_label)
        self.confirm_password_entry = Entry(self.root, font=("Gliker", 14), width=30, bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 488, window=self.confirm_password_entry)

        sign_up_button = Button(
            self.root, text="Sign Up", font=("Gliker", 18), bg="#eae4d2", fg="#17726d",
            command=lambda: self.register_user(self.email_entry.get(), self.password_entry.get(), self.confirm_password_entry.get())
        )
        canvas.create_window(640, 553, window=sign_up_button)

        back_to_registerlogin = Label(self.root, text="← Kembali ke halaman login", font=("Gliker", 12), bg="#ffffff", fg="#17726d", cursor="hand2")
        back_to_registerlogin.bind("<Button-1>", lambda e: self.registerlogin_page())
        canvas.create_window(640, 665, window=back_to_registerlogin)

    def register_user(self, email, password, confirm_password):
        if not email or not password or not confirm_password:
            messagebox.showerror("Registration Failed", "All columns must be filled in")
            return

        if password != confirm_password:
            messagebox.showerror("Registration Failed", "Passwords don't match!")
            return

        if email in self.user_manager.users:
            messagebox.showerror("Registration Failed", "Email already registered.")
        else:
            self.user_manager.users[email] = password
            self.user_manager.save_users()
            messagebox.showinfo("Registration Success", "Registration successful! Please login.")
            self.registerlogin_page()

    def forgotpassword_page(self):
        self.clear_screen()
        
        canvas = Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanForgotPassword.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        email_label = Label(self.root, text="Enter Email", font=("Gliker", 12), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 340, window=email_label)
        email_entry = Entry(self.root, font=("Gliker", 14), bg="#eae4d2", fg="#17726d", width=30)
        canvas.create_window(640, 362, window=email_entry)

        send_code_button = Button(
            self.root, text="Send Verification Code", font=("Gliker", 12), bg="#eae4d2", fg="#17726d",
            command=lambda: self.user_manager.send_verification_email(email_entry.get())
        )
        canvas.create_window(640, 397, window=send_code_button)

        code_label = Label(self.root, text="Verification Code", font=("Gliker", 12), bg="#b5cfa1", fg="#17726d")
        canvas.create_window(640, 464, window=code_label)

        code_entry = Entry(self.root, font=("Gliker", 14), bg="#b5cfa1", fg="#17726d", width=30)
        canvas.create_window(640, 486, window=code_entry)

        verify_button = Button(self.root, text="Verify Code", font=("Gliker", 12), bg="#b5cfa1", fg="#17726d",
                            command=lambda: self.verify_code_and_redirect(email_entry.get(), code_entry.get()))
        canvas.create_window(640, 520, window=verify_button)
        
        back_to_registerlogin = Label(self.root, text="← Kembali ke halaman login", font=("Gliker", 12), bg="#17726d", fg="#ffffff", cursor="hand2")
        back_to_registerlogin.bind("<Button-1>", lambda e: self.registerlogin_page())
        canvas.create_window(640, 598, window=back_to_registerlogin)
      
    def verify_code_and_redirect(self, email, entered_code):
        if self.user_manager.verify_code(entered_code):
            messagebox.showinfo("Verification Success", "Code verified! You can now reset your password.")
            self.reset_password_page()
        else:
            messagebox.showerror("Verification Failed", "Invalid verification code.")

    def reset_password_page(self):
        self.clear_screen()

        canvas = Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanResetPassword.jpg") 
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))  
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        new_password_label = Label(self.root, text="New Password", font=("Gliker", 14), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 342, window=new_password_label)  
        self.new_password_entry = Entry(self.root, font=("Gliker", 14), bg="#eae4d2", fg="#17726d", width=30, show="*")  
        canvas.create_window(640, 377, window=self.new_password_entry)  

        confirm_password_label = Label(self.root, text="Confirm Password", font=("Gliker", 14), bg="#b5cfa1", fg="#17726d")
        canvas.create_window(640, 465, window=confirm_password_label)  
        self.confirm_password_entry = Entry(self.root, font=("Gliker", 14), bg="#b5cfa1", fg="#17726d", width=30, show="*")  
        canvas.create_window(640, 486, window=self.confirm_password_entry)  
        
        def reset_password():
            new_password = self.new_password_entry.get() 
            confirm_password = self.confirm_password_entry.get()  
            if not new_password or not confirm_password:
                messagebox.showerror("Error", "Password fields cannot be empty")
                return
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
            messagebox.showinfo("Success", "Password has been reset")
            self.registerlogin_page()  
            
        reset_button = Button(self.root, text="Reset Password", font=("Gliker", 12), bg="#b5cfa1", fg="#17726d", command=reset_password)
        canvas.create_window(640, 517, window=reset_button)
        
        back_to_registerlogin = Label(self.root, text="← Kembali ke halaman login", font=("Gliker", 12), bg="#17726d", fg="#ffffff", cursor="hand2")
        back_to_registerlogin.bind("<Button-1>", lambda e: self.registerlogin_page())
        canvas.create_window(640, 598, window=back_to_registerlogin)

    def menu_page(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("MenuUtama.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        frame = tk.Frame(self.root, bg="#ffffff")
        frame.place(relx=0.2, rely=0.68, anchor="center")

        menu_options = ["Flashcard", "Quiz", "Resume", "Back"]
        actions = [self.flashcard_page, self.quiz_page, self.resume_page, self.start_page]

        for i, (option, action) in enumerate(zip(menu_options, actions), start=0):
            tk.Button(
                frame, text=option, font=("Gliker", 18), bg="#eae4d2", fg="#17726d",
                command=action
            ).grid(row=i, column=1, padx=20, pady=20, ipadx=22, ipady=5, sticky="w")

        exit_button = tk.Button(
            self.root, text="Exit", font=("Gliker", 18), bg="#ffcccc", fg="#990000",
            command=self.root.quit  # Fungsi untuk keluar dari aplikasi
        )
        exit_button.place(relx=0.95, rely=0.05, anchor="ne")

    def flashcard_page(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanFlashcard.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        add_button = tk.Button(self.root, text="Add Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                               command=self.add_flashcard_page)
        canvas.create_window(98, 220, window=add_button)

        show_button = tk.Button(self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                                command=self.show_flashcards_page)
        canvas.create_window(98, 340, window=show_button)

        delete_button = tk.Button(self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                                  command=self.delete_flashcard_page)
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
                                   command=self.menu_page)
        canvas.create_window(98, 580, window=kembali_button)

    def add_flashcard_page(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanFlashcard.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        add_button = tk.Button(self.root, text="Add Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                               command=self.add_flashcard_page)
        canvas.create_window(98, 220, window=add_button)

        show_button = tk.Button(self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                                command=self.show_flashcards_page)
        canvas.create_window(98, 340, window=show_button)

        delete_button = tk.Button(self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                                  command=self.delete_flashcard_page)
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
                                   command=self.menu_page)
        canvas.create_window(98, 580, window=kembali_button)

        frame = tk.Frame(self.root, bg="#ffffff")
        canvas.create_window(700, 250, window=frame)

        Label(frame, text="Keyword:", font=("Gliker", 18), bg="#17726d", fg="#eae4d2").grid(row=0, column=0, pady=10, sticky="e")
        keyword_entry = Entry(frame, font=("Gliker", 18), bg="#eae4d2", fg="#17726d", width=30)
        keyword_entry.grid(row=0, column=1, pady=10)

        Label(frame, text="Description:", font=("Gliker", 18), bg="#17726d", fg="#eae4d2").grid(row=1, column=0, pady=10, sticky="e")
        description_entry = Entry(frame, font=("Gliker", 18), bg="#eae4d2", fg="#17726d", width=30)
        description_entry.grid(row=1, column=1, pady=10)

        tambah_button = Button(
            self.root, text="Add Flashcard", font=("Gliker", 18), bg="#17726d", fg="#eae4d2",
            command=lambda: self.add_flashcard(keyword_entry.get(), description_entry.get())
        )
        canvas.create_window(700, 450, window=tambah_button)

    def add_flashcard(self, keyword, description):
        self.flashcard_manager.add_flashcard(keyword, description)
        self.flashcard_page()

    def show_flashcards_page(self):  
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanFlashcard.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        add_button = tk.Button(
            self.root, text="Add Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.add_flashcard_page
        )
        canvas.create_window(98, 220, window=add_button)

        show_button = tk.Button(
            self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.show_flashcards_page
        )
        canvas.create_window(98, 340, window=show_button)

        delete_button = tk.Button(
            self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.delete_flashcard_page
        )
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=self.menu_page
        )
        canvas.create_window(98, 580, window=kembali_button)
        
        flashcard_frame = tk.Frame(canvas, width=1000, height=650, bg="#ffffff")  
        flashcard_frame.place(relx=0.58, rely=0.68, anchor="center")  

        flashcard_canvas = tk.Canvas(flashcard_frame, bg="#ffffff", highlightthickness=0, width=1000, height=650)
        flashcard_canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(
            flashcard_frame, orient="vertical", command=flashcard_canvas.yview, width=15
        )
        scrollbar.pack(side="right", fill="y")

        flashcard_canvas.configure(yscrollcommand=scrollbar.set)
        flashcard_inner_frame = tk.Frame(flashcard_canvas, bg="#ffffff", width=400)  
        flashcard_canvas.create_window((0, 0), window=flashcard_inner_frame, anchor="nw")

        colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#CCFFFF", "#FFCCFF"]
        row, col = 0, 0  

        for flashcard, description in self.flashcard_manager.flashcards.items():
            bg_color = random.choice(colors)
            card = tk.Frame(flashcard_inner_frame, bg=bg_color, bd=2, relief="solid", padx=10, pady=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            tk.Label(card, text=flashcard, font=("Gliker", 16, "bold"), bg=bg_color).pack()
            tk.Label(card, text=description, font=("Gliker", 12), bg=bg_color, wraplength=200, justify="left").pack()

            col += 1
            if col == 4:  
                col = 0
                row += 1

        flashcard_inner_frame.update_idletasks()
        flashcard_canvas.config(scrollregion=flashcard_canvas.bbox("all"))

    def delete_flashcard_page(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanFlashcard.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        add_button = tk.Button(
            self.root, text="Add Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.add_flashcard_page
        )
        canvas.create_window(98, 220, window=add_button)

        show_button = tk.Button(
            self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.show_flashcards_page
        )
        canvas.create_window(98, 340, window=show_button)

        delete_button = tk.Button(
            self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.delete_flashcard_page
        )
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=self.menu_page
        )
        canvas.create_window(98, 580, window=kembali_button)

        frame = tk.Frame(self.root, bg="#eae4d2")
        canvas.create_window(700, 300, window=frame)

        Label(frame, text="Choose Flashcard:", font=("Gliker", 18), fg="#eae4d2", bg="#17726d").grid(row=0, column=0, pady=10, sticky="e")

        flashcard_keys = list(self.flashcard_manager.flashcards.keys())
        if flashcard_keys:
            selected_flashcard = tk.StringVar()
            selected_flashcard.set(flashcard_keys[0])

            tk.OptionMenu(frame, selected_flashcard, *flashcard_keys).grid(row=0, column=1, pady=10)

            delete_button = tk.Button(
                self.root, text="Delete", font=("Gliker", 18), bg="#17726d", fg="#eae4d2",
                command=lambda: self.delete_flashcard(selected_flashcard.get())
            )
            canvas.create_window(700, 450, window=delete_button)
        else:
            no_flashcard_label = Label(self.root, text="No flashcard available", font=("Arial", 18), bg="#f0f8ff")
            canvas.create_window(640, 350, window=no_flashcard_label)

    def delete_flashcard(self, keyword):
        self.flashcard_manager.delete_flashcard(keyword)
        self.flashcard_page()

    def quiz_page(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanSoalQuiz.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#17726d", fg="#eae4d2",
            command=self.menu_page
        )
        canvas.create_window(640, 610, window=kembali_button)

        jumlah_label = tk.Label(
            self.root, text="Number of Questions:", font=("Gliker", 18), bg="#17726d", fg="#eae4d2"
        )
        canvas.create_window(640, 300, window=jumlah_label)

        jumlah_entry = tk.Entry(self.root, font=("Gliker", 18), fg="#17726d", bg="#eae4d2", width=5)
        canvas.create_window(640, 350, window=jumlah_entry)

        start_button = tk.Button(
            self.root, text="Start Quiz", font=("Gliker", 18), bg="#17726d", fg="#eae4d2",
            command=lambda: self.start_quiz(jumlah_entry.get())
        )
        canvas.create_window(640, 420, window=start_button)

    def start_quiz(self, jumlah_soal):
        try:
            jumlah_soal = int(jumlah_soal)  # Validasi input angka
            total_soal = len(self.flashcard_manager.flashcards)  # Total soal tersedia

            if jumlah_soal <= 0:
                tk.messagebox.showerror("Error", "Number of questions must be greater than 0!")
                return

            if total_soal == 0:
                tk.messagebox.showerror("Error", "No questions available in the database!")
                return

            self.quiz_manager.questions = self.flashcard_manager.get_random_flashcards(jumlah_soal)
            self.quiz_manager.score = 0
            self.quiz_manager.current_question = 0

            if self.quiz_manager.questions:  # Mulai kuis jika ada soal
                self.ask_question()
            else:
                tk.messagebox.showerror("Error", "No questions to display!")
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number.")
    
    def ask_question(self):
        self.clear_screen()

        if self.quiz_manager.current_question < len(self.quiz_manager.questions):
            canvas = tk.Canvas(self.root, width=1280, height=720)
            canvas.pack(fill="both", expand=True)
            try:
                image = Image.open("HalamanSoalQuiz.jpg")
                self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
                canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
            except Exception as e:
                print(f"Error loading image: {e}")

            question_data = self.quiz_manager.questions[self.quiz_manager.current_question]
            keyword, explanation = question_data

            question_label = Label(self.root, text="Question:", font=("Gliker", 24), bg="#17726d", fg="#eae4d2")
            canvas.create_window(640, 235, window=question_label)
            explanation_label = Label(self.root, text=explanation, font=("Gliker", 24), bg="#17726d", fg="#eae4d2")
            canvas.create_window(640, 295, window=explanation_label)

            answer_label = Label(self.root, text="Answer:", font=("Gliker", 24), bg="#17726d", fg="#eae4d2")
            canvas.create_window(640, 395, window=answer_label)
            answer_entry = Entry(self.root, font=("Gliker", 24), fg="#17726d", bg="#eae4d2", width=30)
            canvas.create_window(640, 455, window=answer_entry)

            next_button = tk.Button(
                self.root, text="Next", font=("Gliker", 15), bg="#17726d", fg="#eae4d2",
                command=lambda: [self.check_answer(answer_entry.get(), keyword)]
            )
            canvas.create_window(1020, 600, window=next_button)
        else:
            self.show_result()

    def check_answer(self, user_answer, correct_answer):
        question_data = self.quiz_manager.check_answer(user_answer, correct_answer)
        if question_data:
            self.ask_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanSoalQuiz.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 15), bg="#17726d", fg="#eae4d2",
            command=self.menu_page
        )
        canvas.create_window(640, 580, window=kembali_button)

        quiz_label = Label(
            self.root, text="Quiz Finished", font=("Gliker", 50, "bold"), bg="#17726d", fg="#eae4d2"
        )
        canvas.create_window(640, 300, window=quiz_label)

        score, total = self.quiz_manager.show_result()
        result_text = f"Result: Correct {score} out of {total} Questions"
        result_label = Label(
            self.root, text=result_text, font=("Gliker", 29), bg="#17726d", fg="#eae4d2"
        )
        canvas.create_window(640, 420, window=result_label)

    def resume_page(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanResume.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        view_button = tk.Button(
            self.root, text="Show Resume", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.view_resume
        )
        canvas.create_window(96, 223, window=view_button)

        download_button = tk.Button(
            self.root, text="Download Resume", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.download_resume
        )
        canvas.create_window(96, 378, window=download_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=self.menu_page
        )
        canvas.create_window(96, 530, window=kembali_button)

    def view_resume(self):
        self.clear_screen()

        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanResume.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")
            
        view_button = tk.Button(
            self.root, text="Show Resume", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.view_resume
        )
        canvas.create_window(96, 223, window=view_button)

        download_button = tk.Button(
            self.root, text="Download Resume", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.download_resume
        )
        canvas.create_window(96, 378, window=download_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=self.menu_page
        )
        canvas.create_window(96, 530, window=kembali_button)

        flashcard_frame = tk.Frame(canvas, width=800, height=400, bg="#ffffff")  
        flashcard_frame.place(relx=0.55, rely=0.5, anchor="center")  

        flashcard_canvas = tk.Canvas(flashcard_frame, bg="#ffffff", highlightthickness=0, width=800, height=400)
        flashcard_canvas.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(
            flashcard_frame, orient="vertical", command=flashcard_canvas.yview, width=15
        )
        scrollbar.pack(side="right", fill="y")

        flashcard_canvas.configure(yscrollcommand=scrollbar.set)
        flashcard_inner_frame = tk.Frame(flashcard_canvas, bg="#ffffff", width=400)  
        flashcard_canvas.create_window((0, 0), window=flashcard_inner_frame, anchor="nw")

        for keyword, explanation in self.flashcard_manager.flashcards.items():
            keyword_label = tk.Label(
                flashcard_inner_frame, text=f"Kata Kunci: {keyword}", font=("Gliker", 14), bg="#ffffff", fg="#17726d"
            )
            keyword_label.pack(anchor="w", pady=5, padx=15)

            explanation_label = tk.Label(
                flashcard_inner_frame, text=f"Penjelasan: {explanation}", font=("Gliker", 13), bg="#ffffff", wraplength=750
            )
            explanation_label.pack(anchor="w", pady=5, padx=15)

        flashcard_inner_frame.update_idletasks()
        flashcard_canvas.config(scrollregion=flashcard_canvas.bbox("all"))
            
    def download_resume(self):
        self.clear_screen()
        
        canvas = tk.Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanResume.jpg")
            self.bg_image = ImageTk.PhotoImage(image.resize((1280, 720)))
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")
            
        view_button = tk.Button(
            self.root, text="Show Resume", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.view_resume
        )
        canvas.create_window(96, 223, window=view_button)

        download_button = tk.Button(
            self.root, text="Download Resume", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=self.download_resume
        )
        canvas.create_window(96, 378, window=download_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=self.menu_page
        )
        canvas.create_window(96, 530, window=kembali_button)

        self.resume_manager.download_resume()

        downloadresume_label = tk.Label(
            self.root, text="Resume downloaded successfully!", font=("Gliker", 30), bg="#ffffff", fg="#17726d"
        )
        canvas.create_window(715, 350, window=downloadresume_label)