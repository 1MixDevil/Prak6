

import asyncio
import time
import random


class Station_Metro:
    MAX_PEOPLE = 200

    def __init__(self, name, left=0, right=0, ):
        self.name = name
        self.right = right
        self.left = left
        self.people_r = 0
        self.people_l = 0

    async def add_people(self):
        while True:
            # print(f"На станции {self.name} {self.people} людей")
            await asyncio.sleep(4)
            rand_people = random.randint(1, 50)
            self.people += rand_people
            self.people_l += (50 - rand_people)

    def del_people(self, has_already):
        print(f"Поезд стоит на станции {self.name}")
        add_max = self.MAX_PEOPLE - has_already
        max = self.people - add_max
        if max < 0:
            self.people = 0
            return max
        else:
            self.people -= max
            return max


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

    async def directions(self):
        while True:
            if self.position >= len(stations) - 1:
                self.right = False
            elif self.position <= 0:
                self.right = True

            if self.right:
                print(f"Поезд {self.number} уехал со станции {stations[self.position].name}")
                await asyncio.sleep(stations[self.position].right)
                print(f"Поезд {self.number} прибыл на станцию {stations[self.position + 1].name}")
                self.position += 1
            elif not self.right:
                f"Поезд {self.number} уехал со станции {stations[self.position].name}"
                await asyncio.sleep(stations[self.position].left)
                print(f"Поезд {self.number} прибыл на станцию {stations[self.position - 1].name}")
                self.position -= 1
            await asyncio.sleep(5)


async def Main():
    for i in range(2):
        loop.create_task(Train(i, 0, 1).directions())
        await asyncio.sleep(4)
    for i in range(0, len(stations)):
        loop.create_task(stations[i].add_people())

    while True:
        await asyncio.sleep(4)


stations = [
    Station_Metro('Rokossovskoy', 0, 6),
    Station_Metro("Sobornaya", 6, 3),
    Station_Metro("Crystal", 3, 2),
    Station_Metro("Dyrochnaya", 2, 7),
    Station_Metro("Lib_Push", 7, 0),
]

loop = asyncio.get_event_loop()
loop.create_task(Main())
loop.run_forever()