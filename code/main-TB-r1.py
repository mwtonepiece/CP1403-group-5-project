import json
from datetime import datetime, timedelta
from colorama import Fore, Style, init

MENU=("Task Tracker Menu:"
      "\n1. Add Task"
      "\n2. View Tasks"
      "\n3. Mark Task as Done"
      "\n4. Save and Exit")

init(autoreset=True)
tasks = []

def main():
    load_tasks()
    print(MENU)
    choice = input("Choose an option (1-4): ")
    while choice != '4':
        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_task_done()
        else:
            print("Invalid choice. Try again.")
        print()
        print(MENU)
        choice = input("Choose an option (1-4): ")
    save_tasks()
    print("Tasks saved. Goodbye!")

def add_task():
    task = input("Enter task description: ")
    if not task:
        print("Task description cannot be empty.")
        return
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
    sorted_tasks = sorted(tasks, key=lambda t: t['due'])
    with open("tasks.json", "w") as out_file:
        json.dump(sorted_tasks, out_file, indent=4)

def load_tasks():
    try:
        with open("tasks.json", "r") as in_file:
            global tasks
            tasks = json.load(in_file)
            today = datetime.today().date()
            overdue = [task for task in tasks if not task['done']
                       and datetime.strptime(task['due'], "%Y-%m-%d").date() < today]
            if overdue:
                print(Fore.RED + f"⚠️ You have {len(overdue)} overdue task(s)!")
    except FileNotFoundError:
        tasks.clear()

main()
