from random import randint, choice
from math import sqrt
from food import Food
from meat import Meat


RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
WHITE = (255, 255, 255, 255)


def exit_border(x, y, width, height):
    """Функция, отвечающая за выход клетки с поля
        Мир замкнут в Тор

        Входными аргументами должны быть координаты клетки: x и y, а также
        размеры поля: width, height
        Выходными параметрами являются новые координаты, если клетка вышла за
        поле или старые координаты клетки
    """
    if x < 0:
        x = width + ((x - 1) // 20) * 20 + 1
    elif x > width:
        x = x - width
    if y < 0:
        y = height + ((y - 1) // 20) * 20 + 1
    elif y > height:
        y = y - height

    return x, y


class Bacteria(object):
    """Класс Bacteria используется для создания экземпляра клетки

    Attributes
    ----------
    __movement : int
        используется для запоминания итерации шага клетки
    age : int
        возраст клетки
    generation : int
        номер поколения клетки
    energy : int
        количество энергии у клетки
    genome : list
        хранит в себе геном клетки. В первой ячейке хранится радиус зрения
        клетки, во второй ячейке хранится list с шансами пойти в одном из
        возможных направлений [up, down, left, right], в третьей
        ячейке хранится ген, отвечающий за то, чем питаются клетки
        '0'-растения, а '1'-мясо.
    position : list
        хранит в себе информацию о позиции клетки на поле (x, y)
    memory : list
        хранит в себе информацию о пище, которую они могут есть
    memory_enemy : list
        хранит в себе информацию об объектах, не относящихся к пище
    delete : bool
        жива или мертва клетка
    colour : tuple
        хранит себе цвет в формате RGB

    Methods
    -------
    __inspect(width, height, meat_positions, food_positions,
                  cell_positions)
        Функция отвечает за зрение клетки и запоминает, где находятся другие
        объекты
    __move_rules(width, height, objects_positions, start=False)
        Функция, отвечающая за передвижение клетки, когда нет пищи в поле
        зрения или когда клетка не может пройти к еде.
    __die(age=40)
        Функция определяет, умерла ли клетка от старости
    move(width, height, objects_positions, meat_positions,food_positions,
         cell_positions,  age)
        Функция отвечает за передвижение клетки, когда есть пища или вызывает
        функцию move_rules
    check_energy()
        Функция, отвечающая за смерть клетки от истощения
    __mutation()
        Функция, отвечающая за мутацию клетки
    division(width, height, root)
        Функция, отвечающая за деление клтеки
    """

    def __init__(self, width, height, cell=None, root=None):
        if cell is None:
            self.__movement = 0
            self.age = 1
            self.generation = 1
            self.energy = randint(180, 200)
            self.genome = [2, [60, 0, 20, 20], 0]
            self.position = [randint(0, width // 20 - 1) * 20 + 1,
                             randint(0, height // 20 - 1) * 20 + 1]
            self.memory = []
            self.memory_enemy = []
            self.delete = False
            colour = self.genome[0] * 20
            self.colour = (0 + self.genome[0] * 20, colour, colour)
        else:
            self.age = 1
            self.__movement = 0
            self.generation = cell.generation + 1
            self.energy = randint(180, 200)
            self.genome = []

            for gen in cell.genome:
                if not isinstance(gen, list):
                    self.genome.append(gen)
                else:
                    movements = []
                    for movement in gen:
                        movements.append(movement)
                    self.genome.append(movements)

            self.position = []
            flag = True
            k = 0
            spawn_new = []
            while flag and k < 4:
                x = cell.position[0]
                y = cell.position[1]
                if not k and 0 not in spawn_new:
                    x = cell.position[0] + 20 * 2
                    spawn_new.append(0)
                elif k == 1 and 1 not in spawn_new:
                    x = cell.position[0] - 20 * 2
                    spawn_new.append(1)
                elif k == 2 and 2 not in spawn_new:
                    y = cell.position[1] + 20 * 2
                    spawn_new.append(2)
                elif k == 3 and 3 not in spawn_new:
                    y = cell.position[1] - 20 * 2
                    spawn_new.append(3)

                if x < 0:
                    x = width + ((x - 1) // 20) * 20 + 1
                elif x > width:
                    x = x - width
                if y < 0:
                    y = height + ((y - 1) // 20) * 20 + 1
                elif y > height:
                    y = y - height

                if root.get_at((x, y)) == WHITE:
                    self.position = [cell.position[0], cell.position[1]]
                    flag = False
                k += 1

            self.memory = []
            self.memory_enemy = []
            self.delete = False

            colour = self.genome[0] * 40
            if colour > 255:
                colour /= 17
            self.colour = (0 + self.genome[0] * 20, colour, colour)

    def __inspect(self, width, height, meat_positions, food_positions,
                  cell_positions):
        """Функция, отвечающая за зрение клетки. В данной функции запомимается
        вся еда, которую видит клетка, а также другие клетки и объекты

        Все, что видела клетка, забывается к следующему просмотру территории
        """
        self.memory = []
        self.memory_enemy = []
        radius = self.genome[0]
        x, y = self.position[0], self.position[1] - 20 * radius
        k = 0
        while radius >= 1:
            x, y = exit_border(x, y, width, height)

            if not self.genome[2]:
                if [x, y] in meat_positions or [x, y] in cell_positions:
                    self.memory_enemy.append((x, y))
            else:
                if [x, y] in food_positions or [x, y] in cell_positions:
                    self.memory_enemy.append((x, y))

            if not self.genome[2]:
                if [x, y] in food_positions:
                    if 0 <= k < radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '1', x, y))
                    elif radius <= k < 2 * radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '4', x, y))
                    elif 2 * radius <= k < 3 * radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '3', x, y))
                    elif 3 * radius <= k < 4 * radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '2', x, y))
            else:
                if [x, y] in meat_positions:
                    if 0 <= k < radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '1', x, y))
                    elif radius <= k < 2 * radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '4', x, y))
                    elif 2 * radius <= k < 3 * radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '3', x, y))
                    elif 3 * radius <= k < 4 * radius:
                        self.memory.append((sqrt((x - self.position[0]) ** 2 +
                                                 (y - self.position[1]) ** 2),
                                            '2', x, y))

            if 0 <= k < radius:
                x += 20
                y += 20
            elif radius <= k < 2 * radius:
                x -= 20
                y += 20
            elif 2 * radius <= k < 3 * radius:
                x -= 20
                y -= 20
            elif 3 * radius <= k < 4 * radius:
                x += 20
                y -= 20

            k += 1

            if (radius + 1) * 4 == k:
                radius -= 1
                k = 0
                y += 20

        self.energy -= self.genome[0] * 1.75 + 2
        self.check_energy()

    def __move_rules(self, width, height, objects_positions, start=False):
        """Функция отвечает за движение клетки, когда она не видит еду. Если
            клетка не может пойти в то направление, в которое хочет, то она
            выбирает другое направление случайно. Если клетка не может никуда
            пойти, то она стоит на месте.
        """
        x = self.position[0] - 20
        y = self.position[1]
        x, y = exit_border(x, y, width, height)
        if not start:
            if [x, y] not in objects_positions:
                start = True

        x = self.position[0] + 20
        y = self.position[1]
        x, y = exit_border(x, y, width, height)
        if not start:
            if [x, y] not in objects_positions:
                start = True

        x = self.position[0]
        y = self.position[1] - 20
        x, y = exit_border(x, y, width, height)
        if not start:
            if [x, y] not in objects_positions:
                start = True

        x = self.position[0]
        y = self.position[1] + 20
        x, y = exit_border(x, y, width, height)
        if not start:
            if [x, y] not in objects_positions:
                start = True

        if self.__movement <= 3 and start:
            self.__movement += 1
            chance = randint(0, sum(self.genome[1]))
            index = 0
            for i, gen in enumerate(self.genome[1]):
                chance -= gen
                if chance < 0:
                    index = i
                    break

            if not index:
                if len(self.memory_enemy):
                    if (self.position[0], self.position[1] - 20)\
                            not in self.memory_enemy:
                        self.position[1] -= 20
                    else:
                        self.__move_rules(width, height, objects_positions,
                                          start)
                else:
                    self.position[1] -= 20

            elif index == 1:
                if len(self.memory_enemy):
                    if (self.position[0], self.position[1] + 20)\
                            not in self.memory_enemy:
                        self.position[1] += 20
                    else:
                        self.__move_rules(width, height, objects_positions,
                                          start)
                else:
                    self.position[1] += 20

            elif index == 2:
                if len(self.memory_enemy):
                    if (self.position[0] - 20, self.position[1])\
                            not in self.memory_enemy:
                        self.position[0] -= 20
                    else:
                        self.__move_rules(width, height, objects_positions,
                                          start)
                else:
                    self.position[0] -= 20

            elif index == 3:
                if len(self.memory_enemy):
                    if (self.position[0] + 20, self.position[1])\
                            not in self.memory_enemy:
                        self.position[0] += 20
                    else:
                        self.__move_rules(width, height, objects_positions,
                                          start)
                else:
                    self.position[0] += 20

    def __die(self, age=40):
        """Функция отвечает за смерть клетки от старости
        """
        if self.age > age:
            self.delete = True
            self.colour = RED

    def move(self, width, height, objects_positions, meat_positions,
             food_positions, cell_positions,  age):
        """Функция отвечает за передвижение клетки, когда есть еда. Когда
        клетка не видит еду, вызывается функция __move_rules()
        """
        old_position = [self.position[0], self.position[1]]

        self.__die(age)
        self.__movement = 0
        self.age += 1
        self.__inspect(width, height, meat_positions, food_positions,
                       cell_positions)

        if not self.delete:
            if len(self.memory):
                self.memory.sort(key=lambda x: (x[0], x[1], x[2]))
                if self.memory[0][1] == '1':
                    if abs(self.memory[0][2] - self.position[0])\
                            > abs(self.memory[0][3] - self.position[1]):
                        if len(self.memory_enemy):
                            if (self.position[0] + 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] += 20
                            elif (self.position[0], self.position[1] - 20)\
                                    not in self.memory_enemy:
                                self.position[1] -= 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[0] += 20
                    else:
                        if len(self.memory_enemy):
                            if (self.position[0], self.position[1] - 20)\
                                    not in self.memory_enemy:
                                self.position[1] -= 20
                            elif (self.position[0] + 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] += 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[1] -= 20

                elif self.memory[0][1] == '2':
                    if abs(self.memory[0][2] - self.position[0])\
                            > abs(self.memory[0][3] - self.position[1]):
                        if len(self.memory_enemy):
                            if (self.position[0] - 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] -= 20
                            elif (self.position[0], self.position[1] - 20)\
                                    not in self.memory_enemy:
                                self.position[1] -= 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[0] -= 20
                    else:
                        if len(self.memory_enemy):
                            if (self.position[0], self.position[1] - 20)\
                                    not in self.memory_enemy:
                                self.position[1] -= 20
                            elif (self.position[0] - 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] -= 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[1] -= 20

                elif self.memory[0][1] == '3':
                    if abs(self.memory[0][2] - self.position[0])\
                            > abs(self.memory[0][3] - self.position[1]):
                        if len(self.memory_enemy):
                            if (self.position[0] - 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] -= 20
                            elif (self.position[0], self.position[1] + 20)\
                                    not in self.memory_enemy:
                                self.position[1] += 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[0] -= 20
                    else:
                        if len(self.memory_enemy):
                            if (self.position[0], self.position[1] + 20)\
                                    not in self.memory_enemy:
                                self.position[1] += 20
                            elif (self.position[0] - 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] -= 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[1] += 20

                elif self.memory[0][1] == '4':
                    if abs(self.memory[0][2] - self.position[0])\
                            > abs(self.memory[0][3] - self.position[1]):
                        if len(self.memory_enemy):
                            if (self.position[0] + 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] += 20
                            elif (self.position[0], self.position[1] + 20)\
                                    not in self.memory_enemy:
                                self.position[1] += 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[0] += 20
                    else:
                        if len(self.memory_enemy):
                            if (self.position[0], self.position[1] + 20)\
                                    not in self.memory_enemy:
                                self.position[1] += 20
                            elif (self.position[0] + 20, self.position[1])\
                                    not in self.memory_enemy:
                                self.position[0] += 20
                            else:
                                self.__move_rules(width, height,
                                                  objects_positions)
                        else:
                            self.position[1] += 20

                if not self.genome[2]:
                    if [self.memory[0][2], self.memory[0][3]] == self.position:
                        self.energy += Food.energy
                else:
                    if [self.memory[0][2], self.memory[0][3]] == self.position:
                        self.energy += Meat.energy
            else:
                self.__move_rules(width, height, objects_positions)

            self.position[0], self.position[1] =\
                exit_border(self.position[0], self.position[1], width, height)

            if not old_position == self.position:
                objects_positions.remove(old_position)
                objects_positions.append([self.position[0], self.position[1]])
                cell_positions.remove(old_position)
                cell_positions.append([self.position[0], self.position[1]])

            self.energy -= 5
            self.check_energy()

    def check_energy(self):
        """Функция отвечает за смерть клетки от иссякания энергии
        """
        if self.energy <= 0:
            self.delete = True
            self.colour = RED

    def __mutation(self):
        """Функция, отвечающая за мутацию клетки

            С шансом 45% происходит мутация радиуса обзора
            С шансом 45% происходит мутация шансов выбора направления движения
            С шансом 10% происходит мутация гена, отвечающего за мясоедство
        """
        index = randint(0, 100)
        mut = 0
        if 0 <= index <= 45:
            while self.genome[0] < 0 or not mut:
                mut = randint(-1 * 2, 2)
                if self.genome[0] + mut > 0:
                    self.genome[0] += mut
                else:
                    mut = 0
        if 46 <= index <= 90:
            list_index = list(range(0, 4))
            index = randint(0, 3)
            old_value = self.genome[1][index]
            mut = randint(-1 * self.genome[1][index], self.genome[1][index])
            self.genome[1][index] += mut
            list_index.remove(index)
            while mut > 0 and len(list_index):
                index = choice(list_index)
                mut = randint(0, old_value)
                old_value -= mut
                self.genome[1][index] += mut
            if mut > 0:
                for index in range(0, 3):
                    self.genome[1][index] += mut // 4
        else:
            self.genome[2] = 1

    def division(self, width, height, root):
        """Функция, отвечающая за деление клетки

            Если нет места для деления клтеки, то клетка не будет делиться

            С шансом 5% может произойти мутация у новой клетки
        """
        start = False
        x = self.position[0] - 20
        y = self.position[1]

        x, y = exit_border(x, y, width, height)

        if root.get_at((x, y)) == WHITE:
            start = True

        x = self.position[0] + 20
        y = self.position[1]

        x, y = exit_border(x, y, width, height)

        if root.get_at((x, y)) == WHITE:
            start = True

        x = self.position[0]
        y = self.position[1] - 20

        x, y = exit_border(x, y, width, height)

        if root.get_at((x, y)) == WHITE:
            start = True

        x = self.position[0]
        y = self.position[1] + 20

        x, y = exit_border(x, y, width, height)

        if root.get_at((x, y)) == WHITE:
            start = True

        if self.energy > 800 and start:
            index = randint(0, 100)
            new_cells = []
            self.delete = True
            self.colour = RED
            flag = True
            for i in range(2):
                if flag and index < 5:
                    cell = Bacteria(width, height, self, root)
                    cell.__mutation()
                    flag = False
                else:
                    cell = Bacteria(width, height, self, root)
                if len(cell.position):
                    new_cells.append(cell)
            return new_cells
        else:
            return []
