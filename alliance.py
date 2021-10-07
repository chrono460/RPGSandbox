from object import *


class Alliance(Object):
    _meta = {}

    def __init__(self):
        super(Alliance, self).__init__()
        self.add_alliance("Team1")
        self.add_alliance("Team2")
        self.add_alliance("Neutral")
        self.set_relation("Team1", "Team1", 1)
        self.set_relation("Team2", "Team2", 1)
        self.set_relation_mutual("Team1", "Team2", -1)

    def add_alliance(self, name):
        if name in self._meta:
            return

        rel = {key: 0 for (key, _) in self._meta.items()}
        self._meta[name] = rel

        for s, _ in self._meta.items():
            self._meta[s][name] = 0

    def remove_alliance(self, name):
        if name not in self._meta:
            return

        del self._meta[name]

        for s, _ in self._meta.items():
            del self._meta[s][name]

    def set_relation(self, me, other, num):
        self._meta[me][other] = num

    def set_relation_mutual(self, me, other, num):
        self.set_relation(me, other, num)
        self.set_relation(other, me, num)

    def query_relation(self, me, other):
        if me in self._meta and other in self._meta:
            return self._meta[me][other]
        return None
