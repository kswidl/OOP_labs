import tkinter as tk
from tkinter import messagebox

from point import Point
from line import Line
from rectangle import Rectangle
from ellipse import Ellipse


class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab2 - Графічний редактор")
        self.root.geometry("800x600")

        # Поточний тип об'єкта
        self.current_shape = tk.StringVar(value="Крапка")

        # Масив об'єктів
        self.shapes = []
        self.max_shapes = 112

        # Початкові координати
        self.start_x = 0
        self.start_y = 0

        # Головне меню
        self.menu = tk.Menu(root)

        # Меню Файл
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Вихід", command=root.quit)
        self.menu.add_cascade(label="Файл", menu=file_menu)

        # Меню Об'єкти
        self.objects_menu = tk.Menu(self.menu, tearoff=0)

        self.objects_menu.add_radiobutton(
            label="Крапка",
            variable=self.current_shape,
            value="Крапка",
            command=lambda: self.select_object("Крапка")
        )

        self.objects_menu.add_radiobutton(
            label="Лінія",
            variable=self.current_shape,
            value="Лінія",
            command=lambda: self.select_object("Лінія")
        )

        self.objects_menu.add_radiobutton(
            label="Прямокутник",
            variable=self.current_shape,
            value="Прямокутник",
            command=lambda: self.select_object("Прямокутник")
        )

        self.objects_menu.add_radiobutton(
            label="Еліпс",
            variable=self.current_shape,
            value="Еліпс",
            command=lambda: self.select_object("Еліпс")
        )

        self.menu.add_cascade(
            label="Об'єкти",
            menu=self.objects_menu
        )

        # Меню Довідка
        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(
            label="Про програму",
            command=lambda: messagebox.showinfo(
                "Довідка",
                "Графічний редактор Lab2"
            )
        )

        self.menu.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=self.menu)

        # Робоча область
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Обробка натискання та переміщення миші
        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.preview_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)

    # Вибір типу об'єкта
    def select_object(self, name):
        self.current_shape.set(name)

    # Початок малювання
    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    # Попередній перегляд фігури
    def preview_drawing(self, event):
        self.canvas.delete("preview")

        x1 = self.start_x
        y1 = self.start_y
        x2 = event.x
        y2 = event.y

        shape = self.current_shape.get()

        if shape == "Крапка":
            self.canvas.create_oval(
                x2 - 2, y2 - 2,
                x2 + 2, y2 + 2,
                fill="black",
                outline="black",
                tags="preview"
            )

        elif shape == "Лінія":
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="black",
                width=2,
                tags="preview"
            )

        elif shape == "Прямокутник":
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill="yellow",
                outline="black",
                width=2,
                tags="preview"
            )

        elif shape == "Еліпс":
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            self.canvas.create_oval(
                x1 - dx, y1 - dy,
                x1 + dx, y1 + dy,
                outline="black",
                width=2,
                tags="preview"
            )

    # Завершення малювання
    def finish_drawing(self, event):
        self.canvas.delete("preview")

        if len(self.shapes) >= self.max_shapes:
            messagebox.showwarning(
                "Увага",
                "Досягнуто максимальної кількості об'єктів!"
            )
            return

        x1 = self.start_x
        y1 = self.start_y
        x2 = event.x
        y2 = event.y

        shape = self.current_shape.get()

        if shape == "Крапка":
            obj = Point(x2, y2)

        elif shape == "Лінія":
            obj = Line(x1, y1, x2, y2)

        elif shape == "Прямокутник":
            obj = Rectangle(x1, y1, x2, y2)

        elif shape == "Еліпс":
            obj = Ellipse(x1, y1, x2, y2)

        else:
            return

        self.shapes.append(obj)
        self.redraw()

    # Повторне відображення всіх об'єктів
    def redraw(self):
        self.canvas.delete("all")

        for shape in self.shapes:
            shape.draw(self.canvas)


root = tk.Tk()
app = GraphicEditor(root)
root.mainloop()