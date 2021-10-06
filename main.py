from attributes import *





if __name__ == "__main__":
    world = World()
    inspector = Inspector()
    inspector.world = world
    obj1 = Actor()
    obj2 = Actor()

    world.add_object(obj1)
    world.add_object(obj2)
    world.tickN(2500)
    inspector.apply_physical_damage(50, obj1, obj2)
    print(obj2.health)
    world.tickN(500)
    print(obj2.health)
    inspector.apply_heal(20, obj1, obj2)
    print(obj2.health)
    world.tickN(2500)
    inspector.apply_magic_damage(50, obj1, obj2)
    print(obj2.health)
    world.tick1000()
    world.tick1000()
