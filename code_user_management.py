import json
import os
from tkinter import messagebox, Canvas, Button, Label, Entry
from PIL import Image, ImageTk
import smtplib
from email.message import EmailMessage

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def registerlogin_page(self):
        # Implementation of register/login page
        pass

    def authenticate_login(self, email, password):
        if email in self.users and self.users[email] == password:
            messagebox.showinfo("Login Success!", "Login Success!")
            # Call the main menu page
        else:
            messagebox.showerror("Login Failed", "Incorrect email or password")

    def register_page(self):
        # Implementation of the register page
        pass

    def register_user(self, email, password, confirm_password):
        if password != confirm_password:
            messagebox.showerror("Registration Failed", "Password don't match!")
            return

        if email in self.users:
            messagebox.showerror("Registration Failed", "Email already registered.")
        else:
            self.users[email] = password
            self.save_users()
            messagebox.showinfo("Registration Success", "Registration successful! Please login.")
            # Call the login page

    def forgotpassword_page(self):
        # Implementation of forgot password page
        pass

    def send_verification_email(self):
        # Implementation of sending verification email
        pass

    def verify_code(self):
        # Implementation of verifying code
        pass

    def reset_password_page(self):
        # Implementation of reset password page
        pass

    def reset_password(self, new_password, confirm_password):
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        messagebox.showinfo("Success", "Password has been reset")
        # Call the login page
