from actor import *
from attributes import *


class Pawn(Actor):
    name = "New Pawn"

    def tick(self):
        if self.isDead:
            return

        # action to take during this tick
        super(Pawn, self).tick()
        self.controller.query(self)

    def auto_attack(self):
        if ("aa_cooldown" in self.status.meta) or ("aa_prepare" in self.status.meta):
            return
        else:
            self.status.meta["aa_prepare"] = AutoAttackPrepare(owner=self)
            print(self.name + " auto attack " + self.target.name)


class AutoAttackPrepare(Status):
    def __init__(self, name="aa_prepare", duration=700, owner=None):
        super().__init__(name=name, duration=duration, owner=owner)

    def on_end_action(self):
        self.owner.status.meta["aa_cooldown"] = AutoAttack(owner=self.owner)


class AutoAttack(Status):
    def __init__(self, name="aa_cooldown", duration=1800, owner=None):
        super().__init__(name=name, duration=duration, owner=owner)

    def on_begin_action(self):
        self.owner.world.objects["Inspector1"].apply_physical_damage(40, self.owner, self.owner.target)
