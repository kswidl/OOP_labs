import tkinter as tk
from tkinter import messagebox
from functools import partial

from shape_type import ShapeType


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None

        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip is not None:
            return

        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tip,
            text=self.text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padx=5,
            pady=3
        )
        label.pack()

    def hide(self, event=None):
        if self.tip is not None:
            self.tip.destroy()
            self.tip = None


class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")

        self.current_shape = ShapeType.POINT
        self.shape_var = tk.StringVar(value=self.current_shape.name)

        self.icons = []

        self.update_title()
        self.create_menu()
        self.create_toolbar()
        self.create_canvas()

    def update_title(self):
        self.root.title(
            f"Lab3 - Графічний редактор | {self.current_shape.value}"
        )

    def select_shape(self, shape_type):
        self.current_shape = shape_type
        self.shape_var.set(shape_type.name)
        self.update_title()

    def create_menu(self):
        self.menu = tk.Menu(self.root)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(
            label="Вихід",
            command=self.root.quit
        )

        self.menu.add_cascade(
            label="Файл",
            menu=file_menu
        )

        objects_menu = tk.Menu(self.menu, tearoff=0)

        for shape_type in ShapeType:
            objects_menu.add_radiobutton(
                label=shape_type.value,
                variable=self.shape_var,
                value=shape_type.name,
                command=partial(self.select_shape, shape_type)
            )

        self.menu.add_cascade(
            label="Об'єкти",
            menu=objects_menu
        )

        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(
            label="Про програму",
            command=self.show_about
        )

        self.menu.add_cascade(
            label="Довідка",
            menu=help_menu
        )

        self.root.config(menu=self.menu)

    def create_icon(self, shape_type):
        image = tk.PhotoImage(width=32, height=32)

        for x in range(32):
            for y in range(32):
                color = None

                if shape_type == ShapeType.POINT:
                    if (x - 16) ** 2 + (y - 16) ** 2 <= 12:
                        color = "black"

                elif shape_type == ShapeType.LINE:
                    if abs(y - (31 - x)) <= 1:
                        color = "black"

                elif shape_type == ShapeType.RECTANGLE:
                    if 5 <= x <= 26 and 7 <= y <= 24:
                        if x in (5, 26) or y in (7, 24):
                            color = "black"
                        else:
                            color = "yellow"

                elif shape_type == ShapeType.ELLIPSE:
                    value = ((x - 16) / 12) ** 2 + ((y - 16) / 8) ** 2
                    if 0.85 <= value <= 1.15:
                        color = "black"

                if color:
                    image.put(color, (x, y))

        return image

    def create_toolbar(self):
        self.toolbar = tk.Frame(
            self.root,
            bd=1,
            relief=tk.RAISED
        )
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        for shape_type in ShapeType:
            icon = self.create_icon(shape_type)
            self.icons.append(icon)

            button = tk.Button(
                self.toolbar,
                image=icon,
                width=36,
                height=36,
                command=partial(self.select_shape, shape_type)
            )
            button.pack(side=tk.LEFT, padx=2, pady=2)

            ToolTip(button, shape_type.value)

    def create_canvas(self):
        self.canvas = tk.Canvas(
            self.root,
            bg="white"
        )
        self.canvas.pack(
            fill=tk.BOTH,
            expand=True
        )

    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Графічний редактор Lab3"
        )


root = tk.Tk()
app = GraphicEditor(root)
root.mainloop()