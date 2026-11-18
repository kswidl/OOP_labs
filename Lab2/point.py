from shape import Shape

class Point(Shape):
    def __init__(self, x, y):
        super().__init__(x, y, x, y)

    def draw(self, canvas):
        x1, y1, x2, y2 = self.get_coords()

        canvas.create_oval(
            x1 - 4, y1 - 4,
            x1 + 4, y1 + 4,
            fill="black",
            outline="black"
        )