#----------------- Author: Omendra Kumar Upadhyay (Date:24/07/2025) --------------------
"""
    The code creates a GUI-based virtual keypad for inputting boolean expressions with buttons for
    operators and variable typing.
    
    :param symbol: The `symbol` parameter in the `insert_at_cursor` function is a string representing
    the symbol that needs to be inserted at the current cursor position in the entry field
"""
#---------------------------------------------------------------------------------------
# code for boolean expression input using GUI based virtual keypad.
#--------- Code Starts -----------------------------------------------------------------
import tkinter as tk
from tkinter import messagebox

# === Function to insert symbol at cursor and move cursor ahead === #
def insert_at_cursor(symbol):
    position = entry.index(tk.INSERT)
    entry.insert(position, symbol)
    entry.icursor(position + len(symbol))  # Move cursor forward

# === Clear entry field === #
def clear_expression():
    entry.delete(0, tk.END)

# === Delete character before cursor === #
def backspace():
    position = entry.index(tk.INSERT)
    if position > 0:
        entry.delete(position - 1)
        entry.icursor(position - 1)

# === Submit expression === #
def submit_expression():
    expr = entry.get()
    if expr.strip():
        messagebox.showinfo("Expression Submitted", f"Your expression: {expr}")
    else:
        messagebox.showwarning("Empty Expression", "Please enter a Boolean expression.")

# === Auto-uppercase typed characters === #
def auto_uppercase(event):
    current_text = entry.get()
    position = entry.index(tk.INSERT)
    new_text = ''
    for char in current_text:
        new_text += char.upper() if char.isalpha() else char
    entry.delete(0, tk.END)
    entry.insert(0, new_text)
    entry.icursor(position)

# === GUI Setup === #
root = tk.Tk()
root.title("Boolean Expression Solver - Part 1")
root.geometry("480x430")
root.resizable(False, False)

# === Entry display === #
entry = tk.Entry(root, font=("Consolas", 20), width=28, bd=3, relief="sunken")
entry.pack(pady=20)
entry.bind("<KeyRelease>", auto_uppercase)

# === Frame for keypad === #
keypad_frame = tk.Frame(root)
keypad_frame.pack(pady=10)

# Button config: (text on button, inserted value)
row1 = [("AND (.)", '.'), ("OR (+)", '+'), ("NOT (')", "'")]
row2 = [("(", '('), (")", ')'), ("XOR (⊕)", '^')]
row3 = [("← Back", 'back'), ("Clear", 'clear'), ("✅ Submit", 'submit')]

def create_button_row(row_data, master):
    frame = tk.Frame(master)
    frame.pack(pady=4)
    for label, val in row_data:
        action = {
            'clear': clear_expression,
            'back': backspace,
            'submit': submit_expression
        }.get(val, lambda v=val: insert_at_cursor(v))

        tk.Button(
            frame,
            text=label,
            width=12,
            height=2,
            font=("Arial", 11),
            command=action
        ).pack(side=tk.LEFT, padx=4)

# Create rows
create_button_row(row1, keypad_frame)
create_button_row(row2, keypad_frame)
create_button_row(row3, keypad_frame)

# Instruction label
tk.Label(
    root,
    text="Type variables (A-Z) using keyboard. Use buttons for operators.",
    font=("Arial", 10),
    fg="gray"
).pack(pady=5)

root.mainloop()
