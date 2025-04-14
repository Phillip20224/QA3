#setting up app. with gui for users (admin and quiz taker)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from coursequestions import Question, save_many_questions
import sqlite3
import random

# Initialize the root window for the main GUI
root = tk.Tk()
root.title("Quiz Application")
root.geometry("400x250")

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
    admin_window.geometry("300x300")
    ttk.Label(admin_window, text="Welcome to Admin Settings", font=("Arial", 14)).pack(pady=50)
    populate_admin_window(admin_window)

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

def add_question():
    add_win = tk.Toplevel()
    add_win.title("Add New Question")

    # Dropdown for course
    tk.Label(add_win, text="Course:").grid(row=0, column=0, sticky='w')
    course_entry = ttk.Combobox(add_win, values=["DS3850", "FIN3210", "DS3620", "BMGT3510", "DS3860"])
    course_entry.grid(row=0, column=1)

    # Question text
    tk.Label(add_win, text="Question:").grid(row=1, column=0, sticky='w')
    question_entry = tk.Entry(add_win, width=50)
    question_entry.grid(row=1, column=1)

    choices_entries = []
    for i in range(4):
        tk.Label(add_win, text=f"Choice {chr(65+i)}:").grid(row=2+i, column=0, sticky='w')
        entry = tk.Entry(add_win, width=40)
        entry.grid(row=2+i, column=1)
        choices_entries.append(entry)

    # Correct answer index
    tk.Label(add_win, text="Correct Index (0-3):").grid(row=6, column=0, sticky='w')
    correct_index_entry = tk.Entry(add_win, width=5)
    correct_index_entry.grid(row=6, column=1, sticky='w')

    def save_question():
        try:
            course = course_entry.get()
            question_text = question_entry.get()
            choices = [entry.get() for entry in choices_entries]
            correct_index = int(correct_index_entry.get())

            q = Question(course, question_text, choices, correct_index)
            save_many_questions([q])
            messagebox.showinfo("Success", "Question added successfully!")
            add_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(add_win, text="Save Question", command=save_question).grid(row=7, columnspan=2, pady=10)

