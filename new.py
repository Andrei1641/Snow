import json
import os.path

import pygame
import sys

from pygame import Surface
from pygame.time import Clock

from snowflake import *
from figure import Figure

from check import Check

from services import *


# setting up all constants
WIDTH: int = 500
HEIGHT:int = 500
BLACK: tuple[int, int, int] = (0, 0, 0)
FIGURE_TYPES: list[str] = ['round', 'rectangle', 'triangle']


# initializing pygame
pygame.init()
screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock: Clock = pygame.time.Clock()
pygame.display.set_caption("DEADLY SNOW - click the snowflakes or game over ...")

check = Check(screen)

# setting up all variables
rand_fig = random.randint(0, len(FIGURE_TYPES) - 1)
snowflakes: list[Figure] = [check.figure_factory(FIGURE_TYPES[rand_fig])]
frames:int = 0

# starting game loop
game_over = False

mouse_pos: tuple[int, int] = 0, 0
old_mouse_pos = None
counter: int = 0

font = pygame.font.SysFont(None, 36)



while not game_over:

    mouse_pos = pygame.mouse.get_pos()

    counter += 1

    # color_change
    if counter > 60:
        for snowflake in snowflakes:
            snowflake.set_color((random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
            counter = 0

    for snowflake in snowflakes:
        cur_x_pos: list = snowflake.get_x()

        #mouse_avoid
        snowflake.avoid_mouse(mouse_pos)


        if old_mouse_pos:
            snowflake.accelerator(old_mouse_pos, mouse_pos)

        # moving snowflakes
        snowflake.move()

        #rotating snowflakes
        snowflake.rotate()

        #border_limitation
        snowflake.border_lim(WIDTH)

        #checking for game over
        if snowflake.hits_the_ground(HEIGHT):
            your_place: int = 0
            first_place_score: int = 0

            app = create_app()
            with app.app_context():
                print(get_users_safe())
                lst = get_users_safe()

            file = {}
            lst.sort(reverse=True)
            print(lst)

            if lst:
                your_place = Check.find(lst, int(Figure.score)) + 1
                first_place_score = lst[0]
                file['scores'] = lst
            else:
                first_place_score = int(Figure.score)
                file['scores'] = [int(Figure.score)]

                your_place = 1


            with app.app_context():
                try:
                    new_user = User(score=Figure.score)

                    db.session.add(new_user)
                    db.session.commit()
                except Exception:
                    with open("data.json", "w") as f:
                        json.dump(file, f)


            for i in snowflakes:
                i.set_color((255, 255, 255))

            snowflake.set_color((255, 0, 0))
            game_over = True

            # Last Renders
            start_ticks = pygame.time.get_ticks()
            paused = True
            while paused:
                seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
                if seconds_passed >= 2:
                    paused = False

                screen.fill((0, 0, 0))
                for f in snowflakes:
                    check.render(f)

                text = font.render("Score: " + str(int(Figure.score)), True, (255, 255, 255))
                screen.blit(text, (10, 10))

                pygame.display.update()


            start_ticks = pygame.time.get_ticks()
            paused = True
            while paused:
                seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
                if seconds_passed >= 5:
                    paused = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                screen.fill((0, 0, 0))

                line2 = font.render(f"Your place is: {your_place}", True, (255, 255, 255))
                line1 = font.render(f"Your Score: {int(Figure.score)} points", True, (255, 255, 255))
                line3 = font.render(f"The first place has: {first_place_score} points", True, (255, 255, 255))


                screen.blit(line1, (80, 200))
                screen.blit(line2, (80, 240))
                screen.blit(line3, (80, 280))

                pygame.display.update()

    old_mouse_pos = mouse_pos

    # generating more and more snow
    while len(snowflakes) < frames // (60 * 60 * 10):
        rand_fig = random.randint(0, len(FIGURE_TYPES) - 1)
        snowflakes.append(check.figure_factory(FIGURE_TYPES[rand_fig]))


    # looking up for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            snowflakes = [snowflake for snowflake in snowflakes if not snowflake.is_collision(mx, my)]
            rand_fig = random.randint(0, len(FIGURE_TYPES) - 1)
            snowflakes.append(check.figure_factory(FIGURE_TYPES[rand_fig]))


    # drawing snowflakes
    screen.fill(BLACK)
    for snowflake in snowflakes:
        check.render(snowflake)

    text = font.render("Score: " + str(int(Figure.score)), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # showing the drawing
    pygame.display.flip()
    clock.tick(60)

    # counting the frames
    frames += 1
