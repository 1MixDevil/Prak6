import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

passengers = []
passengers_inside = []
passengers_time = []
time_x = []
time_y = []
grid = GridSpec(3, 1,
            left=0.1, right=0.99, bottom=0.1, top=0.9, height_ratios=[1, 1, 1])


def Passengers_chart():
    x = []
    y = []
    c = []
    for i in passengers:
        if i[1] not in y:
            y.append(i[1])
            x.append(i[0])
            c.append(1)
        else:
            c[i[1] - 1] += 1
            x[i[1] - 1] += i[0]
    for i in range(len(c)):
        x[i] = x[i] // c[i]
    plt.subplot(grid[0])
    plt.plot(y, x)
    plt.title("Кол-во людей на платформе")
    plt.show()


def Update():
    time_x.append(float(sum(passengers_time) / len(passengers_time)))
    time_y.append(len(passengers_time))


def Time_Passengers():
    plt.subplot(grid[2])
    plt.plot(time_y, time_x)
    plt.title("Среднее время поездки")


def Passengers_train_chart():
    x = []
    y = []
    c = []
    for i in passengers_inside:
        if i[1] not in y:
            y.append(i[1])
            x.append(i[0])
            c.append(1)
        else:
            c[i[1] - 1] += 1
            x[i[1] - 1] += i[0]
    for i in range(len(c)):
        x[i] = x[i] // c[i]
    plt.subplot(grid[1])
    plt.plot(y, x)
    plt.title("Кол-во людей в поезде")



