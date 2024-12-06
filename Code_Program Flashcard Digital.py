import tkinter as tk
from tkinter import messagebox
import json
import os
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import Canvas, Button, Label, Entry
from PIL import Image, ImageTk
import smtplib
from email.message import EmailMessage

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Digital")
        self.root.state('zoomed')
        self.root.configure(bg="#f0f8ff")
        self.flashcards_file = "flashcards.json"
        self.users_file = "users.json"  
        self.flashcards = self.load_flashcards()
        self.users = self.load_users()
        self.start_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_flashcards(self):
        if os.path.exists(self.flashcards_file):
            with open(self.flashcards_file, "r") as f:
                return json.load(f)
        return {}

    def save_flashcards(self):
        with open(self.flashcards_file, "w") as f:
            json.dump(self.flashcards, f, indent=4)

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=4)
            
    def start_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        canvas = Canvas(self.root, width=1280, height=720)
        canvas.pack(fill="both", expand=True)
        try:
            image = Image.open("HalamanUtama.jpg") 
            self.bg_image = ImageTk.PhotoImage(image.resize((1280,720))) 
            canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error loading image: {e}")

        start_button = Button(
            self.root, text="Start", font=("Gliker", 24, "bold"),
            bg="#eae4d2", fg="#17726d", command=self.registerlogin_page
        )
        start_button = canvas.create_window(600, 550, window=start_button)  
        
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
            self.root, text="Don't have an account? Sign up here!", font=("Gliker", 14), bg="#ffffff", fg="#17726d",cursor="hand2",
        )
        register_link.bind("<Button-1>", lambda e: self.register_page())
        canvas.create_window(640, 665, window=register_link)
        
        forgotpassword_link = Label(
            self.root, text="Forgot Password?", font=("Gliker", 12), bg="#17726d", fg="#ffffff", cursor="hand2",
        )
        forgotpassword_link.bind("<Button-1>", lambda e: self.forgotpassword_page())  
        canvas.create_window(640, 605, window=forgotpassword_link) 
        
    def authenticate_login(self, email, password):
        print(f"Isi self.users saat login: {self.users}")  # Debug log
        if not self.users:
            print("Error: User data is not available")
            messagebox.showerror("Login Failed", "User data is not available.")
            return

        if email in self.users and self.users[email] == password:
            messagebox.showinfo("Login Success!", "Login Success!")
            self.menu_page()  
        else:
            print("Incorrect email or password")  
            messagebox.showerror("Login Failed", "Incorrect email or password")

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
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

        sign_up_button = tk.Button(
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
            messagebox.showerror("Registration Failed", "Password dont match!")
            return

        if self.users is None:
            self.users = {}  

        if email in self.users:
            messagebox.showerror("Registration Failed", "Email sudah terdaftar.")
        else:
            self.users[email] = password
            self.save_users()  
            messagebox.showinfo("Registration Success", "Registrasi berhasil! Silakan login.")
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

        self.email_label = Label(self.root, text="Enter Email", font=("Gliker", 12), bg="#eae4d2", fg="#17726d")
        canvas.create_window(640, 340, window=self.email_label)  
        self.email_entry = Entry(self.root, font=("Gliker", 14), bg="#eae4d2", fg="#17726d", width=30)
        canvas.create_window(640, 362, window=self.email_entry)  
        
        send_code_button = Button(self.root, text="Send Verification Code", font=("Gliker", 12), bg="#eae4d2", fg="#17726d", command=self.send_verification_email)
        canvas.create_window(640, 397, window=send_code_button) 
        code_label = Label(self.root, text="Verification Code", font=("Gliker", 12), bg="#b5cfa1", fg="#17726d")
        canvas.create_window(640, 464, window=code_label) 

        self.code_entry = Entry(self.root, font=("Gliker", 14), bg="#b5cfa1", fg="#17726d", width=30)
        canvas.create_window(640, 486, window=self.code_entry)  

        verify_button = Button(self.root, text="Verify Code", font=("Gliker", 12), bg="#b5cfa1", fg="#17726d", command=self.verify_code)
        canvas.create_window(640, 520, window=verify_button)  

        back_to_registerlogin = Label(self.root, text="← Kembali ke halaman login", font=("Gliker", 12), bg="#17726d", fg="#ffffff", cursor="hand2")
        back_to_registerlogin.bind("<Button-1>", lambda e: self.registerlogin_page())
        canvas.create_window(640, 598, window=back_to_registerlogin)  
         
    def send_verification_email(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showerror("Error", "Email cannot be empty")
            return

        sender_email = "flashcarddigital@gmail.com"
        sender_password = "hzyngfsfaniaoatj"  

        self.verification_code = str(random.randint(100000, 999999))

        subject = "Reset Password Flashcard Digital App"
        body = f"Your verification code is: {self.verification_code}"

        message = EmailMessage()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.set_content(body)

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Memulai koneksi TLS
                server.login(sender_email, sender_password)
                server.send_message(message)

            messagebox.showinfo("Success", f"Verification code sent to {email}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

    def verify_code(self):
        entered_code = self.code_entry.get()
        if entered_code == self.verification_code:
            messagebox.showinfo("Success", "Verification code is correct!")
            self.verified_email = self.email_entry.get()
            self.reset_password_page() 
        else:
            messagebox.showerror("Error", "Invalid verification code!")

    def reset_password_page(self):
        self.clear_screen()
        self.root.title("Reset Password")

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
    
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

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
        
        menu_options = ["Flashcard", "Quiz", "Resume", "Kembali"]
        actions = [self.flashcard_page, self.quiz_page, self.resume_page, self.start_page]

        for i, (option, action) in enumerate(zip(menu_options, actions), start=0):
            tk.Button(
                frame, text=option, font=("Gliker", 18), bg="#eae4d2", fg="#17726d",
                command=action
            ).grid(row=i, column=1, padx=20, pady=20, ipadx=22, ipady=5, sticky="w") 

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
                command=lambda: self.add_flashcard_page()
                )
        canvas.create_window(98, 220, window=add_button)
        
        show_button = tk.Button(
                self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                command=lambda: self.show_flashcards_page()
                )
        canvas.create_window(98, 340, window=show_button)
        
        delete_button = tk.Button(
                self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                command=lambda: self.delete_flashcard_page()
                )
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(
                self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
                command=lambda: self.menu_page()
                )
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

        add_button = tk.Button(
                self.root, text="Add Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                command=lambda: self.add_flashcard_page()
                )
        canvas.create_window(98, 220, window=add_button)
        
        show_button = tk.Button(
                self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                command=lambda: self.show_flashcards_page()
                )
        canvas.create_window(98, 340, window=show_button)
        
        delete_button = tk.Button(
                self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
                command=lambda: self.delete_flashcard_page()
                )
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(
                self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
                command=lambda: self.menu_page()
                )
        canvas.create_window(98, 580, window=kembali_button)
        
        frame = tk.Frame(self.root, bg="#ffffff")
        canvas.create_window(700, 250, window=frame)  

        tk.Label(frame, text="Keyword:", font=("Gliker", 18), bg="#17726d", fg="#eae4d2").grid(row=0, column=0, pady=10, sticky="e")
        keyword_entry = tk.Entry(frame, font=("Gliker", 18), bg="#eae4d2", fg="#17726d", width=30)
        keyword_entry.grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Description:", font=("Gliker", 18), bg="#17726d", fg="#eae4d2").grid(row=1, column=0, pady=10, sticky="e")
        description_entry = tk.Entry(frame, font=("Gliker", 18), bg="#eae4d2", fg="#17726d", width=30)
        description_entry.grid(row=1, column=1, pady=10)

        tambah_button = tk.Button(
            self.root, text="Add Flashcard", font=("Gliker", 18), bg="#17726d", fg="#eae4d2",
            command=lambda: self.add_flashcard(keyword_entry.get(), description_entry.get())
        )
        canvas.create_window(700, 450, window=tambah_button)

    def add_flashcard(self, keyword, description):
        if keyword and description:
            self.flashcards[keyword] = description
            self.save_flashcards()
            messagebox.showinfo("Success", "Flashcard added successfully!")
            self.flashcard_page()
        else:
            messagebox.showerror("Error", "All columns must be filled in")
            
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
            command=lambda: self.add_flashcard_page()
        )
        canvas.create_window(98, 220, window=add_button)

        show_button = tk.Button(
            self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=lambda: self.show_flashcards_page()
        )
        canvas.create_window(98, 340, window=show_button)

        delete_button = tk.Button(
            self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=lambda: self.delete_flashcard_page()
        )
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=lambda: self.menu_page()
        )
        canvas.create_window(98, 580, window=kembali_button)
        
        tk.Label(self.root, text="Flashcards", font=("Arial", 36, "bold"), bg="#ffffff", fg="#4682b4").pack(pady=50)

        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(pady=50)
        canvas.create_window(640, 360, window=frame)
        # for i in range(5):  # Contoh 5 tombol
        #     tk.Button(frame, text=f"Button {i+1}").pack(side="left", padx=5)

        colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#CCFFFF", "#FFCCFF"]

        # Variabel untuk melacak posisi grid
        row = 0
        col = 0  # Pastikan col didefinisikan di sini

        # Menampilkan flashcards dengan 4 per baris
        for flashcard, description in self.flashcards.items():
            bg_color = random.choice(colors)
            card = tk.Frame(frame, bg=bg_color, bd=2, relief="solid", padx=10, pady=10)

            # Tempatkan card pada grid, di baris dan kolom yang sesuai
            card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            # Menambahkan label flashcard
            tk.Label(card, text=flashcard, font=("Gliker", 18, "bold"), bg=bg_color).pack()

            # Menambahkan label deskripsi dengan newline
            tk.Label(card, text=description, font=("Gliker", 14), bg=bg_color, wraplength=200, justify="left").pack()

            # Menyesuaikan kolom untuk setiap 4 card, dan pindah ke baris baru
            col += 1
            if col == 5:  # Setelah 4 kolom, pindah ke baris baru
                col = 0
                row += 1
        
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
            command=lambda: self.add_flashcard_page()
        )
        canvas.create_window(98, 220, window=add_button)

        show_button = tk.Button(
            self.root, text="Show Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=lambda: self.show_flashcards_page()
        )
        canvas.create_window(98, 340, window=show_button)

        delete_button = tk.Button(
            self.root, text="Delete Flashcard", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=lambda: self.delete_flashcard_page()
        )
        canvas.create_window(96, 460, window=delete_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=lambda: self.menu_page()
        )
        canvas.create_window(98, 580, window=kembali_button)

        # Frame untuk memilih flashcard
        frame = tk.Frame(self.root, bg="#eae4d2")
        canvas.create_window(700, 300, window=frame)  

        # Label dan dropdown untuk memilih flashcard
        tk.Label(frame, text="Choose Flashcard:", font=("Gliker", 18), fg="#eae4d2", bg="#17726d").grid(row=0, column=0, pady=10, sticky="e")

        flashcard_keys = list(self.flashcards.keys())
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
            no_flashcard_label = tk.Label(self.root, text="No flashcard available", font=("Arial", 18), bg="#f0f8ff")
            canvas.create_window(640, 350, window=no_flashcard_label)  
            
    def delete_flashcard(self, keyword):
        if keyword in self.flashcards:
            del self.flashcards[keyword]
            self.save_flashcards()
            messagebox.showinfo("Success", "Flashcard succesfully deleted!")
            self.flashcard_page()
        else:
            messagebox.showerror("Error", "Flashcard not found")
            
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
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=lambda: self.menu_page()
        )
        canvas.create_window(98, 580, window=kembali_button)

        self.score = 0
        self.current_question = 0
        self.questions = list(self.flashcards.items())  # Memuat semua soal dan jawaban
        print(f"DEBUG: {self.questions}")  # Debugging untuk memastikan soal dimuat

        if self.questions:  
            self.ask_question()
        else:
            print("ERROR: Tidak ada soal untuk ditampilkan!")

    def ask_question(self):
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
            command=lambda: self.menu_page()
        )
        canvas.create_window(320, 600, window=kembali_button)

        if self.current_question < len(self.questions):
            keyword, explanation = self.questions[self.current_question]
            self.current_question += 1
            
            question_label = tk.Label(self.root, text="Question:", font=("Gliker", 24), bg="#17726d", fg="#eae4d2")
            canvas.create_window(640, 235, window=question_label)  
            explanation_label = tk.Label(self.root, text=explanation, font=("Gliker", 24), bg="#17726d", fg="#eae4d2")
            canvas.create_window(640, 295, window= explanation_label)  

            answer_label = tk.Label(self.root, text="Answer:", font=("Gliker", 24), bg="#17726d", fg="#eae4d2")
            canvas.create_window(640, 395, window=answer_label)
            answer_entry = tk.Entry(self.root, font=("Gliker",24), fg="#17726d", bg="#eae4d2", width=30)
            canvas.create_window(640, 455, window=answer_entry)
            
            next_button = tk.Button(
                self.root, text="Next", font=("Gliker", 15), bg="#17726d", fg="#eae4d2",
                command=lambda: [self.check_answer(answer_entry.get(), keyword), next_button.config(state=tk.DISABLED)]
            )
            canvas.create_window(1020, 600, window=next_button) 

        else:
            self.show_result()

    def check_answer(self, user_answer, correct_answer):
        if user_answer.strip().lower() == correct_answer.lower():
            self.score += 1  
       
        if self.current_question < len(self.questions):
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
            command=lambda: self.menu_page()
        )
        canvas.create_window(640, 580, window=kembali_button)

        quiz_label = tk.Label(
            self.root, text="Quiz Finished", font=("Gliker", 50, "bold"), bg="#17726d", fg="#eae4d2"
        )
        canvas.create_window(640, 300, window=quiz_label)  

        result_text = f"Result: Correct {self.score} out of {len(self.questions)} Questions"
        result_label = tk.Label(
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
            command=lambda: self.view_resume()
        )
        canvas.create_window(96, 223, window=view_button)

        download_button = tk.Button(
            self.root, text="Download Resume", font=("Gliker", 13), bg="#eae4d2", fg="#17726d",
            command=lambda: self.download_resume()
        )
        canvas.create_window(96, 378, window=download_button)

        kembali_button = tk.Button(
            self.root, text="Back to Main Menu", font=("Gliker", 11), bg="#eae4d2", fg="#17726d",
            command=lambda: self.menu_page()
        )
        canvas.create_window(96, 530, window=kembali_button)

    def view_resume(self):
        self.clear_screen()

        for keyword, explanation in self.flashcards.items():
            tk.Label(self.root, text=f"Kata Kunci: {keyword}", font=("Gliker", 10), bg="#f0f8ff").pack(pady=10)
            tk.Label(self.root, text=f"Penjelasan: {explanation}", font=("Gliker", 10), bg="#f0f8ff", wraplength=800).pack(pady=10)

        tk.Button(
            self.root, text="Kembali", font=("Gliker", 18), bg="#17726d", fg="#eae4d2", command=self.menu_page
        ).pack(pady=20, ipadx=20, ipady=5)

    def download_resume(self):
        self.clear_screen()

        pdf_filename = "resume_flashcards.pdf"
 
        c = canvas.Canvas(pdf_filename, pagesize=letter)

        c.setFont("Helvetica-Bold", 24)
        c.drawString(100, 750, "Resume Flashcards")
        c.setFont("Helvetica", 18)
    
        y_position = 720 

        for keyword, explanation in self.flashcards.items():
            if y_position <= 100:  # Jika mencapai batas bawah halaman, buat halaman baru
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
        # Memeriksa apakah file telah berhasil disimpan
        if os.path.exists(pdf_filename):
            print("PDF berhasil disimpan!")
        else:
            print("Terjadi kesalahan saat menyimpan PDF.")

        tk.Label(self.root, text="Resume berhasil diunduh!", font=("Arial", 18), bg="#f0f8ff", fg="#4682b4").pack(pady=20)

        tk.Button(
            self.root, text="Kembali", font=("Arial", 18), bg="#d3d3d3", command=self.menu_page
        ).pack(pady=20, ipadx=20, ipady=5)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root) 
    root.mainloop()