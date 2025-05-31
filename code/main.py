import json
from datetime import datetime, timedelta
from colorama import Fore, Style, init

init(autoreset=True)
tasks = []

def main():
    load_tasks()
    while True:
        print("\nTask Tracker Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Save and Exit")

        choice = input("Choose an option (1-4): ")
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_task_done()
        elif choice == '4':
            save_tasks()
            print("Tasks saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def add_task():
    task = input("Enter task description: ")
    due = input("Enter due date (YYYY-MM-DD): ")
    try:
       due_date =  datetime.strptime(due, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format.")
        return
    tasks.append({
        'description': task,
        'due': str(due_date),
        'done': False
    })
    print("Task added!")

def view_tasks():
    if not tasks:
        print("No tasks yet.")
        return

    sorted_tasks = sorted(tasks, key=lambda t: t['due'])

    print("\nYour Tasks:")
    for i, task in enumerate(sorted_tasks):
        status = "✅ Done" if task['done'] else "❌ Not done"
        due_date = datetime.strptime(task['due'], "%Y-%m-%d").date()
        today = datetime.today().date()

        if task['done']:
            color = Fore.GREEN
        elif due_date < today:
            color = Fore.RED
        elif due_date == today + timedelta(days=1):
            color = Fore.YELLOW
        else:
            color = Fore.GREEN

        print(f"{i + 1}. {color}{task['description']} (Due: {task['due']}) - {status}")

def mark_task_done():
    if not tasks:
        print("No tasks to mark.")
        return

    view_tasks()
    try:
        task_num = int(input("Enter task number to mark as done: ")) - 1
        if 0 <= task_num < len(tasks):
            tasks[task_num]['done'] = True
            print("Task marked as done.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Must be a number.")

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            global tasks
            tasks = json.load(f)
    except FileNotFoundError:
        tasks.clear()

if __name__ == '__main__':
    main()
