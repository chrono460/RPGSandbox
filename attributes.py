from world import *


# 定义各项属性
class Attributes(Object):
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


class StatusEffects(Object):
    Modified = False
    meta = None

    def __init__(self):
        self.meta = {}

    def tick(self):
        to_remove = []
        for s, v in list(self.meta.items()):
            if v.duration < 1:
                to_remove.append(s)
            else:
                v.tick()
        [self.meta.pop(s, None) for s in tuple(to_remove)]

    def get_multipliers(self):
        a, b, c, d = np.array([1] * 2), np.array([1] * 2), np.array([1] * 2), np.array([1.0] * Attributes.get_length())
        for _, v in self.meta.items():
            a *= v.damage_multiplier
            b *= v.defence_multiplier
            c *= v.heal_multiplier
            d *= v.attrMultiplier
        return a, b, c, Attributes(*d)


class Status(Object):
    name = "new status"
    duration = 0
    owner = None
    damage_multiplier = np.array([1] * 2)  # 物理/魔法
    defence_multiplier = np.array([1] * 2)  # 物理/魔法
    heal_multiplier = np.array([1] * 2)  # 治疗/被治疗
    attrMultiplier = np.array([1.0] * Attributes.get_length())

    def __init__(self, name="new status", duration=0, owner=None):
        self.name = name
        self.duration = duration
        self.owner = owner
        self.on_begin_action()

    def tick(self):
        self.duration -= 1

        if self.duration < 1:
            return
        if self.duration > 1:
            self.action()
        else:
            self.on_end_action()

    def action(self):
        # any modification to self happens here
        pass

    def on_begin_action(self):
        pass

    def on_end_action(self):
        pass


class Inspector(Object):
    world = None
    name = "Inspector"

    def __init__(self, world=None):
        self.world = world

        if world:
            world.add_object(self)

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
            print(self.world.get_timelabel() + sender.name + " deals " + str(
                damage) + "! physical damage to " + receiver.name)
        else:
            print(self.world.get_timelabel() + sender.name + " deals " + str(
                damage) + " physical damage to " + receiver.name)

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
            print(self.world.get_timelabel() + sender.name + " deals " + str(
                damage) + "! magic damage to " + receiver.name)
        else:
            print(self.world.get_timelabel() + sender.name + " deals " + str(
                damage) + " magic damage to " + receiver.name)

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
