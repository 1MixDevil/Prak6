import matplotlib.pyplot as plt

passengers = []
passengers_inside = []


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


