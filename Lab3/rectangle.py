from shape import Shape


class Rectangle(Shape):
    def __init__(self, center_x, center_y, corner_x, corner_y):
        dx = abs(corner_x - center_x)
        dy = abs(corner_y - center_y)

        super().__init__(
            center_x - dx,
            center_y - dy,
            center_x + dx,
            center_y + dy
        )

    def draw(self, canvas):
        x1, y1, x2, y2 = self.get_coords()

        canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="black",
            width=2
        )