from random import seed
from random import random
import numpy as np

seed(77777)


# 定义各项属性
class Attributes(object):
    MaxHealth = 100
    MaxMana = 0
    Attack = 0
    Magic = 0
    PhysicalDefence = 0
    MagicalDefence = 0
    AttackSpeed = 0
    CriticalChance = 0
    CriticalRate = 0.5
    PhysicalPenetration = 0
    MagicalPenetration = 0
    Avoidance = 0
    Accuracy = 1.0

    @staticmethod
    def get_length():
        return 13

    def __init__(self, *args, **kwargs):
        if len(args) == self.get_length():
            self.MaxHealth = args[0]
            self.MaxMana = args[1]
            self.Attack = args[2]
            self.Magic = args[3]
            self.PhysicalDefence = args[4]
            self.MagicalDefence = args[5]
            self.AttackSpeed = args[6]
            self.CriticalChance = args[7]
            self.CriticalRate = args[8]
            self.PhysicalPenetration = args[9]
            self.MagicalPenetration = args[10]
            self.Avoidance = args[11]
            self.Accuracy = args[12]


class StatusEffects(object):
    Modified = False
    meta = {}

    def tick(self):
        pass

    def get_multipliers(self):
        a, b, c, d = np.array([1] * 2), np.array([1] * 2), np.array([1] * 2), np.array([1.0] * Attributes.get_length())
        for s in self.meta:
            s.action()
            a *= s.damage_multiplier
            b *= s.defence_multiplier
            c *= s.heal_multiplier
            d *= s.attrMultiplier
        return a, b, c, Attributes(*d)


class Alliance(object):
    meta = {
        "Team1": [1, -1, 0],
        "Team2": [-1, 1, 0],
        "Neutral": [0, 0, 0]
    }


class Controller:
    owner = []
    alliance = "Neutral"

    def tick(self):
        pass


class Object:
    name = "New Object"

    def tick(self):
        pass


class Actor(Object):
    name = "New Actor"
    owner = Controller()
    attr = Attributes()
    status = StatusEffects()

    health = attr.MaxHealth
    mana = 0
    isDead = False

    def receive_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.health = 0
            self.death()

    def receive_heal(self, heal):
        self.health += heal
        if self.health > self.attr.MaxHealth:
            self.health = self.attr.MaxHealth

    def death(self):
        self.isDead = True
        print(self.name + " is dead.")


class Status(Object):
    MaxTime = 0
    damage_multiplier = np.array([1] * 2)  # 物理/魔法
    defence_multiplier = np.array([1] * 2)  # 物理/魔法
    heal_multiplier = np.array([1] * 2)  # 治疗/被治疗
    attrMultiplier = np.array([1.0] * Attributes.get_length())
    owner = Actor()

    def action(self):
        # any modification to self happens here
        pass


class World:
    time = 0  # ms
    players = {}
    objects = {}

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
                print(name+" is added into world.")
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


class Inspector(Object):
    world = World()
    name = "New Inspector"

    def apply_physical_damage(self, factor, sender, receiver):
        if receiver.isDead:
            return

        # 读取属性和状态
        attr1 = sender.attr
        d1, _, _, a1 = sender.status.get_multipliers()
        attr2 = receiver.attr
        _, f2, _, a2 = receiver.status.get_multipliers()

        d1 = d1[0]
        f2 = f2[0]

        # 命中判定
        chance = attr1.Accuracy * a1.Accuracy - attr2.Avoidance * a2.Avoidance
        if random() > chance:
            print("Avoid!")
            return

        # 暴击判定
        chance = attr1.CriticalChance * a1.CriticalChance
        is_critical_hit = random() < (attr1.CriticalChance * a1.CriticalChance)

        # 伤害计算 = 基础伤害 * 基础伤害系数1（由属性得出）* 状态系数1（由buff/debuff计算）* 暴击伤害系数1
        # * 基础减伤系数2 * 状态系数2

        damage = factor * (1.0 + attr1.Attack / 100.0) * d1 * (1.0 + is_critical_hit * attr1.CriticalRate) \
                 * (1.0 - attr2.PhysicalDefence / 100.0) * f2
        damage = np.floor(damage)

        assert damage >= 0, "Damage should be non-negative"

        if is_critical_hit:
            print(self.world.get_timelabel() + sender.name + " deals " + str(damage) + "! physical damage to " + receiver.name)
        else:
            print(self.world.get_timelabel() + sender.name + " deals " + str(damage) + " physical damage to " + receiver.name)

        receiver.receive_damage(damage)

    def apply_magic_damage(self, factor, sender, receiver):
        if receiver.isDead:
            return

        # 读取属性和状态
        attr1 = sender.attr
        d1, _, _, a1 = sender.status.get_multipliers()
        attr2 = receiver.attr
        _, f2, _, a2 = receiver.status.get_multipliers()

        d1 = d1[1]
        f2 = f2[1]

        # 命中判定
        chance = attr1.Accuracy * a1.Accuracy - attr2.Avoidance * a2.Avoidance
        if random() > chance:
            print("Avoid!")
            return

        # 暴击判定
        chance = attr1.CriticalChance * a1.CriticalChance
        is_critical_hit = random() < (attr1.CriticalChance * a1.CriticalChance)

        # 伤害计算 = 基础伤害 * 基础伤害系数1（由属性得出）* 状态系数1（由buff/debuff计算）* 暴击伤害系数1
        # * 基础减伤系数2 * 状态系数2

        damage = factor * (1.0 + attr1.Magic / 100.0) * d1 * (1.0 + is_critical_hit * attr1.CriticalRate) \
                 * (1.0 - attr2.MagicalDefence / 100.0) * f2
        damage = np.floor(damage)

        assert damage >= 0, "Damage should be non-negative"

        if is_critical_hit:
            print(self.world.get_timelabel() + sender.name + " deals " + str(damage) + "! magic damage to " + receiver.name)
        else:
            print(self.world.get_timelabel() + sender.name + " deals " + str(damage) + " magic damage to " + receiver.name)

        receiver.receive_damage(damage)

    def apply_heal(self, factor, sender, receiver):
        if receiver.isDead:
            return

        # 读取属性和状态
        attr1 = sender.attr
        _, _, h1, a1 = sender.status.get_multipliers()
        _, _, h2, a2 = receiver.status.get_multipliers()
        h12 = h1[0] * h2[1]

        # 暴击判定
        chance = attr1.CriticalChance * a1.CriticalChance
        is_critical_hit = random() < (attr1.CriticalChance * a1.CriticalChance)

        # 治疗计算 = 基础治疗数字 * 基础治疗系数1（由属性得出）* 状态系数1（由buff/debuff计算 * 状态系数2 * 暴击系数1
        heal = factor * (1.0 + attr1.Magic / 100.0) * h12 * (1.0 + is_critical_hit * attr1.CriticalRate)
        heal = np.floor(heal)

        assert heal >= 0, "Heal should be non-negative"

        if is_critical_hit:
            print(self.world.get_timelabel() + sender.name + " deals " + str(heal) + "! healing to " + receiver.name)
        else:
            print(self.world.get_timelabel() + sender.name + " deals " + str(heal) + " healing to " + receiver.name)

        receiver.receive_heal(heal)
