from object import *
from controller import *
from attributes import *


class Actor(Object):
    name = "New Actor"
    world = None

    controller = None
    attr = None
    status = None

    health = -1
    mana = -1
    isDead = False

    target = None

    def __init__(self, world=None, owner=None):
        self.world = world
        self.controller = Controller(world=world, owner=owner)

        if world:
            world.add_object(self)

        self.attr = Attributes()
        self.status = StatusEffects()
        self.health = self.attr.MaxHealth
        self.mana = self.attr.MaxMana

    def tick(self):
        if self.isDead:
            return

        self.status.tick()

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


