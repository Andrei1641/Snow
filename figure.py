import random
from abc import ABC, abstractmethod
import math

class Figure(ABC):
    score = 0
    figure_count = 0

    def __init__(self, width: int):
        self._x: int = random.randint(10, width - 10)
        self._y: int = 0
        self._vertical_velocity: int = random.randint(1, 3)
        self.__horizontal_velocity: float = random.randint(0, 10)
        self._color: tuple[int, int, int] = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self._local_center: list[float] = [0.0, 0.0]
        self.points: list[list[float]] = [[0.0, 0.0]]
        self.__rotation_speed: int = random.randint(-10, 10)

        Figure.figure_count += 1

        self._has_limiter: bool = False
        self.__detection_limit: int = random.randint(50, 300)

        self.has_accelerator: bool = False
        self.__ini_horizontal_velocity: float = self.__horizontal_velocity
        self.accel: int = 3

        self.has_center_accel: bool = False

    def __del__(self):
        score = 100
        if self.has_accelerator:
            score += 30
        if self._has_limiter:
            score += 20
        if self.has_center_accel:
            score += 10

        Figure.figure_count -= 1
        multy = Figure.figure_count * 1.5
        score *= multy

        Figure.score += score

    def set_center_accel(self, has_center_accel: bool):
        self.has_center_accel = has_center_accel

    def set_accelerator(self, has_accelerator: bool):
        self.has_accelerator = has_accelerator

    def set_limiter(self, has_limiter: bool):
        self._has_limiter = has_limiter


    def accelerator(self, old_mouse_pos: tuple[int, int], mouse_pos: tuple[int, int]):
        x1: int = mouse_pos[0]
        x2: int = old_mouse_pos[0]
        y1: int = mouse_pos[1]
        y2: int = old_mouse_pos[1]

        if self.has_accelerator:
            if self.__distance_determimant(x1=x1, x2=x2, y1=y1, y2=y2) > 5:
                self.__horizontal_velocity += self.accel
            else:
                self.__horizontal_velocity = self.__ini_horizontal_velocity

        #accelerates when approaching an object
        if self.has_center_accel:
            detection_limit: int = 75
            dist: float = self.__distance_determimant(x1=x1, x2=x2, y1=y1, y2=y2)
            if dist < detection_limit:
                factor: float = (detection_limit - dist) / detection_limit
                self.__horizontal_velocity = self.__ini_horizontal_velocity + factor * 15
            else:
                self.__horizontal_velocity = self.__ini_horizontal_velocity


    def avoid_mouse_vector(self, mouse_x: int) -> float:
        slower: int = 5
        if mouse_x - self.get_center()[0] >= self._local_center[0]:
            return -1 * self.__horizontal_velocity / slower
        else:
            return 1 * self.__horizontal_velocity / slower

    def set_color(self, color: tuple[int, int, int]):
        self._color = color

    def get_color(self) -> tuple[int, int, int]:
        return self._color

    @abstractmethod
    def get_x(self) -> list[float]:
        ...

    @staticmethod
    def rotate_point_calc(cx: float, cy: float, x: float, y: float, rot_angle: float) -> list[float]:
        theta = math.radians(1 * rot_angle)
        dx: float = x - cx
        dy: float = y - cy
        x1: float = dx * math.cos(theta) - dy * math.sin(theta) + cx
        y1: float = dx * math.sin(theta) + dy * math.cos(theta) + cy
        return [x1, y1]


    def rotate(self):
        cx, cy = self.get_center()
        for i in range(len(self.points)):
            x, y = self.points[i]
            x1, y1 = Figure.rotate_point_calc(cx, cy, x, y, self.__rotation_speed)

            self.points[i][0] = x1
            self.points[i][1] = y1

    @staticmethod
    def __distance_determimant(*, x1, x2, y1, y2) -> float:
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def detection_limiter(self, mouse_pos: tuple[int, int]) -> bool:
        x1: float = self.get_center()[0]
        x2: float = mouse_pos[0]
        y1: float = self.get_center()[1]
        y2: float = mouse_pos[1]

        distance: float = self.__distance_determimant(x1=x1, x2=x2, y1=y1, y2=y2)

        if distance > self.__detection_limit:
            return False
        return True

    @abstractmethod
    def get_center(self) -> list[float]:
        ...

    @abstractmethod
    def move(self):
        ...

    @abstractmethod
    def hits_the_ground(self, canvas_height: int) -> bool:
        ...

    @abstractmethod
    def border_lim(self, canvas_width: int):
        ...

    @abstractmethod
    def is_collision(self, x: int, y: int) -> bool:
        ...

    @abstractmethod
    def avoid_mouse(self, mouse_pos: tuple[int, int]):
        ...

class Cornered(Figure, ABC):
    def __init__(self, width: int):
        super().__init__(width)
        self.rotation_speed = random.randint(-10, 10)

    def get_center(self) -> tuple[float, float]:
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return sum(xs) / len(self.points), sum(ys) / len(self.points)

    def avoid_mouse(self, mouse_pos: tuple[int, int]):
        if self.detection_limiter(mouse_pos) or not self._has_limiter:
            mouse_x: int = mouse_pos[0]
            for i in range(len(self.points)):
                self.points[i][0] += self.avoid_mouse_vector(mouse_x)

    @staticmethod
    def inside_angle(corners_count: int) -> float:
        return ((corners_count - 2) * 180) / corners_count


    def move(self):
        for i in range(len(self.points)):
            self.points[i][1] += self._vertical_velocity

    def is_collision(self, x: int, y: int) -> bool:
        lines: list[list] = []

        first_point = self.points[0]
        for i in self.points[1:]:
            second_point = i
            lines.append([first_point, second_point])
            first_point = second_point

        lines.append([self.points[-1], self.points[0]])

        crossing_times: int = 0

        for line in lines:
            x1, y1 = line[0]
            x2, y2 = line[1]

            if (y1 > y) != (y2 > y):
                x_cross = (x2 - x1) * (y - y1) / (y2 - y1) + x1

                if x < x_cross:
                    crossing_times += 1

        return crossing_times % 2 == 1

        # a = self.points[0]
        # b = self.points[1]
        # d = self.points[3]
        # vector_ab = (b[0] - a[0], b[1] - a[1])
        # vector_ad = (d[0] - a[0], d[1] - a[1])
        # vector_am = (x - a[0], y - a[1])
        # dot_product_am_ab = vector_am[0] * vector_ab[0] + vector_am[1] * vector_ab[1]
        # dot_product_ab_ab = vector_ab[0] * vector_ab[0] + vector_ab[1] * vector_ab[1]
        # dot_product_am_ad = vector_am[0] * vector_ad[0] + vector_am[1] * vector_ad[1]
        # dot_product_ad_ad = vector_ad[0] * vector_ad[0] + vector_ad[1] * vector_ad[1]
        #
        # if 0 <= dot_product_am_ab <= dot_product_ab_ab and 0 <= dot_product_am_ad <= dot_product_ad_ad:
        #     return True
        # else:
        #     return False

    def hits_the_ground(self, canvas_height: int) -> bool:
        for i in range(len(self.points)):
            if self.points[i][1] >= canvas_height:
                return True
        return False

    def border_lim(self, canvas_width: int):
        min_x = min(p[0] for p in self.points)
        max_x = max(p[0] for p in self.points)

        if max_x > canvas_width:
            shift = max_x - canvas_width
            for p in self.points:
                p[0] -= shift

        elif min_x < 0:
            shift = -min_x
            for p in self.points:
                p[0] += shift

    def get_x(self) -> list[float]:
        return [p[0] for p in self.points]