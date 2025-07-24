#----------------- Author: Omendra Kumar Upadhyay (Date:24/07/2025) --------------------
"""
    The code creates a GUI application in Python using tkinter to generate a truth table for a given
    Boolean expression.
    
    :param expr: The `expr` parameter in the code represents a Boolean expression input by the user.
    This expression can contain logical operators like AND (.), OR (+), NOT ('), and XOR (⊕), along with
    variables (A-Z) and parentheses for grouping. The code processes this expression to generate a
    :return: The code provided is a Python script that creates a GUI application using tkinter for
    generating a truth table based on a given Boolean expression. The script defines functions for
    formatting the expression, extracting variables, evaluating the expression, and displaying the truth
    table in a pop-up window.
"""
#---------------------------------------------------------------------------------------
# code for truth table for the input expression
#------- Code Starts ---------------------------------------------------
import tkinter as tk
from tkinter import messagebox
from itertools import product
from tkinter import ttk


# === Boolean evaluation helpers === #
def format_expression(expr):
    expr = expr.replace('.', ' and ')
    expr = expr.replace('+', ' or ')
    expr = expr.replace("'", ' == 0')  # A' means NOT A
    expr = expr.replace('^', ' != ')   # XOR is a != b
    return expr

def extract_variables(expr):
    return sorted(set(filter(str.isalpha, expr)))

def evaluate_expression(expr, variables):
    formatted_expr = format_expression(expr)
    results = []
    for values in product([0, 1], repeat=len(variables)):
        env = dict(zip(variables, values))
        try:
            result = eval(formatted_expr, {}, env)
            results.append((values, int(result)))
        except Exception:
            results.append((values, 'Error'))
    return results

def show_truth_table(expr):
    variables = extract_variables(expr)
    results = evaluate_expression(expr, variables)

    # Create a new pop-up window
    table_window = tk.Toplevel(root)
    table_window.title("Truth Table")
    table_window.geometry("600x400")
    table_window.resizable(True, True)

    # Create a Treeview widget
    columns = variables + ['Output']
    tree = ttk.Treeview(table_window, columns=columns, show='headings', height=20)

    # Configure column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=60)

    # Insert data
    for values, result in results:
        row = list(values) + [result]
        tree.insert('', tk.END, values=row)

    # Add vertical scrollbar
    vsb = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    # Pack the tree and scrollbar
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

# === GUI Functions for input === #
def insert_at_cursor(symbol):
    position = entry.index(tk.INSERT)
    entry.insert(position, symbol)
    entry.icursor(position + len(symbol))

def clear_expression():
    entry.delete(0, tk.END)

def backspace():
    position = entry.index(tk.INSERT)
    if position > 0:
        entry.delete(position - 1)
        entry.icursor(position - 1)

def submit_expression():
    expr = entry.get()
    if expr.strip():
        try:
            show_truth_table(expr)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Expression.\n{e}")
    else:
        messagebox.showwarning("Empty Expression", "Please enter a Boolean expression.")

def auto_uppercase(event):
    current_text = entry.get()
    position = entry.index(tk.INSERT)
    new_text = ''.join(char.upper() if char.isalpha() else char for char in current_text)
    entry.delete(0, tk.END)
    entry.insert(0, new_text)
    entry.icursor(position)

# === GUI Setup === #
root = tk.Tk()
root.title("Boolean Expression Solver")
root.geometry("500x450")
root.resizable(False, False)

entry = tk.Entry(root, font=("Consolas", 20), width=28, bd=3, relief="sunken")
entry.pack(pady=20)
entry.bind("<KeyRelease>", auto_uppercase)

keypad_frame = tk.Frame(root)
keypad_frame.pack(pady=10)

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

create_button_row(row1, keypad_frame)
create_button_row(row2, keypad_frame)
create_button_row(row3, keypad_frame)

tk.Label(
    root,
    text="Type variables (A-Z) using keyboard. Use buttons for operators.",
    font=("Arial", 10),
    fg="gray"
).pack(pady=5)

root.mainloop()
