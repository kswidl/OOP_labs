import tkinter as tk
from tkinter import messagebox
from functools import partial

from shape_type import ShapeType
from point import Point
from line import Line
from rectangle import Rectangle
from ellipse import Ellipse


# Клас для відображення підказок біля кнопок панелі інструментів
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None

        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    # Показ підказки при наведенні курсора
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

    # Приховування підказки
    def hide(self, event=None):
        if self.tip is not None:
            self.tip.destroy()
            self.tip = None


# Головний клас графічного редактора
class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")

        # Поточний тип графічного об'єкта
        self.current_shape = ShapeType.POINT
        self.shape_var = tk.StringVar(value=self.current_shape.name)

        # Статичний масив для зберігання об'єктів
        self.max_shapes = 113
        self.shapes = [None] * self.max_shapes
        self.shape_count = 0

        # Початкові координати малювання
        self.start_x = 0
        self.start_y = 0

        # Зберігання зображень кнопок панелі інструментів
        self.icons = []

        # Створення основних елементів інтерфейсу
        self.update_title()
        self.create_menu()
        self.create_toolbar()
        self.create_canvas()

    # Оновлення заголовка вікна відповідно до вибраного об'єкта
    def update_title(self):
        self.root.title(
            f"Lab3 - Графічний редактор | {self.current_shape.value}"
        )

    # Вибір типу графічного об'єкта
    def select_shape(self, shape_type):
        self.current_shape = shape_type
        self.shape_var.set(shape_type.name)
        self.update_title()

    # Створення головного меню програми
    def create_menu(self):
        self.menu = tk.Menu(self.root)

        # Меню Файл
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(
            label="Вихід",
            command=self.root.quit
        )

        self.menu.add_cascade(
            label="Файл",
            menu=file_menu
        )

        # Меню Об'єкти з можливістю вибору поточного типу фігури
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

        # Меню Довідка
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

    # Створення графічного зображення для кнопки панелі інструментів
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

                elif shape_type == ShapeType.ELLIPSE:
                    value = ((x - 16) / 12) ** 2 + ((y - 16) / 8) ** 2
                    if 0.85 <= value <= 1.15:
                        color = "black"
                    elif value < 0.85:
                        color = "yellow"

                if color:
                    image.put(color, (x, y))

        return image

    # Створення панелі інструментів із кнопками вибору об'єктів
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

            # Додавання підказки до кнопки
            ToolTip(button, shape_type.value)

    # Створення робочої області та налаштування обробки подій миші
    def create_canvas(self):
        self.canvas = tk.Canvas(
            self.root,
            bg="white"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.preview_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)

    # Запам'ятовування координат початку малювання
    def start_drawing(self, event):
        self.start_x = event.x
        self.start_y = event.y

    # Відображення гумового сліду під час переміщення миші
    def preview_drawing(self, event):
        self.canvas.delete("preview")

        x1 = self.start_x
        y1 = self.start_y
        x2 = event.x
        y2 = event.y

        if self.current_shape == ShapeType.POINT:
            self.canvas.create_oval(
                x2 - 4, y2 - 4,
                x2 + 4, y2 + 4,
                fill="red",
                outline="red",
                tags="preview"
            )

        elif self.current_shape == ShapeType.LINE:
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="red",
                width=2,
                tags="preview"
            )

        elif self.current_shape == ShapeType.RECTANGLE:
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            self.canvas.create_rectangle(
                x1 - dx, y1 - dy,
                x1 + dx, y1 + dy,
                outline="red",
                width=2,
                tags="preview"
            )

        elif self.current_shape == ShapeType.ELLIPSE:
            self.canvas.create_oval(
                min(x1, x2),
                min(y1, y2),
                max(x1, x2),
                max(y1, y2),
                outline="red",
                fill="yellow",
                width=2,
                tags="preview"
            )

    # Завершення малювання та створення об'єкта відповідного класу
    def finish_drawing(self, event):
        self.canvas.delete("preview")

        # Перевірка максимальної кількості об'єктів
        if self.shape_count >= self.max_shapes:
            messagebox.showwarning(
                "Увага",
                "Досягнуто максимальної кількості об'єктів!"
            )
            return

        x1 = self.start_x
        y1 = self.start_y
        x2 = event.x
        y2 = event.y

        # Створення об'єкта залежно від поточного вибору
        if self.current_shape == ShapeType.POINT:
            obj = Point(x2, y2)

        elif self.current_shape == ShapeType.LINE:
            obj = Line(x1, y1, x2, y2)

        elif self.current_shape == ShapeType.RECTANGLE:
            obj = Rectangle(x1, y1, x2, y2)

        elif self.current_shape == ShapeType.ELLIPSE:
            obj = Ellipse(x1, y1, x2, y2)

        else:
            return

        # Додавання об'єкта до масиву
        self.shapes[self.shape_count] = obj
        self.shape_count += 1

        self.redraw()

    # Повторне відображення всіх збережених об'єктів
    def redraw(self):
        self.canvas.delete("all")

        for i in range(self.shape_count):
            self.shapes[i].draw(self.canvas)

    # Відображення інформації про програму
    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Графічний редактор Lab3"
        )


# Створення головного вікна та запуск програми
root = tk.Tk()
app = GraphicEditor(root)
root.mainloop()