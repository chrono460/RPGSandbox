from world import *


class Controller(Object):
    name = "New Controller"
    owner = None
    world = None

    def __init__(self, world=None, owner=None):
        self.world = world
        self.owner = owner

        if world:
            world.add_object(self)

        #if owner:
            #owner.add_controller(self)

    def tick(self):
        pass

    def query(self, pawn):
        # run behaviour tree
        # searching enemy
        # set as target, approach -> battle loop
        if pawn.target:
            if not pawn.target.isDead:
                pawn.auto_attack()
            else:
                pawn.target = None
        else:
            tt = self.world.env.env_get_one_enemy(self)
            if tt:
                pawn.target = tt
                print(pawn.name+" sets target to "+tt.name)
