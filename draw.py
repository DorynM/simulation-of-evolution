import pygame as p
from pygame.locals import QUIT

BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0, 255)
RED = (255, 0, 0, 255)


def __draw_food(root, foods):
    """Функция отрисовки еды на поле
    """
    for food in foods:
        if root.get_at((food.position[0], food.position[1])) == WHITE:
            p.draw.rect(root, GREEN, (food.position[0], food.position[1], 19,
                                      19))


def __draw_meat(root, meats):
    """Функция отрисовки мяса на поле
    """
    for meat in meats:
        p.draw.rect(root, RED, (meat.position[0], meat.position[1], 19, 19))


def draw_first_cell(root, cells):
    """Функция отрисовки клеток на поле в самом начале симуляции
    """
    for cell in cells:
        p.draw.rect(root, cell.colour, (cell.position[0], cell.position[1], 19,
                                        19))


def draw_cell(root, cell, objects_positions, meat_positions, food_positions,
              cell_positions, age):
    """Функция отрисовки клетки после её передвижения
    """
    cell.move(root.get_width(), root.get_height(), objects_positions,
              meat_positions, food_positions, cell_positions, age)
    p.draw.rect(root, cell.colour, (cell.position[0], cell.position[1],
                                    19, 19))


def __draw_grid(root):
    """Функция отрисовки линий на поле
    """
    root.fill(WHITE)
    for i in range(0, root.get_height() // 20):
        p.draw.line(root, BLACK, (0, i * 20), (root.get_width(), i * 20))
    for j in range(0, root.get_width() // 20):
        p.draw.line(root, BLACK, (j * 20, 0), (j * 20, root.get_height()))


def start_draw(root, cells):
    """Функция вызывающая функции __draw_grid и draw_first_cell
    """
    __draw_grid(root)
    draw_first_cell(root, cells)


def draw_simulation(root, foods, meats):
    """Функция отрисоки линий, еды и мяса на поле
    """
    for i in p.event.get():
        if i.type == QUIT:
            quit()
    __draw_grid(root)
    __draw_food(root, foods)
    __draw_meat(root, meats)
