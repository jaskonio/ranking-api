# from typing import List
# from Domain.Race import Race
# from Domain.Runner import Runner


# class FinalRanking:
#     def __init__(self):
#         self.historial:List[Race] = []
#         self.sorted = False

#     def add_race(self, race:Race):
#         self.historial.append(race)
#         self.sorted = False

#     def get_final_ranking(self):        
#         self.__sort_final_ranking()

#         return self.historial

#     def show_ranking_final(self):
#         print("Ranking final:")
#         ranking_final = self.calcular_ranking_final()
#         for i, persona in enumerate(ranking_final, start=1):
#             print(f"{i}. {persona.nombre} - Puntos totales: {persona.puntos}")

#     def __order_races(self):
#         self.historial = sorted(self.historial, key=lambda race: (race.order))
#         self.sorted = True

#     def __sort_final_ranking(self):
#         if not self.sorted:
#             self.__order_races()

#         ranking_final = {}

#         for race in self.historial:
#             for i, runner in enumerate(race.get_ranking(), start=1):
#                 if runner.nombre not in ranking_final:
#                     ranking_final[runner.nombre] = Runner(runner.nombre)
#                 ranking_final[runner.nombre].puntos += runner.puntos
#                 ranking_final[runner.nombre].posiciones_ant.append(i)

#         self.historial = sorted(ranking_final.values(), key=lambda runner: (runner.puntos, sum(runner.posiciones_ant) / len(runner.posiciones_ant)), reverse=True)

