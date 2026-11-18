import tkinter as tk
from tkinter import messagebox

class GraphicEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab2 - Графічний редактор")
        self.root.geometry("800x600")

        # Головне меню
        self.menu = tk.Menu(root)

        # Меню Файл
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Вихід", command=root.quit)
        self.menu.add_cascade(label="Файл", menu=file_menu)

        # Меню Об'єкти
        self.objects_menu = tk.Menu(self.menu, tearoff=0)

        self.objects_menu.add_command(
            label="Крапка",
            command=lambda: self.select_object("Крапка")
        )

        self.objects_menu.add_command(
            label="Лінія",
            command=lambda: self.select_object("Лінія")
        )

        self.objects_menu.add_command(
            label="Прямокутник",
            command=lambda: self.select_object("Прямокутник")
        )

        self.objects_menu.add_command(
            label="Еліпс",
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
        self.canvas = tk.Canvas(
            root,
            bg="white",
            width=800,
            height=550
        )

        self.canvas.pack(fill=tk.BOTH, expand=True)

    def select_object(self, name):
        pass

root = tk.Tk()
app = GraphicEditor(root)
root.mainloop()