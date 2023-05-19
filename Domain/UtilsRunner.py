from Domain.Runner import Runner


def build_runner(dorsal=None, name=None, club=None, nationality=None, finished=None, gender=None, category=None,
                 officialTime=None, officialPos=None, officialAverageTime=None, officialCatPos=None, officialGenPos=None, 
                 realTime=None, realPos=None, realAverageTime=None, realCatPos=None, realGenPos=None,
                 puntos=0, posiciones_ant=[]) -> Runner:
    
    new_runner = Runner(name)
    new_runner.dorsal = dorsal
    
    new_runner.club = club
    new_runner.nationality = nationality
    new_runner.finished = finished
    new_runner.gender = gender
    new_runner.category = category
    new_runner.officialTime = officialTime
    new_runner.officialPos = officialPos
    new_runner.officialAverageTime = officialAverageTime
    new_runner.officialCatPos = officialCatPos
    new_runner.officialGenPos = officialGenPos

    new_runner.realTime = realTime
    new_runner.realPos = realPos
    new_runner.realAverageTime = realAverageTime
    new_runner.realCatPos = realCatPos
    new_runner.realGenPos = realGenPos

    new_runner.puntos = puntos
    new_runner.posiciones_ant = posiciones_ant

    return new_runner
