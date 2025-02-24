import tkinter as tk
import tkinter.messagebox as messagebox
import re

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg="black")
        self.root.resizable(False, False)

        self.equation = ""

        self.display = tk.Label(root, 
                            font=("Arial", 20), 
                            bg="black", 
                            fg="white", 
                            anchor="e",  
                            width=20, 
                            relief="sunken", 
                            bd=1)       
        self.display.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        self.create_buttons()

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('<', 4, 2), ('/', 4, 3),
            ('(', 5, 0), (')', 5, 1), ('.', 5, 2), ('=', 5, 3)
        ]

        for (text, row, col) in buttons:
            btn_color = "#D68C45" if text in ('=', 'C', '<', '(', ')', '.') else "gray" if text in ('+', '-', '*', '/') else "#E0E0E0"
            btn = tk.Button(self.root, text=text, font=("Arial", 16), width=5, height=2,
                            bg=btn_color, command=lambda t=text: self.on_button_click(t),
                            relief="flat", bd=0, highlightthickness=0)
            btn.configure(borderwidth=1, highlightbackground="black")
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def on_button_click(self, char):
        if char == "=":
            try:
                result = self.evaluate_expression(self.equation)
                self.equation = str(int(result)) if result.is_integer() else str(result) 
            except ZeroDivisionError:
                messagebox.showerror("Error", "Bilangan tidak bisa dibagi 0")
                self.equation = ""
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
                self.equation = ""
        elif char == "C":
            self.equation = ""
        elif char == "<":
            self.equation = self.equation[:-1]
        else:
            self.equation += char
        self.update_display()

    def update_display(self):
        self.display.config(text=self.equation)

    def evaluate_expression(self, expression):
        expression = re.sub(r'\s+', '', expression)
        expression = re.sub(r'(?<!\d|\))-(\d+(\.\d*)?)', r'~\1', expression)
        tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/()]|~\d+\.\d+|~\d+', expression)
        return self.calculate(tokens)

    def calculate(self, tokens):
        def precedence(op):
            return {'+': 1, '-': 1, '*': 2, '/': 2}.get(op, 0)

        def apply_operation(ops, values):
            right = values.pop()
            left = values.pop()
            op = ops.pop()
            if op == '+': values.append(left + right)
            elif op == '-': values.append(left - right)
            elif op == '*': values.append(left * right)
            elif op == '/': 
                if right == 0:
                    raise ZeroDivisionError("Bilangan tidak bisa dibagi 0")
                values.append(left / right)

        values, ops = [], []
        i = 0
        while i < len(tokens):
            if re.match(r'~?\d+(\.\d+)?', tokens[i]): 
                values.append(float(tokens[i].replace('~', '-')))
            elif tokens[i] == '(':
                ops.append(tokens[i])
            elif tokens[i] == ')':
                while ops and ops[-1] != '(':
                    apply_operation(ops, values)
                ops.pop()
            else:
                while ops and ops and precedence(ops[-1]) >= precedence(tokens[i]):
                    apply_operation(ops, values)
                ops.append(tokens[i])
            i += 1

        while ops:
            apply_operation(ops, values)
        return values[0]

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
