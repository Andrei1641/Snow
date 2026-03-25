import random

import pygame.draw
from pygame import Surface

from figure import Figure, Cornered
from snowflake import Round, Rectangle, Triangle


class Check:
    def __init__(self, screen: Surface):
        self.screen = screen

    def render(self, figure: Figure):
        if isinstance(figure, Round):
            pygame.draw.circle(self.screen, figure.get_color(), (figure.points[0][0], figure.points[0][1]), figure.get_radius())
        if isinstance(figure, Cornered):
            pygame.draw.polygon(self.screen, figure.get_color(), figure.points, width=0)

    def figure_factory(self, name: str) -> Figure:
        if name == 'round':
            round1 = Round(self.screen.get_width())
            round1.set_limiter(Check.probability_of_mutation(0.7))
            round1.set_accelerator(Check.probability_of_mutation(0.7))
            round1.set_center_accel(Check.probability_of_mutation(0.7))
            return round1
        elif name == 'rectangle':
            rectangle1 = Rectangle(self.screen.get_width())
            rectangle1.set_limiter(Check.probability_of_mutation(0.7))
            rectangle1.set_accelerator(Check.probability_of_mutation(0.7))
            rectangle1.set_center_accel(Check.probability_of_mutation(0.7))
            return rectangle1
        elif name == 'triangle':
            triangle1 = Triangle(self.screen.get_width())
            triangle1.set_limiter(Check.probability_of_mutation(0.7))
            triangle1.set_accelerator(Check.probability_of_mutation(0.7))
            triangle1.set_center_accel(Check.probability_of_mutation(0.7))
            return triangle1
        else:
            return Round(self.screen.get_width())


    @staticmethod
    def probability_of_mutation (probability: float) -> bool:
        if random.random() > probability:
            return True
        return False

    @staticmethod
    def find(lst: list[int], num: int):
        start = 0
        end = len(lst) - 1
        mid = 0

        while start <= end:
            mid = (start + end) // 2

            if num < lst[mid]:
                start = mid + 1
            elif num > lst[mid]:
                end = mid - 1
            else:
                lst.insert(mid, num)
                return mid

        lst.insert(start, num)
        return mid