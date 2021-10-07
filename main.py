from actor import *
from pawn import *

if __name__ == "__main__":
    world = World()

    # set alliance
    world.env.add_alliance("Team1")
    world.env.add_alliance("Team2")
    world.env.add_alliance("Neutral")
    world.env.set_relation("Team1", "Team1", 1)
    world.env.set_relation("Team2", "Team2", 1)
    world.env.set_relation_mutual("Team1", "Team2", -1)

    # add player
    p1 = Player(world=world, name="kirito", alliance="Team1")
    p2 = Player(world=world, name="sakuya", alliance="Team2")

    inspector = Inspector(world)
    obj1 = Pawn(world=world, owner=p1)
    obj2 = Pawn(world=world, owner=p2)
    obj3 = Pawn(world=world, owner=p1)
    obj4 = Pawn(world=world, owner=p2)

    world.tickN(500)
    #inspector.apply_physical_damage(50, obj1, obj2)
    #print(obj2.health)
    world.tickN(500)
    #print(obj2.health)
    inspector.apply_heal(100, obj4, obj2)
    #print(obj2.health)
    world.tickN(2500)
    #inspector.apply_magic_damage(50, obj1, obj2)
    #print(obj2.health)
    world.tickN(2500)
    world.tickN(2500)