def view_table():
    table = simpledialog.askstring("View Table", "Enter course name (e.g., DS3850):")
    if not table:
        return

    view_win = tk.Toplevel()
    view_win.title(f"{table} Questions")

    conn = sqlite3.connect("questionsdb.db")
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            tk.Label(view_win, text=str(row)).grid(row=i, column=0, sticky='w')
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def delete_question():
    course = simpledialog.askstring("Delete Question", "Course name:")
    q_id = simpledialog.askinteger("Delete Question", "Question ID to delete:")

    if course and q_id is not None:
        conn = sqlite3.connect("questionsdb.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"DELETE FROM {course} WHERE id = ?", (q_id,))
            conn.commit()
            messagebox.showinfo("Deleted", f"Question {q_id} deleted from {course}.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

def modify_question():
    course = simpledialog.askstring("Modify Question", "Course name:")
    q_id = simpledialog.askinteger("Modify Question", "Question ID to modify:")

    if course and q_id is not None:
        conn = sqlite3.connect("questionsdb.db")
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT * FROM {course} WHERE id = ?", (q_id,))
            question_row = cursor.fetchone()

            if question_row:
                edit_win = tk.Toplevel()
                edit_win.title("Edit Question")

                tk.Label(edit_win, text="Question:").grid(row=0, column=0, sticky='w')
                question_entry = tk.Entry(edit_win, width=50)
                question_entry.insert(0, question_row[1])
                question_entry.grid(row=0, column=1)

                choices_entries = []
                for i in range(4):
                    tk.Label(edit_win, text=f"Choice {chr(65+i)}:").grid(row=i+1, column=0, sticky='w')
                    entry = tk.Entry(edit_win, width=40)
                    entry.insert(0, question_row[i+2])
                    entry.grid(row=i+1, column=1)
                    choices_entries.append(entry)

                tk.Label(edit_win, text="Correct Index (0-3):").grid(row=5, column=0, sticky='w')
                correct_index_entry = tk.Entry(edit_win, width=5)
                correct_index_entry.insert(0, question_row[6])
                correct_index_entry.grid(row=5, column=1, sticky='w')

                def save_changes():
                    try:
                        new_question = question_entry.get()
                        new_choices = [e.get() for e in choices_entries]
                        new_index = int(correct_index_entry.get())

                        cursor.execute(f"""
                            UPDATE {course}
                            SET question = ?, choice_a = ?, choice_b = ?, choice_c = ?, choice_d = ?, correct_index = ?
                            WHERE id = ?
                        """, (new_question, *new_choices, new_index, q_id))
                        conn.commit()
                        messagebox.showinfo("Success", "Question updated successfully.")
                        edit_win.destroy()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

                tk.Button(edit_win, text="Save Changes", command=save_changes).grid(row=6, columnspan=2, pady=10)
            else:
                messagebox.showwarning("Not Found", "No question found with that ID.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()


# Call this inside your existing open_admin_window() function
def populate_admin_window(admin_window):
    ttk.Button(admin_window, text="Add New Question", command=add_question).pack(pady=5)
    ttk.Button(admin_window, text="View Course Table", command=view_table).pack(pady=5)
    ttk.Button(admin_window, text="Delete a Question", command=delete_question).pack(pady=5)
    ttk.Button(admin_window, text="Modify a Question", command=modify_question).pack(pady=5)


def open_quiz_window():
    quiz_window = tk.Toplevel(root)
    quiz_window.title("Quiz")
    quiz_window.geometry("350x200")

    ttk.Label(quiz_window, text="Choose a Course", font=("Arial", 14)).pack(pady=10)

    # Dropdown for selecting course
    selected_course = tk.StringVar()
    course_dropdown = ttk.Combobox(
        quiz_window, 
        textvariable=selected_course, 
        values=["DS3850", "FIN3210", "DS3620", "BMGT3510", "DS3860"]
    )
    course_dropdown.pack(pady=10)

from coursequestions import Question  # Importing the Question class

def open_quiz_window():
    quiz_window = tk.Toplevel(root)
    quiz_window.title("Quiz")
    quiz_window.geometry("400x250")

    ttk.Label(quiz_window, text="Choose a Course", font=("Arial", 14)).pack(pady=10)

    selected_course = tk.StringVar()
    course_dropdown = ttk.Combobox(
        quiz_window,
        textvariable=selected_course,
        values=["DS3850", "FIN3210", "DS3620", "BMGT3510", "DS3860"]
    )
    course_dropdown.pack(pady=10)

    def start_quiz():
        course = selected_course.get()
        if not course:
            messagebox.showwarning("Missing Selection", "Please select a course first.")
            return

        questions = Question.get_all_questions_for_course(course)
        if not questions:
            messagebox.showinfo("Empty", f"No questions available in {course}.")
            return

        random.shuffle(questions)
        questions = questions[:10]  # ✅ limit to 10 questions max

        course_dropdown.pack_forget()
        start_button.pack_forget()

        current_q = {'index': 0}
        score = {'correct': 0}

        question_label = tk.Label(quiz_window, text="", wraplength=350, font=("Arial", 12))
        question_label.pack(pady=10)

        answer_buttons = []
        for i in range(4):
            btn = tk.Button(quiz_window, text="", width=40, wraplength=300)
            btn.pack(pady=2)
            answer_buttons.append(btn)

        feedback_label = tk.Label(quiz_window, text="", font=("Arial", 10))
        feedback_label.pack(pady=5)

        score_label = tk.Label(quiz_window, text="Score: 0", font=("Arial", 12))
        score_label.pack(pady=5)

        def show_question():
            feedback_label.config(text="")

            if current_q['index'] >= len(questions):
                question_label.config(text="🎉 Quiz complete!")
                for btn in answer_buttons:
                    btn.pack_forget()

                feedback_label.config(
                    text=f"Final Score: {score['correct']} / {len(questions)}",
                    fg="blue"
                )

                def return_to_menu():
                    quiz_window.destroy()

                tk.Button(
                    quiz_window,
                    text="Return to Course Selection",
                    font=("Arial", 11),
                    command=return_to_menu
                ).pack(pady=10)

                return

            q = questions[current_q['index']]
            question_label.config(text=f"Q{current_q['index']+1}: {q.question_text}")
            choices = q.choices
            correct_index = q.correct_index

            def make_click_handler(index):
                def handle_click():
                    if index == correct_index:
                        feedback_label.config(text="✅ Correct!", fg="green")
                        score['correct'] += 1
                    else:
                        feedback_label.config(
                            text=f"❌ Incorrect. Correct answer: {choices[correct_index]}",
                            fg="red"
                        )
                    score_label.config(text=f"Score: {score['correct']}")
                    current_q['index'] += 1
                    quiz_window.after(1500, show_question)
                return handle_click

            for i, btn in enumerate(answer_buttons):
                btn.config(text=f"{chr(65+i)}. {choices[i]}", command=make_click_handler(i))

        show_question()

    start_button = ttk.Button(quiz_window, text="Start Quiz", command=start_quiz)
    start_button.pack(pady=10)


# Add these at the bottom of your script before root.mainloop()

welcome_label = ttk.Label(root, text="Welcome to the Quiz App", font=("Arial", 14))
welcome_label.pack(pady=20)

admin_button = ttk.Button(root, text="Admin Login", command=open_admin_login)
admin_button.pack(pady=10)

quiz_taker_button = ttk.Button(root, text="Take a Quiz", command=open_quiz_window)
quiz_taker_button.pack(pady=10)




# Run the app
root.mainloop()
