import constants
import utility

class Athlete:
    def __init__(self, name):
        self.name = name
        self.elo = constants.STARTING_ELO

# def makeAthletes():
#     return [ Athlete(name) for name in utility.getAthleteNames() ]
