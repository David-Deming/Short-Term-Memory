import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import os

# Initialize global variables
is_notes_mode = True  # Indicates whether we're in notes mode

def load_todos():
    todo_file = os.path.join(os.path.expanduser("~/Notes"), "todo.txt")
    if os.path.exists(todo_file):
        with open(todo_file, 'r') as f:
            return f.read()
    return ""

def switch_to_notes(event=None):
    global is_notes_mode
    is_notes_mode = True
    text_area.pack_forget()
    note_area.pack(fill=tk.BOTH, expand=True)
    note_area.focus_set()

def switch_to_todos(event=None):
    global is_notes_mode
    is_notes_mode = False
    note_area.pack_forget()
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", load_todos())
    text_area.focus_set()

def save_content(event=None):
    global is_notes_mode
    content = note_area.get("1.0", tk.END).strip() if is_notes_mode else text_area.get("1.0", tk.END).strip()
    current_time = datetime.now().strftime("[%H:%M] ")

    if is_notes_mode:
        filename = datetime.now().strftime("%m-%d-%y") + ".txt"
        full_path = os.path.join(os.path.expanduser("~/Notes"), filename)

        # Check if the file already exists
        if not os.path.exists(full_path):
            # Create the header with ASCII art
            ascii_art = '''
                                /
                           ,.. /
                         ,'   ';
              ,,.__    _,' /';  .
             :','  ~~~~    '. '~'
            :' (   )         )::,
            '; '~~~~~~~~~~~~ .;'
'''

            header = f"------------------------------------------------\n{ascii_art}\n------------------------------------------------\n              Notes for {datetime.now().strftime('%m-%d-%y')}\n------------------------------------------------\n"

            # Write the header to the file only if it's a new file
            with open(full_path, 'w') as f:
                f.write(header)

        # Append the current note to the file
        with open(full_path, 'a') as f:
            f.write(current_time + content + "\n")

        note_area.delete("1.0", tk.END)
    else:
        full_path = os.path.join(os.path.expanduser("~/Notes"), "todo.txt")
        with open(full_path, 'w') as f:
            f.write(content + "\n")

    print(f"Saved content to {full_path}")


def insert_newline(event):
    if is_notes_mode:
        text_area.insert(tk.INSERT, '\n')
    else:
        note_area.insert(tk.INSERT, '\n')
    return "break"

def toggle_todo(event=None):
    if is_notes_mode:
        switch_to_todos()
    else:
        switch_to_notes()

def toggle_notes(event=None):
    if is_notes_mode:
        switch_to_todos()
    else:
        switch_to_notes()

def close_program(event=None):
    root.quit()


root = tk.Tk()
root.title("Note and To-do Taker")
root.geometry("400x400")
root.configure(bg='#4B0082')
root.attributes("-alpha", 0.9)

note_area = scrolledtext.ScrolledText(root, width=50, height=20, bg='#4B0082', fg='white', insertbackground='black')
note_area.pack(fill=tk.BOTH, expand=True)
text_area = scrolledtext.ScrolledText(root, width=50, height=20, bg='#4B0082', fg='white', insertbackground='black')
text_area.pack_forget()

# Set up keyboard shortcuts
text_area.bind('<Control-w>', lambda e: root.quit())
text_area.bind('<Alt-Return>', insert_newline)
text_area.bind('<Return>', save_content)
text_area.bind('<Alt-t>', toggle_todo)
text_area.bind('<Alt-n>', toggle_notes)
text_area.bind('<Control-s>', save_content)

note_area.bind('<Control-w>', close_program)
note_area.bind('<Return>', save_content)
note_area.bind('<Alt-t>', toggle_todo)
note_area.bind('<Alt-n>', toggle_notes)
note_area.bind('<Control-s>', save_content)

button_frame = tk.Frame(root, bg='#4B0082')
button_frame.pack(side=tk.BOTTOM, fill=tk.X)

switch_notes_button = tk.Button(button_frame, text="Switch to Notes", command=switch_to_notes, bg='#8B00FF', fg='white')
switch_notes_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
switch_todo_button = tk.Button(button_frame, text="Switch to To-dos", command=switch_to_todos, bg='#8B00FF', fg='white')
switch_todo_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)

note_area.focus_set()

root.mainloop()
