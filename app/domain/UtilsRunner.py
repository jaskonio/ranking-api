from ..model.RunnerModel import RunnerModel

def build_runner(dorsal=0, name="", club="", nationality="", finished="", gender="", category="",
                 officialTime="", officialPos="", officialAverageTime="", officialCatPos="", officialGenPos="", 
                 realTime="", realPos="", realAverageTime="", realCatPos="", realGenPos="",
                 puntos=0, posiciones_ant=[]):
    finished = strtobool(finished)
    officialPos = convert_to_int(officialPos)
    officialCatPos = convert_to_int(officialCatPos)
    officialGenPos = convert_to_int(officialGenPos)
    realPos = convert_to_int(realPos)    
    realCatPos = convert_to_int(realCatPos)
    realGenPos = convert_to_int(realGenPos)    
    
    puntos = convert_to_int(puntos)
    new_runner = RunnerModel(name= name, dorsal=dorsal, club=club, nationality=nationality, finished=finished, gender=gender, category=category, 
                             officialTime=officialTime, officialPos=officialPos, officialAverageTime=officialAverageTime, officialCatPos=officialCatPos, officialGenPos=officialGenPos, 
                             realTime=realTime, realPos=realPos, realAverageTime=realAverageTime, realCatPos=realCatPos, realGenPos=realGenPos, 
                             puntos=puntos, posiciones_ant=posiciones_ant)

    return new_runner

def strtobool(val):
    """Convert a string representation of truth to true or false.
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = str(val).lower()

    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))

def convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
