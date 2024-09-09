import tkinter as tk

tasks = ['Complete Python project update – Work on Tkinter to-do app',
'Grocery shopping – Buy essentials for the week',
'Exercise – 30-minute workout or a run',
'Call a friend or family member – Catch up with someone',
'Read 20 pages of a book – Choose any book you\'re currently reading',
'Organize workspace – Clean and tidy your desk or home office',
'Reply to emails – Clear out your inbox and respond to important messages',
'Prepare meals for the week – Meal prep to save time during the week',
'Review Python programming concepts – Go over recent lessons or notes',
'Plan weekend activities – Schedule time for relaxation or hobbies']

def add_task():
    task = task_entry.get().strip()
    if task != "":
        tasks.append(task)
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)

def delete_task():
    global tasks
    tasks_to_be_deleted = task_listbox.curselection()
    tasks = [task for index, task in enumerate(tasks) if index not in tasks_to_be_deleted]
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

def toggle_task():
    global tasks
    tasks_to_be_toggled = task_listbox.curselection()
    for index, task in enumerate(tasks_to_be_toggled):
        if tasks[task].startswith('✅'):   #✅ task
            tasks[task] = tasks[task][2:]
        else:
            tasks[task] = '✅ ' + tasks[task]
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)


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
del_button = tk.Button(window, text="Delete Task", command=delete_task)
del_button.grid(row = 1, column = 8)
# Toggle button
toggle_button = tk.Button(window, text="Toggle Task", command=toggle_task)
toggle_button.grid(row = 2, column = 8)

# Listbox
task_listbox = tk.Listbox(window,selectmode=tk.MULTIPLE, width = 100, height = 30)   
for i, task in enumerate(tasks):
    task_listbox.insert(i, task)
task_listbox.grid(row = 1, column = 0, columnspan = 8, rowspan = 8, padx = 10)


window.mainloop()