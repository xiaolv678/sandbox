import sys

try:
    import tkinter as tk
    from tkinter import ttk
except ModuleNotFoundError as exc:
    if exc.name != "tkinter":
        raise
    raise SystemExit(
        "tkinter is not installed.\n"
        "On Ubuntu/Debian, install it with:\n"
        "  sudo apt install python3-tk"
    ) from exc

from calculator import Calculator, CalculatorError, evaluate


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.calculator = Calculator()

        self.root.title("Calculator")
        self.root.minsize(320, 440)
        self.root.configure(bg="#f4f1ea")

        self.display_var = tk.StringVar()
        self._build_layout()
        self._bind_keys()

    def _build_layout(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Display.TEntry",
            fieldbackground="#fffdf7",
            foreground="#1f2933",
            bordercolor="#c9c2b8",
            lightcolor="#c9c2b8",
            darkcolor="#c9c2b8",
            padding=12,
        )
        style.configure(
            "Calc.TButton",
            background="#fffdf7",
            foreground="#1f2933",
            bordercolor="#c9c2b8",
            focusthickness=0,
            font=("Arial", 16),
            padding=12,
        )
        style.map("Calc.TButton", background=[("active", "#ebe5da")])
        style.configure(
            "Action.TButton",
            background="#355c7d",
            foreground="#ffffff",
            bordercolor="#28465f",
            font=("Arial", 16),
            padding=12,
        )
        style.map("Action.TButton", background=[("active", "#28465f")])
        style.configure(
            "Clear.TButton",
            background="#c4493d",
            foreground="#ffffff",
            bordercolor="#96362e",
            font=("Arial", 16),
            padding=12,
        )
        style.map("Clear.TButton", background=[("active", "#96362e")])

        container = tk.Frame(self.root, bg="#f4f1ea", padx=14, pady=14)
        container.pack(fill="both", expand=True)

        display = ttk.Entry(
            container,
            textvariable=self.display_var,
            style="Display.TEntry",
            justify="right",
            font=("Arial", 26),
            state="readonly",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 12))

        buttons = [
            ("C", "Clear.TButton"), ("(", "Calc.TButton"), (")", "Calc.TButton"), ("Backspace", "Calc.TButton"),
            ("7", "Calc.TButton"), ("8", "Calc.TButton"), ("9", "Calc.TButton"), ("/", "Action.TButton"),
            ("4", "Calc.TButton"), ("5", "Calc.TButton"), ("6", "Calc.TButton"), ("*", "Action.TButton"),
            ("1", "Calc.TButton"), ("2", "Calc.TButton"), ("3", "Calc.TButton"), ("-", "Action.TButton"),
            ("0", "Calc.TButton"), (".", "Calc.TButton"), ("%", "Calc.TButton"), ("+", "Action.TButton"),
            ("=", "Action.TButton"),
        ]

        for index, (label, button_style) in enumerate(buttons):
            row = index // 4 + 1
            column = index % 4
            columnspan = 4 if label == "=" else 1
            text = "⌫" if label == "Backspace" else label
            button = ttk.Button(
                container,
                text=text,
                style=button_style,
                command=lambda value=label: self._press(value),
            )
            button.grid(
                row=row,
                column=column,
                columnspan=columnspan,
                sticky="nsew",
                padx=4,
                pady=4,
            )

        for column in range(4):
            container.columnconfigure(column, weight=1, uniform="buttons")
        for row in range(6):
            container.rowconfigure(row, weight=1, uniform="buttons")

    def _bind_keys(self):
        self.root.bind("<Return>", lambda _event: self._press("="))
        self.root.bind("<BackSpace>", lambda _event: self._press("Backspace"))
        self.root.bind("<Escape>", lambda _event: self._press("C"))

        for key in "0123456789+-*/%.()":
            self.root.bind(key, lambda _event, value=key: self._press(value))

    def _press(self, value):
        try:
            display = self.calculator.press(value)
        except CalculatorError as exc:
            # Show error message but preserve expression for editing
            display = f"Error: {str(exc)}"
            # Only clear expression on user-initiated clear (C button)
            if value != "C":
                # Reset will happen on next input or manual clear
                pass
            else:
                self.calculator.expression = ""

        self.display_var.set(display)


def main():
    if "--cli" in sys.argv:
        run_cli()
        return

    try:
        root = tk.Tk()
    except tk.TclError as exc:
        if "display" not in str(exc).lower():
            raise
        raise SystemExit(
            "Cannot open the desktop window because this terminal has no display.\n"
            "Run it from a graphical desktop terminal, or use the terminal mode:\n"
            "  python3 main.py --cli"
        ) from exc

    CalculatorApp(root)
    root.mainloop()


def run_cli():
    print("Calculator terminal mode. Type an expression, or type q to quit.")
    while True:
        expression = input("> ").strip()
        if expression.lower() in {"q", "quit", "exit"}:
            break
        try:
            print(evaluate(expression))
        except CalculatorError as exc:
            print(exc)


if __name__ == "__main__":
    main()
