from random import randint


class Food(object):
    """Класс Food используется для создания экземпляра еды

    Attributes
    ----------
    position : list
         хранит в себе информацию о позиции еды на поле (x, y)
    """
    energy = 150  # Количество энергии, которая даст клетке при съедании

    def __init__(self, width, height):
        self.position = [randint(0, width // 20 - 1) * 20 + 1,
                         randint(0, height // 20 - 1) * 20 + 1]
