import matplotlib.pyplot as plt
import pylab


def draw_grafic(cells, foods, steps, history_gen_vision, generations, x_num):
    """Функция, строящая графики в конце симуляции
    """
    pylab.subplot(2, 3, 1)
    plt.plot(steps, cells, c='red')
    pylab.title("Cells/steps")
    pylab.subplot(2, 3, 2)
    plt.plot(steps, foods, c='green')
    pylab.title("Foods/steps")
    pylab.subplot(2, 3, 3)
    number = []
    for item in set(history_gen_vision):
        number.append(history_gen_vision.count(item))
    plt.bar(list(set(history_gen_vision)), number)
    pylab.title("Gen vision/ numbers")
    pylab.subplot(2, 3, 4)
    plt.plot(steps, generations, c='blue')
    pylab.title("Generations/steps")
    pylab.subplot(2, 3, 5)
    plt.plot(steps, x_num, c='red')
    pylab.title("eat meet (%)/steps")
    pylab.show()
    pylab.pause(1000000000)
