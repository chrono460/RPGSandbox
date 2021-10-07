from object import *
from alliance import *
from environment import *


class Player(Object):
    name = "New Player"
    alliance = ""
    world = None

    def __init__(self, world=None, name="", alliance=""):
        self.name = name
        self.alliance = alliance
        self.world = world

        if world:
            world.add_player(self)


class World(Object):
    name = "New World"
    env = EnvironmentQuery()

    time = 0  # ms
    players = {}
    objects = {}

    def __init__(self):
        super(World, self).__init__()

    def add_player(self, player):
        if player in self.players:
            return
        else:
            self.players[player.name] = player
            print(player.name + " is added into world.")

    def add_object(self, obj):
        index = 1

        while True:
            name = obj.name + str(index)
            if name in self.objects:
                index += 1
                continue
            else:
                obj.name = name
                self.objects[name] = obj
                print(name + " is added into world.")
                break

    def tick(self):
        for _, obj in self.objects.items():
            obj.tick()
        self.time += 1

    def tick1000(self):
        for _ in range(1000):
            self.tick()

        print(self.get_timelabel())

    def tickN(self, n):
        for _ in range(n):
            self.tick()

        print(self.get_timelabel())

    def get_datetime(self):
        hh = np.floor(self.time / 1000 / 3600)
        mm = np.floor(self.time / 1000 / 60) - hh * 60
        ss = self.time / 1000 - hh * 3600 - mm * 60
        return int(hh), int(mm), ss

    def get_timelabel(self):
        hh, mm, ss = self.get_datetime()
        return str(hh) + ":" + str(mm) + ":" + str(ss) + " "
