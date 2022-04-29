import matplotlib.pyplot as plt

passengers = []
passengers_inside = []
passengers_time = []
time_x = []
time_y = []


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
    plt.title("Кол-во людей на платформе")
    plt.xlabel("Секунды")
    plt.ylabel("Кол-во")
    plt.plot(y, x)
    plt.show()


def Update():
    time_x.append(float(sum(passengers_time) / len(passengers_time)))
    time_y.append(len(passengers_time))


def Time_Passengers():
    plt.title("Среднее время в поездке")
    plt.xlabel("Пассажиров всего")
    plt.ylabel("Кол-во")
    plt.plot(time_y, time_x)
    plt.show()


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
    plt.title("Кол-во людей в поезде")
    plt.xlabel("Секунды")
    plt.ylabel("Кол-во")
    plt.plot(y, x)
    plt.show()


