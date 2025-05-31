import tkinter as tk
from tkinter import messagebox, simpledialog
from main import tasks, save_tasks, load_tasks  # Reusing shared data and functions
from datetime import datetime

# --- Function to refresh the listbox with current tasks ---
def refresh_task_list():
    listbox.delete(0, tk.END)  # Clear the listbox

    for i, task in enumerate(tasks):
        status = '✅' if task['done'] else '❌'  # Visual task status
        listbox.insert(tk.END, f"{i + 1}. {task['description']} (Due: {task['due']}) {status}")

# --- Function triggered when user clicks "Add Task" button ---
def add_task():
    # Ask for task description
    desc = simpledialog.askstring("Add Task", "Task description:")
    if not desc:
        return  # Cancel if nothing entered

    # Ask for due date
    due = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
    if not due:
        return  # Cancel if nothing entered

    # Validate date format
    try:
        datetime.strptime(due, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format.")
        return

    # Add the task to the shared tasks list
    tasks.append({
        'description': desc,
        'due': due,
        'done': False
    })

    refresh_task_list()  # Update listbox after adding

# --- Function to mark selected task as done ---
def mark_done():
    try:
        # Get index of selected task
        selection = listbox.curselection()[0]

        # Sort tasks again to match listbox order
        sorted_tasks = sorted(tasks, key=lambda t: t['due'])
        task = sorted_tasks[selection]

        # Find original index in the unsorted list to update it
        index = tasks.index(task)
        tasks[index]['done'] = True  # Mark as done

        refresh_task_list()  # Update UI
    except IndexError:
        messagebox.showwarning("Select Task", "No task selected.")

# --- Function to save and exit the program ---
def closing():
    save_tasks()  # Save tasks to JSON file
    root.destroy()  # Close the app window

# --- Load saved tasks before launching GUI ---
load_tasks()

# --- GUI Setup ---
root = tk.Tk()
root.title("Task Tracker")  # Window title

# Main container frame
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# Listbox to show task list
listbox = tk.Listbox(frame, width=60)
listbox.pack()

# Button row container
btn_frame = tk.Frame(frame)
btn_frame.pack(pady=5)

# Add buttons and connect them to functions
tk.Button(btn_frame, text="Add Task", width=15, command=add_task).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Mark as Done", width=15, command=mark_done).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Save & Quit", width=15, command=closing).pack(side=tk.LEFT, padx=5)

# Populate the listbox with any loaded tasks
refresh_task_list()

# --- Start the GUI event loop ---
root.mainloop()
