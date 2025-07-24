#----------------- Author: Omendra Kumar Upadhyay (Date:24/07/2025) --------------------
"""
    The provided Python script creates a GUI application for solving boolean expressions, allowing users
    to input expressions, generate truth tables, and simplify expressions using boolean laws and K-map.
    
    :param expr: The `expr` parameter in the provided Python script represents the Boolean expression
    input by the user. It is the expression that the user wants to evaluate, generate a truth table for,
    and simplify using Boolean laws and K-map. The script allows users to interact with this expression
    through a GUI interface, input
    :type expr: str
    :return: The code provided is a Python script that creates a GUI application for solving boolean
    expressions. The script includes functions for generating a truth table from a boolean expression,
    simplifying the expression using boolean laws and K-map, and displaying the simplified form in both
    SOP (Sum of Products) and POS (Product of Sums) formats.
"""
    
#---------------------------------------------------------------------------------------
# Final code for boolean expression solver 
# 1.Takes input expression from user using GUI keypad
# 2.Evalutes for all possible values of variables and gives the truth table
# 3.Finally estimates the simplified form of the expression(standard form) using boolean laws and K-map 
# Boolean Expression Solver: Input GUI -> Truth Table -> Simplify (SOP & POS)
#---------------------------------------------------------------------------
#----------------Code Starts------------------------------------------------
#---------------------------------------------------------------------------
# Importing libraries
import tkinter as tk
from tkinter import messagebox, ttk
from itertools import product
import tempfile, os

# External libs
import sympy as sp
from sympy.logic.boolalg import And, Or, Not, simplify_logic

# ------------------------------------------------------------------
# ----------------------- GLOBAL STATE ------------------------------
# ------------------------------------------------------------------
_last_expr = None           # raw user expression string
_last_vars = []             # list of variable names (strings)
_last_tt_rows = []          # list of (tuple_of_bits, output_int)
_last_tt_window = None      # reference to truth table popup (optional)

# ------------------------------------------------------------------
# ------------- TRUTH TABLE GENERATION -----------------------------
# ------------------------------------------------------------------
def _extract_variables(expr: str):
    return sorted(set(filter(str.isalpha, expr.upper())))


def _evaluate_expr_truth_table(expr: str, variables: list[str]):
    """
    Get truth table by evaluating original expression.
    Build a SymPy expression from the raw syntax,then evaluate with bools.
    This is more reliable than manual Python parsing.
    """
    sym_map = {v: sp.Symbol(v) for v in variables}

    # Parse GUI syntax -> SymPy
    sym_expr = gui_expr_to_sympy(expr, sym_map)

    rows = []
    for bits in product([0, 1], repeat=len(variables)):
        env = {sym_map[v]: bool(b) for v, b in zip(variables, bits)}
        val = int(bool(sym_expr.xreplace(env)))
        rows.append((bits, val))
    return rows


def show_truth_table(expr: str):
    global _last_expr, _last_vars, _last_tt_rows, _last_tt_window

    variables = _extract_variables(expr)
    if not variables:
        messagebox.showerror("Error", "No variables found in expression.")
        return

    # evaluate
    try:
        rows = _evaluate_expr_truth_table(expr, variables)
    except Exception as e:
        messagebox.showerror("Evaluation Error", f"Could not evaluate expression.\n{e}")
        return

    _last_expr = expr
    _last_vars = variables
    _last_tt_rows = rows

    # build popup
    tt_win = tk.Toplevel(root)
    tt_win.title("Truth Table")
    tt_win.geometry("600x400")
    tt_win.resizable(True, True)
    _last_tt_window = tt_win

    cols = variables + ["Output"]
    tree = ttk.Treeview(tt_win, columns=cols, show="headings", height=20)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, anchor="center", width=60)

    for bits, out in rows:
        tree.insert("", tk.END, values=list(bits) + [out])

    vsb = ttk.Scrollbar(tt_win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)

