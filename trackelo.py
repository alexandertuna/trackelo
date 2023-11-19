import math

import athlete
import constants
import result
import utility

def main():
    results = getResults()
    athletes = getAthletes(results)

    for result in results:
        delo = {}
        for name in result.names:
            delo[name] = calculate(athletes[name], athletes, result)
        print(f"{result.filename} results")
        for name in delo:
            athletes[name].elo += delo[name]
            athletes[name].elo = max(athletes[name].elo, constants.STARTING_ELO)
            print(f" {name:30} -> delta = {int(delo[name])} -> new total = {int(athletes[name].elo)}")
        print("")

    print("Total")
    for name in sorted(athletes, key=lambda name: athletes[name].elo, reverse=True):
        print(f"{name:30} {int(athletes[name].elo)}")

def getResults():
    return [result.Result(fname) for fname in utility.getDataFileNames()]

def getAthletes(results):
    names = set()
    for result in results:
        for name in result.names:
            names.add(name)
    return {name: athlete.Athlete(name) for name in names}

def calculate(athlete, athletes, result):
    delo = 0
    place = result.places[result.names.index(athlete.name)]
    for othername, otherplace in zip(result.names, result.places):
        if othername == athlete.name:
            continue
        otherathlete = athletes[othername]
        comparison = utility.comparePlaces(place, otherplace)
        change, otherchange = eloResult(athlete, otherathlete, comparison)
        delo += change
        # print(f"{change}, {otherchange} :: {comparison} :: {athlete.name} from ({place}) vs {othername} ({otherplace})")
    return delo

def eloResult(athlete, otherathlete, comparison):
    elodiff = -1*(athlete.elo - otherathlete.elo)
    expectation = expectedProbability(elodiff)
    delta = constants.KFACTOROPTION * (comparison - expectation)
    return (delta, -delta)

def expectedProbability(elodiff):
    # https://mattmazzola.medium.com/implementing-the-elo-rating-system-a085f178e065
    exponent = elodiff / constants.EXPONENTDENOMINATOR
    return 1 / (1 + math.pow(constants.EXPONENTBASE, exponent))

if __name__ == "__main__":
    main()
