from shape import Shape


class Ellipse(Shape):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(
            min(x1, x2),
            min(y1, y2),
            max(x1, x2),
            max(y1, y2)
        )

    def draw(self, canvas):
        x1, y1, x2, y2 = self.get_coords()

        canvas.create_oval(
            x1, y1, x2, y2,
            outline="black",
            fill="yellow",
            width=2
        )