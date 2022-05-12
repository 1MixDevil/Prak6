import asyncio
import os
import random
import signal
import platform
import sys
import time
import Charts

n = int(input("Введите желаемое кол-во поездов (рекомендуемое - 5) \n"))
if n <= 0:
    print("Metro is being constructed")
else:
    time_start = time.time()
    speed = 100
    clear = lambda: os.system('cls.clear') if "Windows" in platform.platform() else os.system('clear')
    helper = [1, 6, 1, 3, 1, 2, 1, 7, 1]


    class Visual:
        def __init__(self):
            self.train_count = n
            self.station_count = 5
            self.line = [[[" "] for j in range((self.station_count * 2)-1)] for i in range(self.train_count)]
            for i in range(0, self.train_count):
                for j in range(1, len(self.line[i]), 2):
                    self.line[i][j] = [[" "]] * helper[j]
            for i in range(0, self.train_count):
                self.line[i][0] = ["T"]

        def print_line(self):
            print("  R ,  ,  ,  ,  ,  ,  ,S ,  ,  ,  ,C ,  ,  ,D ,  ,  ,  ,  ,  ,  ,  ,L")
            i = 0
            for j in self.line:
                i += 1
                print(str(i), end = ": ")
                print(str(j).replace("[", "").replace("]", "").replace("'", ""))


    visual = Visual()


    class Station_Metro:
        MAX_PEOPLE = 400

        def __init__(self, name, left=0, right=0, number=0):
            self.name = name
            self.right = right
            self.left = left
            self.people_r = []
            self.people_l = []
            self.time = 0
            self.number = number

        async def stat_info(self):
            while True:
                self.time += 1
                Charts.passengers.append((len(self.people_r) + len(self.people_l), self.time))
                await asyncio.sleep(1)

        async def add_people(self):
            k = 0
            while True:
                if k == 100:
                    k = 0
                    Charts.Update()
                k += 1
                await asyncio.sleep(1 / speed)
                pers = Person(self.number)

                pers.get_time()
                if pers.right:
                    self.people_r.append(pers)
                else:
                    self.people_l.append(pers)

        def del_people_r(self, has_people, num):
            free = (self.MAX_PEOPLE - len(has_people))  # Получение свободных мест в поезде
            platform_free = len(self.people_r) - free  # Сколько людей останется на платформе, если заполнить все места
            if platform_free <= 0:
                people = list(self.people_r)
                self.people_r = []
                c = []
                for i in people:
                    c.append(i.finish)
                return c

            else:
                c = []
                for i in range(free):
                    c.append(self.people_r.pop().finish)
                return c

        def del_people_l(self, has_people, num):
            free = (self.MAX_PEOPLE - len(has_people))  # Получение свободных мест в поезде
            platform_free = len(self.people_l) - free  # Сколько людей останется на платформе, если заполнить все места
            if platform_free <= 0:
                people = list(self.people_l)
                self.people_l = []
                c = []
                for i in people:
                    c.append(i.finish)
                return c

            else:
                c = []
                for i in range(free):
                    c.append(self.people_l.pop().finish)
                return c


    class Person:
        def __init__(self, number):
            self.start = number
            self.finish = random.randint(0, 3)
            self.right = True

            if self.start == self.finish:
                self.finish = 4
            if self.finish < self.start:
                self.right = False

        def get_time(self):
            tim = 0
            if self.right:
                for i in range(self.start, self.finish + 1):
                    tim += 15
                    tim += int(stations[i].right * speed)
                Charts.passengers_time.append(tim)

            else:
                for i in range(self.finish, self.start + 1):
                    tim += 15
                    tim += int(stations[i].left * speed)
                Charts.passengers_time.append(tim)


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
            self.passengers = []
            self.right = right
            self.people = []
            self.number = number
            self.position = position
            self.standing = True
            self.time = 0
            self.position_metro = 0

        async def stat_info(self):
            while True:
                self.time += 1
                Charts.passengers_inside.append((len(self.people), self.time))
                await asyncio.sleep(1)

        def del_people(self):
            while self.position in self.people:
                self.people.remove(self.position)

        # print(f"Из поезда {self.number} вышли {del_pep}")

        async def directions(self):
            while True:
                if self.position >= len(stations) - 1:
                    self.right = False
                elif self.position <= 0:
                    self.right = True

                if self.right:
                    # print(f"Поезд {self.number} уехал со станции {stations[self.position].name}")
                    visual.line[self.number-1][self.position_metro] = [" "]
                    self.position_metro += 1
                    for i in range(0, len(visual.line[self.number - 1][self.position_metro])):
                        visual.line[self.number - 1][self.position_metro][i] = ["T"]
                        await asyncio.sleep(stations[self.position].right / len(visual.line[self.number - 1][self.position_metro]))
                        visual.line[self.number - 1][self.position_metro][i] = [" "]
                    self.position_metro += 1
                    self.position += 1
                    visual.line[self.number-1][self.position_metro] = ["T"]
                    # print(f"Поезд {self.number} прибыл на станцию {stations[self.position].name} \n \n")
                    self.del_people()
                    if self.position >= len(stations) - 1:
                        self.people += stations[self.position].del_people_l(self.people, self.number)
                    else:
                        self.people += stations[self.position].del_people_r(self.people, self.number)

                elif not self.right:
                    visual.line[self.number-1][self.position_metro] = [" "]
                    self.position_metro -= 1
                    for i in range(len(visual.line[self.number - 1][self.position_metro])-1, -1, -1):
                        visual.line[self.number - 1][self.position_metro][i] = ["T"]
                        await asyncio.sleep(stations[self.position].left / len(visual.line[self.number - 1][self.position_metro]))
                        visual.line[self.number - 1][self.position_metro][i] = [" "]
                    # visual.line[self.number-1][self.position_metro] = ["T"]
                    # # print(f"Поезд {self.number} уехал со станции {stations[self.position].name}")
                    # await asyncio.sleep(stations[self.position].left)
                    # visual.line[self.number-1][self.position_metro] = [" "]
                    self.position -= 1
                    self.position_metro -= 1
                    visual.line[self.number-1][self.position_metro] = ["T"]
                    # print(f"Поезд {self.number} прибыл на станцию {stations[self.position].name} \n \n")
                    self.del_people()
                    if self.position <= 0:
                        self.people += stations[self.position].del_people_r(self.people, self.number)
                    else:
                        self.people += stations[self.position].del_people_l(self.people, self.number)

                await asyncio.sleep(15 / speed)


    def signal_handler(signum, frame):
        Charts.Time_Passengers()
        Charts.Passengers_train_chart()
        Charts.Passengers_chart()
        sys.exit
        os.abort()


    async def Main():
        trains = []
        for i in range(n):
            a = Train(i + 1, 0, 1)
            trains.append(a)
            loop.create_task(a.directions())
            loop.create_task(a.stat_info())
            if i == 0:
                loop.create_task(start())
            await asyncio.sleep((2280 / speed) / n)

        while True:
            clear()
            print(f"Real time: {int(time.time() - time_start)} sec")
            print(f"Project time: {int((time.time() - time_start) * speed)} sec")
            print()
            for i in stations:
                print(f"{i.name}: {len(i.people_r) + len(i.people_l)}")

            print()
            for i in trains:
                if i.right:
                    if i.position >= len(stations)-1:
                        print(
                            f"{i.number}: {stations[i.position].name} -> {stations[i.position - 1].name}"
                        )
                    else:
                        print(
                            f"{i.number}: {stations[i.position].name} -> {stations[i.position+1].name}"
                        )
                else:
                    if i.position <= 0:
                        print(
                            f"{i.number}: {stations[i.position].name} -> {stations[i.position + 1].name}"
                        )
                    else:
                        print(
                            f"{i.number}: {stations[i.position].name} -> {stations[i.position-1].name}"
                        )

            print()
            visual.print_line()
            await asyncio.sleep(0.1)
            print("\n")


    async def start():
        clear()
        print("LOADING...")
        print()
        visual.print_line()
        await asyncio.sleep(1080 / speed)
        for i in range(0, len(stations)):
            loop.create_task(stations[i].add_people())
        await asyncio.sleep(1)
        for i in range(0, len(stations)):
            loop.create_task(stations[i].stat_info())


    stations = [
        Station_Metro('Rokossovskoy', 0, 360 / speed, 0),
        Station_Metro("Sobornaya", 360 / speed, 180 / speed, 1),
        Station_Metro("Crystal", 180 / speed, 120 / speed, 2),
        Station_Metro("Dyrochnaya", 120 / speed, 420 / speed, 3),
        Station_Metro("Lib_Push", 420 / speed, 0, 4),
    ]

    signal.signal(signal.SIGINT, signal_handler)
    loop = asyncio.get_event_loop()
    loop.create_task(Main())
    loop.run_forever()