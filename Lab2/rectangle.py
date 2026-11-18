from shape import Shape


class Rectangle(Shape):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)

    def draw(self, canvas):
        x1, y1, x2, y2 = self.get_coords()

        canvas.create_rectangle(
            x1, y1,
            x2, y2,
            fill="yellow",
            outline="black",
            width=2
        )