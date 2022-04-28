import asyncio
import random
import signal
import Charts

n = 5


class Station_Metro:
    MAX_PEOPLE = 400

    def __init__(self, name, left=0, right=0, ):
        self.name = name
        self.right = right
        self.left = left
        self.people_r = 0
        self.people_l = 0
        self.time = 0

    async def stat_info(self):
        while True:
            self.time += 1
            Charts.passengers.append((self.people_r + self.people_l, self.time))
            await asyncio.sleep(1)

    async def add_people(self):
        while True:
            await asyncio.sleep(0.01)
            rand_people = random.randint(0, 1)
            if self.right == 0:
                self.people_l += rand_people
            elif self.left == 0:
                self.people_r += rand_people
            else:
                self.people_r += rand_people
                self.people_l += (1 - rand_people)

    def del_people_r(self, has_people, num):
        free = (self.MAX_PEOPLE - has_people)  # Получение свободных мест в поезде
        platform_free = self.people_r - free  # Сколько людей останется на платформе, если заполнить все места
        if platform_free <= 0:
            people = int(self.people_r)
            self.people_r = 0
            # print(f"Поезд {num} забрал {people} людей (ВСЕХ)")
            return people
        else:
            # print(f"Поезд {num} забрал {free} людей")
            self.people_r -= free
            return free

    def del_people_l(self, has_people, num):
        # print(f"На станции {self.name} стоит {self.people_r} которые хотят направо и {self.people_l} налево")
        free = self.MAX_PEOPLE - has_people
        if free < 0:
            return 0
        platform_free = self.people_l - free
        if platform_free <= 0:
            people = int(self.people_l)
            self.people_l = 0
            # print(f"Поезд {num} забрал {people} людей (ВСЕХ)")
            return people
        else:
            # print(f"Поезд {num} забрал {free} людей")
            self.people_l -= free
            return free


class Train:
    dictionary = {
        True: 1,
        False: 2,
    }
    Carriage = 4
    Capacity = 50
    max_people = Capacity * Carriage
    Count_station = 4

    def __init__(self, number, position, right=True):
        self.right = right
        self.people = 0
        self.number = number
        self.position = position
        self.standing = True
        self.time = 0

    async def stat_info(self):
        while True:
            self.time += 1
            Charts.passengers_inside.append((self.people, self.time))
            await asyncio.sleep(1)

    def del_people(self):
        del_pep = random.randint(0, self.people)
        self.people -= del_pep
        # print(f"Из поезда {self.number} вышли {del_pep}")

    async def directions(self):
        while True:
            if self.position >= len(stations) - 1:
                self.right = False
            elif self.position <= 0:
                self.right = True

            if self.right:
                # print(f"Поезд {self.number} уехал со станции {stations[self.position].name}")
                await asyncio.sleep(stations[self.position].right)
                self.position += 1
                # print(f"Поезд {self.number} прибыл на станцию {stations[self.position].name} \n \n")
                self.del_people()
                self.people += stations[self.position].del_people_r(self.people, self.number)
                if self.position >= len(stations) - 1:
                    self.people += stations[self.position].del_people_l(self.people, self.number)
                else:
                    self.people += stations[self.position].del_people_r(self.people, self.number)

            elif not self.right:
                # print(f"Поезд {self.number} уехал со станции {stations[self.position].name}")
                await asyncio.sleep(stations[self.position].left)
                self.position -= 1
                # print(f"Поезд {self.number} прибыл на станцию {stations[self.position].name} \n \n")
                self.del_people()
                if self.position <= 0:
                    self.people += stations[self.position].del_people_r(self.people, self.number)
                else:
                    self.people += stations[self.position].del_people_l(self.people, self.number)

            await asyncio.sleep(0.15)


def signal_handler(signum, frame):
    Charts.Passengers_train_chart()
    Charts.Passengers_chart()


async def Main():
    trains = []
    for i in range(n):
        a = Train(i + 1, 0, 1)
        trains.append(a)
        loop.create_task(a.directions())
        loop.create_task(a.stat_info())
        if i == 0:
            loop.create_task(start())
        await asyncio.sleep(22.8 / n)

    while True:
        for i in stations:
            print(f"{i.name}: {int(i.people_r) + int(i.people_l)}")

        print(f"\n \n")
        for i in trains:
            try:
                print(
                    f"{i.number}: {stations[i.position].name} -> {stations[i.position + 1].name if i.right else stations[i.position - 1].name}      {i.people}")
            except():
                print(
                    f"{i.number}: {stations[i.position].name} -> {stations[i.position - 1].name if i.right else stations[i.position + 1].name}      {i.people}")
        await asyncio.sleep(10)
        print("\n")


async def start():
    await asyncio.sleep(10.8)
    for i in range(0, len(stations)):
        loop.create_task(stations[i].add_people())
    await asyncio.sleep(1)
    for i in range(0, len(stations)):
        loop.create_task(stations[i].stat_info())



stations = [
    Station_Metro('Rokossovskoy', 0, 3.6),
    Station_Metro("Sobornaya", 3.6, 1.8),
    Station_Metro("Crystal", 1.8, 1.2),
    Station_Metro("Dyrochnaya", 1.2, 4.2),
    Station_Metro("Lib_Push", 4.2, 0),
]

signal.signal(signal.SIGINT, signal_handler)
loop = asyncio.get_event_loop()
loop.create_task(Main())
loop.run_forever()
