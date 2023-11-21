import math

import athlete
import constants
import query
import result
import utility

def main():

    # gather results
    results = getResults()
    athletes = getAthletes(results)

    # check each result
    for result in results:
        delo = {}
        for name in result.names:
            delo[name] = calculate(athletes[name], athletes, result)
        print(f"{result.date} {result.racename} results")
        for name in delo:
            athletes[name].elo += delo[name]
            athletes[name].elo = max(athletes[name].elo, constants.STARTING_ELO)
            print(f" {name:30} -> delta = {int(delo[name])} -> new total = {int(athletes[name].elo)}")
        print("")

    # summarize
    print("Total")
    for name in sorted(athletes, key=lambda name: athletes[name].elo, reverse=True):
        print(f"{name:30} {int(athletes[name].elo)}")

def getResults():
    results = []
    competitionIds = [
        7172922,
        7172925,
        7172926,
        7155407,
        7154228,
        7155467,
        7172927,
        7147656,
        7154214,
        7172928,

        7154215,
        7190105,
        7154216,
        7154217,

        7138987,

    ]

    # NB: order is important
    # They sometimes track the 1500m split of a mile race
    eventIds = [
        10229632, # 2000m
        10229503, # mile
        10229502, # 1500m
    ]
    gender = "M"

    for competitionId in competitionIds:
        for eventId in eventIds:
            site = f"https://worldathletics.org/competition/calendar-results/results/{competitionId}?eventId={eventId}&gender={gender}"
            eventResults = [result.Result(f"{competitionId} {racename}", date, table) for (racename, date, table) in query.query(site)]
            # championships tend to be in reverse order
            results.extend(reversed(eventResults))
            if eventResults:
                break
    results = sorted(results, key=lambda result: result.datetuple)
    return results

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
