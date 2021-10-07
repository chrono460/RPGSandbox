from object import *
from alliance import *


class EnvironmentQuery(Alliance):
    name = "New EnvironmentQuery"

    def __init__(self):
        super(EnvironmentQuery, self).__init__()

    def env_get_one_enemy(self, controller):
        for _, obj in controller.world.objects.items():
            try:
                if obj.controller and not obj.isDead:
                    if self.query_relation(controller.owner.alliance, obj.controller.owner.alliance) < 0:
                        return obj
            except AttributeError:
                pass
        return None
