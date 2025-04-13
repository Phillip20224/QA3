#setting up app. with gui for users (admin and quiz taker)

import tkinter as tk
from tkinter import ttk

# Function to handle admin window
def open_admin_window():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Settings")
    admin_window.geometry("300x200")
    ttk.Label(admin_window, text="Welcome to Admin Settings", font=("Arial", 14)).pack(pady=50)
    # Add admin-related widgets later here

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
admin_button = ttk.Button(root, text="Admin", command=open_admin_window)
admin_button.pack(pady=10)

quiz_button = ttk.Button(root, text="Take Quiz", command=open_quiz_window)
quiz_button.pack(pady=10)

# Run the app
root.mainloop()
