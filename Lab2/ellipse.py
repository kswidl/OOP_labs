from shape import Shape


class Ellipse(Shape):
    def __init__(self, center_x, center_y, corner_x, corner_y):
        x1 = center_x - abs(corner_x - center_x)
        y1 = center_y - abs(corner_y - center_y)
        x2 = center_x + abs(corner_x - center_x)
        y2 = center_y + abs(corner_y - center_y)

        super().__init__(x1, y1, x2, y2)

    def draw(self, canvas):
        x1, y1, x2, y2 = self.get_coords()

        canvas.create_oval(
            x1, y1,
            x2, y2,
            outline="black",
            width=2
        )