from random import randint


class Meat(object):
    """Класс Meat используется для создания экземпляра мяса

    Attributes
    ----------
    position : list
         хранит в себе информации о позиции мяса на поле (x, y)
    """
    energy = 300  # Количество энергии, которая даст клетке при съедании

    def __init__(self, width=None, height=None, position=None):
        if position is not None:
            self.position = [position[0], position[1]]
        else:
            self.position = [randint(0, width // 20 - 1) * 20 + 1,
                             randint(0, height // 20 - 1) * 20 + 1]
