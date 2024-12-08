import json
import os
import random
import smtplib
from email.message import EmailMessage
from tkinter import messagebox

class UserManager:
    def __init__(self, users_file="users.json"):
        self.users_file = users_file
        self.users = self.load_users()
        self.verification_code = None
        self.verified_email = None

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def register_user(self, email, password, confirm_password):
        try:
            if not email or not password or not confirm_password:
                raise ValueError("All fields must be filled.")
            if password != confirm_password:
                raise ValueError("Passwords do not match.")
            if email in self.users:
                raise ValueError("Email is already registered.")
            self.users[email] = password
            self.save_users()
            messagebox.showinfo("Registration Success", "Registration successful! Please log in.")
        except ValueError as e:
            messagebox.showerror("Registration Failed", str(e))

    def authenticate_login(self, email, password):
        if email in self.users and self.users[email] == password:
            messagebox.showinfo("Login Success", "Login successful!")
            return True
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password.")
            return False

    def send_verification_email(self, email):
        try:
            if not email:
                raise ValueError("Email cannot be empty.")

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

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            messagebox.showinfo("Email Sent", f"Verification code sent to {email}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")

    def verify_code(self, entered_code):
        if entered_code == self.verification_code:
            return True
        return False 