from numbers import Number
from typing import List
from Domain.Runner import Runner
from datetime import datetime

class Race:
    def __init__(self, name):
        self.name = name
        self.ranking:List[Runner] = []
        self.order:Number = 0
        self.sorted:bool = False
        
        self.format = "%H:%M:%S"

    def add_runner(self, runner):
        self.ranking.append(runner)
        self.sorted = False

    def get_ranking(self):
        if not self.sorted:
            self.__sort_runners()
            self.__set_points()
        
        return self.ranking

    def __sort_runners(self):
        # Orderna los Runner primero por finished True primero False segundo, realTime y officialTime

        self.ranking = sorted(self.ranking, key=lambda runner: (not runner.finished, datetime.strptime(runner.realTime, self.format), datetime.strptime(runner.officialTime, self.format)), reverse=False)
        
        self.sorted = True

    def __set_points(self):
        if not self.sorted:
            self.sort_runners()

        # Asignar puntos solo a las 10 primeras personas en llegar a la meta
        for i, persona in enumerate(self.ranking[:10], start=1):
            persona.puntos = 10 - i + 1