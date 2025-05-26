import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from datetime import datetime

tasks = []

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

def refresh_listbox():
    listbox.delete(0, tk.END)
    sorted_tasks = sorted(tasks, key=lambda t: t['due'])
    for i, task in enumerate(sorted_tasks):
        status = "✓" if task['done'] else "✗"
        listbox.insert(tk.END, f"{i+1}. {task['description']} (Due: {task['due']}) [{status}]")

def add_task():
    desc = simpledialog.askstring("Add Task", "Task description:")
    if not desc:
        return
    due = simpledialog.askstring("Add Task", "Due date (YYYY-MM-DD):")
    try:
        datetime.strptime(due, "%Y-%m-%d")  # Validate format
    except ValueError:
        messagebox.showerror("Invalid date", "Date must be in YYYY-MM-DD format.")
        return
    tasks.append({'description': desc, 'due': due, 'done': False})
    refresh_listbox()

def mark_done():
    index = listbox.curselection()
    if not index:
        return
    sorted_tasks = sorted(tasks, key=lambda t: t['due'])
    task_index = tasks.index(sorted_tasks[index[0]])
    tasks[task_index]['done'] = True
    refresh_listbox()

def on_closing():
    save_tasks()
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Task Tracker")

frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=50)
listbox.pack()

button_frame = tk.Frame(root)
button_frame.pack()

tk.Button(button_frame, text="Add Task", command=add_task).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Mark as Done", command=mark_done).grid(row=0, column=1, padx=5)

load_tasks()
refresh_listbox()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
