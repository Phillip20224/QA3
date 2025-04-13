#setting up app. with gui for users (admin and quiz taker)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Dictionary to store valid usernames and passwords
admin_credentials = {
    "admin1": "password123",
    "admin2": "securepass",
    "phillip": "openAI2024"
}

    # Function to open the real Admin Settings window after successful login
def open_admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Settings")
    admin_window.geometry("300x200")
    ttk.Label(admin_window, text="Welcome to Admin Settings", font=("Arial", 14)).pack(pady=50)

# Function to validate login credentials
def validate_admin_login(username, password, login_window):
    if username in admin_credentials and admin_credentials[username] == password:
        login_window.destroy()
        open_admin_panel()
    else:
        messagebox.showerror("Access Denied", "Invalid username or password.")

# Function to display login window for admin
def open_admin_login():
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    ttk.Label(login_window, text="Admin Login", font=("Arial", 14)).pack(pady=10)

    ttk.Label(login_window, text="Username:").pack()
    username_entry = ttk.Entry(login_window)
    username_entry.pack()

    ttk.Label(login_window, text="Password:").pack()
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.pack()

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        validate_admin_login(username, password, login_window)

    ttk.Button(login_window, text="Login", command=attempt_login).pack(pady=10)

# Function to handle quiz taker window
def open_quiz_window():
    quiz_window = tk.Toplevel(root)
    quiz_window.title("Quiz")
    quiz_window.geometry("300x200")
    ttk.Label(quiz_window, text="Welcome to the Quiz", font=("Arial", 14)).pack(pady=50)
    # Add quiz-related widgets later here

# Main application window
root = tk.Tk()
root.title("User Selection")
root.geometry("350x200")

ttk.Label(root, text="Select User Type", font=("Arial", 16)).pack(pady=20)

# Buttons to open respective windows
admin_button = ttk.Button(root, text="Admin", command=open_admin_login)
admin_button.pack(pady=10)

quiz_button = ttk.Button(root, text="Take Quiz", command=open_quiz_window)
quiz_button.pack(pady=10)

# Run the app
root.mainloop()
