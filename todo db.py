import tkinter as tk
import sqlite3

def initialize_database():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL,
                        completed INTEGER NOT NULL DEFAULT 0
                      )''')
    
    conn.commit()
    conn.close()

def fetch_todo_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT task FROM tasks WHERE completed = 0')
    tasks = cursor.fetchall()
    conn.close()
    return [task[0] for task in tasks]

def fetch_completed_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT task FROM tasks WHERE completed = 1')
    tasks = cursor.fetchall()
    conn.close()
    return [task[0] for task in tasks]

def populate_todo_listbox():
    tasks = fetch_todo_tasks()
    for task in tasks:
        task_listbox.insert(tk.END, task)

def populate_completed_listbox():
    tasks = fetch_completed_tasks()
    for task in tasks:
        completed_task_listbox.insert(tk.END, task)


def add_task():
    task = task_entry.get()
    if task:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()

        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)

def delete_task():
    tasks_to_be_deleted_num = task_listbox.curselection()
    tasks_to_be_deleted = []
    for num in tasks_to_be_deleted_num:
            tasks_to_be_deleted.append(task_listbox.get(num))

    placeholders = ','.join(['?'] * len(tasks_to_be_deleted_num))

    print(placeholders)
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM tasks WHERE task IN ({placeholders})", tasks_to_be_deleted)
    conn.commit()
    conn.close()

    task_listbox.delete(0, tk.END)
    completed_task_listbox.delete(0, tk.END)
    populate_completed_listbox()
    populate_todo_listbox()

def toggle_task():

    todo_tasks_to_be_toggled_num = task_listbox.curselection()
    completed_tasks_to_be_toggled_num = completed_task_listbox.curselection()
    tasks_to_be_toggled = []
    for num in todo_tasks_to_be_toggled_num:
            tasks_to_be_toggled.append(task_listbox.get(num))

    for num in completed_tasks_to_be_toggled_num:
            tasks_to_be_toggled.append(completed_task_listbox.get(num))


    todo_placeholders = ','.join(['?'] * len(todo_tasks_to_be_toggled_num))
    completed_placeholders = ','.join(['?'] * len(completed_tasks_to_be_toggled_num))

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    print(tasks_to_be_toggled)
    for task in tasks_to_be_toggled:
        if task in fetch_todo_tasks():
            cursor.execute(f"UPDATE tasks SET completed = 1 WHERE task = ?", (task,))
        else:
            cursor.execute(f"UPDATE tasks SET completed = 0 WHERE task = ?", (task,))
        conn.commit()
    conn.close()

    task_listbox.delete(0, tk.END)
    populate_todo_listbox()
    completed_task_listbox.delete(0, tk.END)
    populate_completed_listbox()


initialize_database()

# Window
window = tk.Tk()
window.title("To-Do List with Checkboxes")
window.geometry("1000x800")

# Entry widget
task_entry = tk.Entry(window, width=35)
task_entry.grid(row = 0, column = 0, pady = 40, padx = 10)

# Add button
add_button = tk.Button(window, text="Add Task", command=add_task)
add_button.grid(row = 0, column = 1)
# Delete button
del_button = tk.Button(window, text="Delete task(s)", command=delete_task)
del_button.grid(row = 3, column = 8)
# Toggle button
toggle_button = tk.Button(window, text="Toggle task(s)", command=toggle_task)
toggle_button.grid(row = 7, column = 8)

# Completed Tasks Label
todo_tasks_label = tk.Label(text = "ToDo tasks:",anchor=tk.W)
todo_tasks_label.grid(row = 1, column = 0)

# Task Listbox
task_listbox = tk.Listbox(window,selectmode=tk.MULTIPLE, width = 100, height = 15)   
populate_todo_listbox()
task_listbox.grid(row = 2, column = 0, columnspan = 8, rowspan = 2, padx = 10, pady = 20)

# Completed Tasks Label
completed_tasks_label = tk.Label(text = "Completed tasks:")
completed_tasks_label.grid(row = 6, column = 0)


# Completed Task Listbox
completed_task_listbox = tk.Listbox(window,selectmode=tk.MULTIPLE, width = 100, height = 15)   
populate_completed_listbox()
completed_task_listbox.grid(row = 7, column = 0, columnspan = 8, rowspan = 2, padx = 10, pady = 20)


window.mainloop()