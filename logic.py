from random import randint
from bacteria import Bacteria
from draw import draw_simulation, draw_cell, start_draw
from food import Food
import pygame as p
from grafic import draw_grafic
import tkinter as tk
from threading import Thread, Event
import pickle
from tkinter import filedialog as fd
from meat import Meat


WHITE = (255, 255, 255, 255)
GREEN = (0, 255, 0, 255)
RED = (255, 0, 0, 255)


event = Event()
event.set()


X_NUM = []  # Лист, в котором хранится процент мясоедов
RESTART = False  # Переменная, отвечающая за перезапуск программы
AGE = 80  # Возраст клетки, при котором они будут умирать
LOAD = False  # Если файл загружается, то ставится True
NUMBER_FOOD = 60  # Количество еды в начале симуляции
NUMBER_MEAT = 15  # Количество мяса в начале симуляции
FLAG = True  # Флаг, отвечающий за остановку симуляции
DATA = {}  # Словарь, в котором хранятся данные после сохраненения или загрузки
CELLS = []  # Лист, в котором хранятся все клетки
FOODS = []  # Лист, в котором хранится вся еда
MOTION = [1]  # Лист, в котором записывается шаг симуляции
GENERATIONS = [1]  # Лист, в котором записывается средние поколение клетки
HISTORY_CELLS = []  # Лист, в котором хранится количество клеток на шаге
HISTORY_FOODS = []  # Лист, в котором хранится количество еды на шаге
HISTORY_GEN_VISION = []  # Лист, в котором хранятся гены
WIDTH = 1000  # Ширина окна
HEIGHT = 500  # Высота окна
ROOT = None  # Переменная, в которой хранится окно
FILE_NAME_SAVE = None  # Переменная, в которой хранится путь к файлу сохранения
START = False  # Переменная отвечающая за запуск симуляции
res = []  # Лист, в котором хранятся данные для построения графиков
MEATS = []  # Лист, в котором хранится все мясо
MEAT_POSITIONS = []  # Лист, в котором хранятся все позиции мяса
FOOD_POSITIONS = []  # Лист, в котором хранятся все позиции еды
CELL_POSITIONS = []  # Лист, в котором хранятся все позиции клеток
OBJECTS_POSITIONS = []  # Лист, в котором хранятся все позиции всех объектов


def save(file=None):
    """Функция сохраняет данные в файл
    """
    global NUMBER_FOOD, FLAG, res, DATA, HEIGHT, WIDTH, HISTORY_FOODS
    global FOODS, FILE_NAME_SAVE, MEATS, MOTION, CELLS, ROOT, GENERATIONS
    global HISTORY_CELLS, HISTORY_GEN_VISION

    if file is None:
        FILE_NAME_SAVE = fd.asksaveasfilename(
            filetypes=(("TXT files", "*.txt"),
                       ("HTML files", "*.html;*.htm"),
                       ("All files", "*.*")))
    DATA = {'cells': CELLS,
            'foods': FOODS,
            'number_food': NUMBER_FOOD,
            'motion': MOTION,
            'generations': GENERATIONS,
            'history_cells': HISTORY_CELLS,
            'history_foods': HISTORY_FOODS,
            'history_gen_vision': HISTORY_GEN_VISION,
            'width': WIDTH,
            'height': HEIGHT,
            'MEAT_POSITIONS': MEAT_POSITIONS,
            'FOOD_POSITIONS': FOOD_POSITIONS,
            'CELL_POSITIONS': CELL_POSITIONS,
            'OBJECTS_POSITIONS': OBJECTS_POSITIONS,
            'X_NUM': X_NUM,
            'MEATS': MEATS}
    try:
        with open(FILE_NAME_SAVE, 'wb') as f:
            pickle.dump(DATA, f)
    except FileNotFoundError:
        print('Error open file')