# ------------------------------------------------------------------
# ------------- SIMPLIFICATION ONLY --------------------------------
# ------------------------------------------------------------------
def gui_expr_to_sympy(expr: str, sym_map: dict[str, sp.Symbol]) -> sp.Expr:
    """
    Parse GUI expression (supports ., +, ', ^, parentheses) into a SymPy Boolean expression.
    All variables assumed single uppercase letters.
    NOT is postfix '.
    XOR is ^ button (use sympy ^ bitwise xor on booleans -> Xor)
    """
    import re

    # Tokenize: variables, operators, parentheses, apostrophe
    tokens = []
    i = 0
    expr = expr.replace(" ", "")
    while i < len(expr):
        ch = expr[i]
        if ch.isalpha():
            tokens.append(ch.upper())
        elif ch in ".+()^'":
            tokens.append(ch)
        else:
            raise ValueError(f"Invalid character: {ch}")
        i += 1

    # Handling postfix NOT: collapse VAR ' and ) '
    # First convert tokens into an expression string in SymPy python syntax
    out = []
    i = 0
    while i < len(tokens):
        t = tokens[i]

        if t == "'":
            # applies to previous token: wrap last item with Not(...)
            if not out:
                raise ValueError("Dangling apostrophe at start.")
            prev = out.pop()
            wrapped = f"~({prev})"
            out.append(wrapped)
            i += 1
            continue

        if t == '.':
            out.append("&")
        elif t == '+':
            out.append("|")
        elif t == '^':
            out.append("^")
        elif t in ('(', ')'):
            out.append(t)
        else:  # variable
            out.append(f"{SymName(t)}")
        i += 1

    py_expr = "".join(out)

    # Build python env mapping SymName->symbol
    env = {SymName(k): sym_map[k] for k in sym_map}

    try:
        sym_expr = eval(py_expr, {}, env)
    except Exception as e:
        raise ValueError(f"Parse error in expression '{expr}': {e}")

    return sym_expr


def SymName(ch: str) -> str:
    """Return a safe Python name for a variable symbol (single char)."""
    return f"_{ch}"  # avoid clashing with builtins


def simplify_from_truth_table():
    """
    Use the stored truth table (_last_tt_rows) to produce minimal SOP and POS.
    FIXED: Proper POS calculation using maxterms where output=0
    """
    if not _last_tt_rows:
        messagebox.showwarning("No Data", "Please generate the truth table first.")
        return

    # Build minterms / maxterms
    # Minterm index: interpret bits as binary number (A is MSB)
    minterms = []
    maxterms = []
    n = len(_last_vars)
    
    for bits, out in _last_tt_rows:
        idx = 0
        for b in bits:
            idx = (idx << 1) | b
        if out == 1:
            minterms.append(idx)
        else:
            maxterms.append(idx)

    syms = [sp.Symbol(v) for v in _last_vars]

    # Minimal SOP (DNF) from minterms
    if minterms:
        sop_expr = sp.SOPform(syms, minterms)
    else:
        sop_expr = sp.false  # No minterms means always false

    # FIXED: Minimal POS (CNF) from maxterms
    # POS uses maxterms directly (where output=0)
    if maxterms:
        pos_expr = sp.POSform(syms, maxterms)
    else:
        pos_expr = sp.true  # No maxterms means always true

    show_simplified_window(sop_expr, pos_expr)


def sympy_to_mathematical_notation(expr: sp.Expr) -> str:
    """
    Convert SymPy Boolean expression to mathematical notation:
    & -> .  (AND)
    | -> +  (OR) 
    ~ -> '  (NOT as postfix)
    """
    if expr == sp.true:
        return "1"
    elif expr == sp.false:
        return "0"
    
    # Convert to string and replace operators
    expr_str = str(expr)
    
    # Handle NOT operator (~ becomes postfix ')
    # First handle complex expressions in parentheses with ~
    import re
    
    # Replace ~(expression) with (expression)'
    expr_str = re.sub(r'~\(([^)]+)\)', r"(\1)`", expr_str)  #using raw string format
    
    # Replace ~variable with variable'
    expr_str = re.sub(r'~([A-Z])', r"\1`", expr_str)
    
    # Replacing logical operators
    expr_str = expr_str.replace('&', '.')
    expr_str = expr_str.replace('|', '+')
    
    # Handle any remaining ~ (edge cases)
    expr_str = expr_str.replace('~', '`')
    
    return expr_str


