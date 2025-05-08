import tkinter as tk
from math import sin, cos, tan, log, sqrt, exp, pi, e, radians, degrees
import ast
import operator

class SafeEval:
    allowed_funcs = {
        'sin': sin, 'cos': cos, 'tan': tan,
        'log': log, 'sqrt': sqrt, 'exp': exp,
        'pi': pi, 'e': e
    }
    allowed_ops = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg
    }

    def __init__(self, use_degrees=False):
        self.use_degrees = use_degrees

    def eval_expr(self, expr):
        tree = ast.parse(expr, mode='eval')
        return self._eval(tree.body)

    def _eval(self, node):
        if isinstance(node, ast.BinOp):
            return self.allowed_ops[type(node.op)](self._eval(node.left), self._eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.allowed_ops[type(node.op)](self._eval(node.operand))
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            if func_name not in self.allowed_funcs:
                raise ValueError("Invalid function")
            args = [self._eval(arg) for arg in node.args]
            if func_name in ['sin', 'cos', 'tan'] and self.use_degrees:
                args[0] = radians(args[0])
            return self.allowed_funcs[func_name](*args)
        elif isinstance(node, ast.Name):
            if node.id in self.allowed_funcs:
                return self.allowed_funcs[node.id]
            raise ValueError("Invalid variable")
        else:
            raise ValueError("Invalid expression")

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("400x550")
        self.expression = ""
        self.memory = 0
        self.use_degrees = True
        self.safe_eval = SafeEval(use_degrees=self.use_degrees)

        self.entry = tk.Entry(root, font=('Arial', 20), bg="#2b2b2b", fg="white", bd=0, justify='right')
        self.entry.pack(fill='both', ipadx=8, ipady=25, padx=10, pady=10)

        self.create_buttons()
        self.bind_keys()
        self.root.bind('<Configure>', lambda e: self.resize_layout())

    def bind_keys(self):
        self.root.bind('<Key>', self.key_input)
        self.root.bind('<Return>', lambda event: self.evaluate())
        self.root.bind('<BackSpace>', lambda event: self.delete_last())
        self.root.bind('<Escape>', lambda event: self.clear())

    def key_input(self, event):
        char = event.char
        if char in '0123456789+-*/().^':
            self.add_to_expression(char)

    def add_to_expression(self, value):
        self.expression += str(value)
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def clear(self):
        self.expression = ""
        self.entry.delete(0, tk.END)

    def delete_last(self):
        self.expression = self.expression[:-1]
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def evaluate(self):
        try:
            expr = self.expression.replace('^', '**')
            self.safe_eval.use_degrees = self.use_degrees
            result = str(self.safe_eval.eval_expr(expr))
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, result)
            self.expression = result
        except Exception:
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, "Error")
            self.expression = ""

    def toggle_deg_rad(self):
        self.use_degrees = not self.use_degrees
        mode = "DEG" if self.use_degrees else "RAD"
        self.toggle_btn.config(text=mode)

    def memory_store(self):
        try:
            self.memory = float(self.entry.get())
        except:
            pass

    def memory_recall(self):
        self.add_to_expression(str(self.memory))

    def memory_clear(self):
        self.memory = 0

    def resize_layout(self):
        for widget in self.btns_frame.winfo_children():
            widget.configure(width=max(self.root.winfo_width() // 100, 4))

    def create_buttons(self):
        self.btns_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.btns_frame.pack(expand=True, fill='both')

        buttons = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '^'],
            ['1', '2', '3', '-', 'log'],
            ['0', '.', '(', ')', '+'],
            ['sin', 'cos', 'tan', 'exp', 'pi'],
            ['e', 'M+', 'MR', 'MC', '=']
        ]

        for r, row in enumerate(buttons):
            for c, btn_text in enumerate(row):
                action = lambda x=btn_text: self.on_button_click(x)
                btn = tk.Button(
                    self.btns_frame, text=btn_text, command=action,
                    font=('Arial', 14), width=5, height=2,
                    bg="#333", fg="white", bd=1, relief="raised",
                    activebackground="#555", activeforeground="white"
                )
                btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        for i in range(5):
            self.btns_frame.grid_columnconfigure(i, weight=1)

        self.toggle_btn = tk.Button(self.root, text="DEG", command=self.toggle_deg_rad,
                                    font=('Arial', 14), bg="#444", fg="white")
        self.toggle_btn.pack(fill='x', padx=10, pady=5)

    def on_button_click(self, char):
        if char == "C":
            self.clear()
        elif char == "DEL":
            self.delete_last()
        elif char == "=":
            self.evaluate()
        elif char == "pi":
            self.add_to_expression(str(pi))
        elif char == "e":
            self.add_to_expression(str(e))
        elif char == "M+":
            self.memory_store()
        elif char == "MR":
            self.memory_recall()
        elif char == "MC":
            self.memory_clear()
        elif char in ["sin", "cos", "tan", "log", "sqrt", "exp"]:
            self.add_to_expression(f"{char}(")
        else:
            self.add_to_expression(char)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()
