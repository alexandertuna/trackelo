import constants
import utility

class Result:
    def __init__(self, filename):
        self.filename = filename
        self.lines    = self.getLines()
        self.names    = [self.getName(line) for line in self.lines]
        self.places   = [self.getPlace(line) for line in self.lines]

    def getLines(self):
        lines = []
        with open(self.filename) as fi:
            for line in fi:
                lines.append(line.strip())
        return lines

    def getName(self, line):
        # From: 5.	Elliot GILES	26 MAY 1994	GBR
        # To: Elliot GILES
        return " ".join(line.split()[constants.LINE_INDEX_NAME : constants.LINE_INDEX_DAY])

    def getPlace(self, line):
        # From: 5.	Elliot GILES	26 MAY 1994	GBR
        # To: 5
        return int(line.split()[constants.LINE_INDEX_PLACE].rstrip("."))