def load():
    """Функция загружает данные с файла
    """
    global NUMBER_FOOD, FLAG, res, DATA, HEIGHT, WIDTH, HISTORY_FOODS, FOODS
    global START, LOAD, X_NUM, MEATS, FILE_NAME_SAVE, CELLS, ROOT
    global HISTORY_CELLS, HISTORY_GEN_VISION, GENERATIONS, MOTION
    global CELL_POSITIONS, OBJECTS_POSITIONS, MEAT_POSITIONS, FOOD_POSITIONS

    file_name = fd.askopenfilename()

    FILE_NAME_SAVE = file_name

    with open(file_name, 'rb') as f:
        DATA = pickle.load(f)
        CELLS = DATA['cells']
        FOODS = DATA['foods']
        HISTORY_CELLS = DATA['history_cells']
        HISTORY_FOODS = DATA['history_foods']
        HISTORY_GEN_VISION = DATA['history_gen_vision']
        MOTION = DATA['motion']
        NUMBER_FOOD = DATA['number_food']
        GENERATIONS = DATA['generations']
        WIDTH = DATA['width']
        HEIGHT = DATA['height']
        OBJECTS_POSITIONS = DATA['OBJECTS_POSITIONS']
        MEAT_POSITIONS = DATA['MEAT_POSITIONS']
        FOOD_POSITIONS = DATA['FOOD_POSITIONS']
        CELL_POSITIONS = DATA['CELL_POSITIONS']
        X_NUM = DATA['X_NUM']
        MEATS = DATA['MEATS']

        START = True
        LOAD = True


def ter():
    """Функция отрисовки окна

        Содержит функции  buttonCallback, button_call, start, restart.
        buttonCallback - функция получает и устанавливает количество еды
        button_call - функция останавливает симуляция
        start - запускает симуляция
        restart - перезапускает симуляцию
    """

    def buttonCallback():
        global NUMBER_FOOD

        event.wait()
        event.clear()
        NUMBER_FOOD = scale_widget.get()
        event.set()

    def button_call():
        global FLAG

        event.wait()
        event.clear()
        FLAG = False
        event.set()

    def start():
        global START
        START = True

    def restart():
        global RESTART
        RESTART = True

    master = tk.Tk()
    scale_widget = tk.Scale(master, orient="horizontal", resolution=1, from_=0,
                            to=1000)
    master.resizable(width=False, height=False)

    label_1 = tk.Label(master, text="Foods")
    label_1.grid(row=0, column=0)
    scale_widget.grid(row=0, column=1)

    button = tk.Button(master, text='enter', command=buttonCallback)
    button.grid(row=1, column=1)
    button_1 = tk.Button(master, text='stop', command=button_call)
    button_1.grid(row=0, column=5)
    button_2 = tk.Button(master, text='save', command=save)
    button_2.grid(row=1, column=2)
    button_2 = tk.Button(master, text='load', command=load)
    button_2.grid(row=1, column=3)
    button_3 = tk.Button(master, text='start', command=start)
    button_3.grid(row=0, column=2)
    button_4 = tk.Button(master, text='restart', command=restart)
    button_4.grid(row=0, column=3)

    tk.mainloop()