def show_simplified_window(sop_expr: sp.Expr, pos_expr: sp.Expr):
    """
    Popup window to show simplified SOP & POS expressions only.
    """
    win = tk.Toplevel(root)
    win.title("Simplified Expressions")
    win.geometry("800x300")
    win.resizable(True, True)

    # Create a frame for better organization
    main_frame = tk.Frame(win)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Convert expressions to mathematical notation
    sop_math = sympy_to_mathematical_notation(sop_expr)
    pos_math = sympy_to_mathematical_notation(pos_expr)

    # SOP Section
    sop_frame = tk.Frame(main_frame)
    sop_frame.pack(fill=tk.X, pady=(0, 20))
    
    tk.Label(sop_frame, text="Minimal SOP (Sum of Products):", 
             font=("Arial", 14, "bold")).pack(anchor=tk.W)
    
    sop_text = tk.Text(sop_frame, height=3, font=("Consolas", 12), 
                       bg="#f0f8f0", fg="green", wrap=tk.WORD)
    sop_text.pack(fill=tk.X, pady=(5, 0))
    sop_text.insert("1.0", sop_math)
    sop_text.config(state=tk.DISABLED)

    # POS Section
    pos_frame = tk.Frame(main_frame)
    pos_frame.pack(fill=tk.X, pady=(0, 20))
    
    tk.Label(pos_frame, text="Minimal POS (Product of Sums):", 
             font=("Arial", 14, "bold")).pack(anchor=tk.W)
    
    pos_text = tk.Text(pos_frame, height=3, font=("Consolas", 12), 
                       bg="#f0f0f8", fg="blue", wrap=tk.WORD)
    pos_text.pack(fill=tk.X, pady=(5, 0))
    pos_text.insert("1.0", pos_math)
    pos_text.config(state=tk.DISABLED)

    # Adding some helpful information
    info_frame = tk.Frame(main_frame)
    info_frame.pack(fill=tk.X)
    
    info_text = ("Note: SOP is built from minterms\n"
                 "POS is built from maxterms")
    tk.Label(info_frame, text=info_text, font=("Arial", 10), 
             fg="gray", justify=tk.LEFT).pack(anchor=tk.W)

# ------------------------------------------------------------------
# ------------- INPUT GUI ------------------------------------------
# ------------------------------------------------------------------
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

def auto_uppercase(event):
    current_text = entry.get()
    position = entry.index(tk.INSERT)
    new_text = ''.join(char.upper() if char.isalpha() else char for char in current_text)
    entry.delete(0, tk.END)
    entry.insert(0, new_text)
    entry.icursor(position)


# wired to "Truth Table" button
def submit_expression():
    expr = entry.get()
    if expr.strip():
        show_truth_table(expr)
    else:
        messagebox.showwarning("Empty Expression", "Please enter a Boolean expression.")


# wired to "Simplify" button
def simplify_action():
    # If user hasn't generated table yet, do it by default (ensures _last_tt_rows ready)
    expr = entry.get()
    if expr.strip():
        if not _last_tt_rows or expr != _last_expr:
            show_truth_table(expr)  # generate & capture state
        simplify_from_truth_table()
    else:
        messagebox.showwarning("Empty Expression", "Please enter a Boolean expression.")


# ------------------------------------------------------------------
# ---------------------- GUI MAIN WINDOW ---------------------------
# ------------------------------------------------------------------
root = tk.Tk()
root.title("Boolean Expression Solver")
root.geometry("520x420")
root.resizable(False, False)

entry = tk.Entry(root, font=("Consolas", 20), width=28, bd=3, relief="sunken")
entry.pack(pady=20)
entry.bind("<KeyRelease>", auto_uppercase)

keypad_frame = tk.Frame(root)
keypad_frame.pack(pady=10)

# keypad rows
row1 = [("AND (.)", '.'), ("OR (+)", '+'), ("NOT (')", "'")]
row2 = [("(", '('), (")", ')'), ("XOR (^)", '^')]
row3 = [("← Back", 'back'), ("Clear", 'clear'), ("✅ Table", 'submit')]
row4 = [("🔍 Simplify", 'simplify')]

def create_button_row(row_data, master):
    frame = tk.Frame(master)
    frame.pack(pady=4)
    for label, val in row_data:
        action = {
            'clear': clear_expression,
            'back': backspace,
            'submit': submit_expression,
            'simplify': simplify_action
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
create_button_row(row4, keypad_frame)

tk.Label(
    root,
    text="Type variables (A-Z) using keyboard. Use buttons for operators.",
    font=("Arial", 10),
    fg="gray"
).pack(pady=5)

root.mainloop()