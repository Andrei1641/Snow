from figure import *


class Round(Figure):
    def __init__(self, width: int):
        self.__radius: int = random.randint(11, 20)
        super().__init__(width)
        self._local_center = [0, 0]
        self.points: list[list[int]] = [[self._x, self._y]]

    def get_radius(self) -> int:
        return self.__radius

    def get_center(self) -> list[float]:
        return [self.points[0][0], self.points[0][1]]

    def avoid_mouse(self, mouse_pos: tuple[int, int]):
        if self.detection_limiter(mouse_pos) or not self._has_limiter:
            mouse_x = mouse_pos[0]
            self.points[0][0] += self.avoid_mouse_vector(mouse_x)

    def move(self):
        self.points[0][1] += self._vertical_velocity

    def is_collision(self, x: int, y: int) -> bool:
        dx: int = (self.points[0][0] - x) ** 2
        dy: int = (self.points[0][1] - y) ** 2
        return dx + dy <= self.__radius ** 2

    def hits_the_ground(self, canvas_height: int) -> bool:
        return self.points[0][1] + self.__radius >= canvas_height

    def border_lim(self, canvas_width: int):
        if self.points[0][0] + self.__radius >= canvas_width:
            duty_x = self.points[0][0] + self.__radius - canvas_width
            self.points[0][0] -= duty_x
        elif self.points[0][0] - self.__radius <= 0:
            duty_x = abs(self.points[0][0] - self.__radius)
            self.points[0][0] += duty_x

    def get_x(self) -> list[float]:
        return [self.get_center()[0]]


class Rectangle(Cornered):
    def __init__(self, width: int):
        super().__init__(width)
        self.width = random.randint(30, 60)
        self.height = random.randint(30, 60)
        self._local_center = [self.width / 2, self.height / 2]
        self.points: list = [[self._x, self._y], [self._x + self.width, self._y],
                             [self._x + self.width, self._y + self.height], [self._x, self._y + self.height]]


class Triangle(Cornered):
    def __init__(self, width: int):
        super().__init__(width)
        side_len = random.randint(35, 60)
        in_angle: float = Cornered.inside_angle(3)
        a = [self._x, self._y]
        b = Figure.rotate_point_calc(a[0], a[1], a[0], a[1] + side_len, in_angle)
        c = Figure.rotate_point_calc(b[0], b[1], b[0], b[1] + side_len, -in_angle)
        self.points: list = [a, b, c]