def __create_cell(width, height, objects_positions, cell_positions):
    """Функция создает начальное количество клеток
    """
    cells = []

    for index in range(3):
        cell = Bacteria(width, height)
        flag = True

        while flag:
            if cell.position not in objects_positions:
                cells.append(cell)
                cell_positions.append([cell.position[0], cell.position[1]])
                objects_positions.append([cell.position[0], cell.position[1]])
                flag = False
            else:
                cell.position = [randint(0, width // 20) * 20 + 1,
                                 randint(0, height // 20) * 20 + 1]

    return cells


def __create_food(width, height, num_food, food_positions, objects_positions):
    """Функция создает начальное количество еды
    """
    foods = []

    for index in range(num_food):
        food = Food(width, height)
        flag = True

        while flag:
            if food.position not in objects_positions:
                foods.append(food)
                flag = False
                food_positions.append([food.position[0], food.position[1]])
                objects_positions.append([food.position[0], food.position[1]])
            else:
                food.position = [randint(0, width // 20 - 1) * 20 + 1,
                                 randint(0, height // 20 - 1) * 20 + 1]
    return foods


def __create_meat(width, height, num_meat, meat_positions, objects_positions):
    """Функция создает начальное количество мяса
    """
    meats = []

    for index in range(num_meat):
        meat = Meat(width=width, height=height)
        flag = True

        while flag:
            if meat.position not in objects_positions:
                meats.append(meat)
                flag = False
                meat_positions.append([meat.position[0], meat.position[1]])
                objects_positions.append([meat.position[0], meat.position[1]])
            else:
                meat.position = [randint(0, width // 20 - 1) * 20 + 1,
                                 randint(0, height // 20 - 1) * 20 + 1]
    return meats


def __delete_food(root, foods, objects_positions, food_positions):
    """Удаляет еду, которую клетки съели
    """
    delete_food = []

    for food in foods:
        if not root.get_at((food.position[0], food.position[1])) == WHITE \
                and not \
                root.get_at((food.position[0], food.position[1])) == GREEN:
            delete_food.append(food)
    for food in delete_food:
        foods.remove(food)
        objects_positions.remove(food.position)
        food_positions.remove(food.position)


def __delete_meat(root, meats, meat_positions, objects_positions):
    """Удаляет мясо, которое клетки съели
    """
    delete_meat = []

    for meat in meats:
        if not root.get_at((meat.position[0], meat.position[1])) == RED:
            delete_meat.append(meat)

    for meat in delete_meat:
        meats.remove(meat)
        meat_positions.remove(meat.position)
        objects_positions.remove(meat.position)


def __move_cell(root, cells, meats, age, objects_positions, food_positions,
                meat_positions, cell_positions):
    """Функция, отвечающая за движение клетки, а также удаление клеток, которые
       умерли

       Возвращает лист, состоящий из генов зрения клеток, среднее значение
       поколения и процент мясоедов
    """
    delete_cells = []
    generations = []
    radius = []
    gen_move = []
    gen_mea = 0

    for cell in cells:
        generations.append(cell.generation)

        draw_cell(root, cell, objects_positions, meat_positions,
                  food_positions, cell_positions, age)

        if cell.delete:
            meat = Meat(position=cell.position)
            meats.append(meat)
            delete_cells.append(cell)
            objects_positions.remove(cell.position)
            cell_positions.remove(cell.position)
            meat_positions.append([meat.position[0], meat.position[1]])
            objects_positions.append([meat.position[0], meat.position[1]])

    for cell in delete_cells:
        cells.remove(cell)

        radius.append(cell.genome[0])
        gen_move.append(cell.genome[1])
        if cell.genome[2] == 1:
            gen_mea += 1

    if len(cells):
        gen_meat = round(gen_mea / len(cells) * 100, 0)
        return list(set(radius)), sum(generations) / len(generations), gen_meat


def __division(root, width, height, cells, meats, meat_positions,
               objects_positions, cell_positions):
    """Функция, отвечающая за деление клетки, добавление новых клеток и мяса в
       листы
    """
    new_cells = []
    delete_cells = []
    for cell in cells:
        new_cells += cell.division(width, height, root)
        if cell.delete:
            meat = Meat(position=cell.position)
            meats.append(meat)
            delete_cells.append(cell)
            objects_positions.remove(cell.position)
            cell_positions.remove(cell.position)
            objects_positions.append([meat.position[0], meat.position[1]])
            meat_positions.append([meat.position[0], meat.position[1]])

    if len(new_cells):
        for cell in new_cells:
            objects_positions.append([cell.position[0], cell.position[1]])
            cell_positions.append([cell.position[0], cell.position[1]])

    for cell in delete_cells:
        cells.remove(cell)
    cells += new_cells


def __spawn_food(root, width, height, foods, num_food, food_positions,
                 objects_positions):
    """Функция. отвечающая за появление новой еды на карте
    """
    if num_food > len(foods):
        for index in range(num_food - len(foods)):
            food = Food(width, height)
            food.position = [randint(0, width // 20 - 1) * 20 + 1,
                             randint(0, height // 20 - 1) * 20 + 1]
            if root.get_at((food.position[0], food.position[1])) == WHITE:
                food_positions.append([food.position[0], food.position[1]])
                objects_positions.append([food.position[0], food.position[1]])
                foods.append(food)


def start_simulation():
    """Функция, отвечающая за обработку данных на каждом шаге симуляции
    """
    global NUMBER_FOOD, FLAG, res, DATA, HEIGHT, WIDTH, HISTORY_FOODS, FOODS
    global LOAD, FILE_NAME_SAVE, AGE, MEATS, NUMBER_MEAT, X_NUM, RESTART
    global HISTORY_CELLS, HISTORY_GEN_VISION, GENERATIONS, MOTION, CELLS, ROOT
    global CELL_POSITIONS, OBJECTS_POSITIONS, MEAT_POSITIONS, FOOD_POSITIONS

    vision, gene, ge = 0, 0, 0

    ROOT = p.display.set_mode((WIDTH, HEIGHT), p.DOUBLEBUF | p.HWSURFACE)

    """Если данные не загружались, то создаются новые
    """
    if not LOAD:
        CELLS = __create_cell(WIDTH, HEIGHT, OBJECTS_POSITIONS, CELL_POSITIONS)
        start_draw(ROOT, CELLS)
        FOODS = __create_food(WIDTH, HEIGHT, NUMBER_FOOD, FOOD_POSITIONS,
                              OBJECTS_POSITIONS)
        p.display.update()
        MEATS = __create_meat(WIDTH, HEIGHT, NUMBER_MEAT, MEAT_POSITIONS,
                              OBJECTS_POSITIONS)

    ROOT.set_alpha(None)

    sum_x = 0
    for cell in CELLS:
        if cell.genome[2] == 1:
            sum_x += 1

    X_NUM.append(round(sum_x / len(CELLS) * 100, 0))

    clock = p.time.Clock()
    clock.tick(60)

    """Основной цикл, в котором происходит запись данных для построения 
       графиков, а также движения клеток и их деления, удаление съеденной еды и
       мяса
    """
    while FLAG and len(CELLS) and not RESTART:
        HISTORY_CELLS.append(len(CELLS))
        HISTORY_FOODS.append(len(FOODS))

        draw_simulation(ROOT, FOODS, MEATS)
        try:
            vision, gene, ge = __move_cell(ROOT, CELLS, MEATS, AGE,
                                           OBJECTS_POSITIONS,
                                           FOOD_POSITIONS, MEAT_POSITIONS,
                                           CELL_POSITIONS)
        except TypeError:
            pass
        __division(ROOT, WIDTH, HEIGHT, CELLS, MEATS, MEAT_POSITIONS,
                   OBJECTS_POSITIONS, CELL_POSITIONS)
        for item in vision:
            HISTORY_GEN_VISION.append(item)

        if not MOTION[-1] % 300:
            save(FILE_NAME_SAVE)

        MOTION.append(MOTION[-1] + 1)
        __delete_food(ROOT, FOODS, OBJECTS_POSITIONS, FOOD_POSITIONS)
        __delete_meat(ROOT, MEATS, MEAT_POSITIONS, OBJECTS_POSITIONS)

        X_NUM.append(ge)
        GENERATIONS.append(gene)
        __spawn_food(ROOT, WIDTH, HEIGHT, FOODS, NUMBER_FOOD, FOOD_POSITIONS,
                     OBJECTS_POSITIONS)

        p.display.update()

    HISTORY_CELLS.append(len(CELLS))
    HISTORY_FOODS.append(len(FOODS))
    for i in range(len(HISTORY_FOODS) - len(MOTION)):
        MOTION.append(MOTION[-1] + 1)

    for i in range(len(MOTION) - len(GENERATIONS)):
        GENERATIONS.append(GENERATIONS[-1])

    # Лист, в котором содержаться данные для построения графиков
    res = [HISTORY_CELLS, HISTORY_FOODS, MOTION, HISTORY_GEN_VISION,
           GENERATIONS, X_NUM]


def start_program():
    """Функция запуска симуляции
    """
    global NUMBER_FOOD, FLAG, res, DATA, HEIGHT, WIDTH, HISTORY_FOODS, FOODS
    global LOAD, RESTART, X_NUM, MEATS, START, MOTION, CELLS, ROOT
    global HISTORY_CELLS, HISTORY_GEN_VISION, GENERATIONS, FOOD_POSITIONS
    global CELL_POSITIONS, OBJECTS_POSITIONS, MEAT_POSITIONS

    start_simulation()
    """Если не была нажата кнопка рестарта, то вызывается функция построения 
       графиков. Если была нажата, то все параметры сбрасываются
    """
    if not RESTART:
        draw_grafic(res[0], res[1], res[2], res[3], res[4], res[5])
    else:
        RESTART = False
        X_NUM = []
        LOAD = False
        NUMBER_FOOD = 60
        FLAG = True
        DATA = {}
        CELLS = []
        FOODS = []
        MOTION = [1]
        GENERATIONS = [1]
        HISTORY_CELLS = []
        HISTORY_FOODS = []
        HISTORY_GEN_VISION = []
        WIDTH = 1000
        HEIGHT = 500
        ROOT = None
        START = False
        res = []
        MEATS = []
        MEAT_POSITIONS = []
        FOOD_POSITIONS = []
        CELL_POSITIONS = []
        OBJECTS_POSITIONS = []


thread_1 = Thread(target=ter)  # Поток, в котором вызывается окно управления
thread_1.start()
threads = [thread_1]
while True:
    if START:
        start_program()
