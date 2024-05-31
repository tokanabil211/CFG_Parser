import tkinter as tk
from tkinter import messagebox

class ParseTreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

class CFGParser:
    def __init__(self, cfg):
        self.cfg = self.parse_cfg(cfg)

    def parse_cfg(self, cfg):
        rules = {}
        for line in cfg.split('\n'):
            lhs, rhs = line.split('->')
            rules[lhs.strip()] = [rule.strip() for rule in rhs.split('|')]
        return rules

    def check_string(self, string):
        count = 0
        for char in string:
            if char == '0' or char=='a':
                count += 1
            elif char == '1' or char=='b':
                count -= 1
            else:
                return False
            if count < 0:
                return False
        return count == 0

    def parse(self, string):
        if not self.check_string(string):
            raise ValueError("The given string does not match the CFG rules.")
        
        derivation_steps = []
        parsing_tree = self.build_parse_tree(string, derivation_steps)
        return parsing_tree, derivation_steps

    def build_parse_tree(self, string, derivation_steps):
        root = ParseTreeNode("S")
        stack = [root]

        for char in string:
            step = f"Expand {char}"
            symbol = ParseTreeNode(char)
            stack[-1].children.append(symbol)
            stack.append(symbol)
            derivation_steps.append(step)

        while len(stack) > 1:
            derivation_steps.append("Reduce")
            stack.pop()

        return root


# GUI code
def parse_string():
    cfg_text = cfg_entry.get("1.0", tk.END).strip()
    string = string_entry.get().strip()
    
    if not cfg_text or not string:
        messagebox.showerror("Error", "Please enter both CFG and string.")
        return
    
    try:
        cfg_parser = CFGParser(cfg_text)
        parsing_tree, derivation_steps = cfg_parser.parse(string)
        display_results(parsing_tree, derivation_steps)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_results(parsing_tree, derivation_steps):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Derivation Steps:\n")
    for step in derivation_steps:
        result_text.insert(tk.END, f"{step}\n")
    result_text.insert(tk.END, "\nParse Tree:\n")
    display_parse_tree_in_text(parsing_tree, result_text)

def display_parse_tree_in_text(node, text_widget, indent=0):
    text_widget.insert(tk.END, "  " * indent + node.value + "\n")
    for child in node.children:
        display_parse_tree_in_text(child, text_widget, indent + 1)

# Create GUI
root = tk.Tk()
root.title("CFGparse GUI")

cfg_label = tk.Label(root, text="Enter CFG:")
cfg_label.pack(pady=5)

cfg_entry = tk.Text(root, height=5, width=50)
cfg_entry.pack(pady=5)

string_label = tk.Label(root, text="Enter string:")
string_label.pack(pady=5)

string_entry = tk.Entry(root, width=50)
string_entry.pack(pady=5)

parse_button = tk.Button(root, text="Parse", command=parse_string)
parse_button.pack(pady=5)

result_text = tk.Text(root, height=20, width=80)
result_text.pack(pady=10)

root.mainloop()