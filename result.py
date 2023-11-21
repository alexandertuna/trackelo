import calendar
import sys

import constants
import utility

class Result:
    def __init__(self, racename, date, table):
        self.racename = racename
        self.date = date
        self.datetuple = self.convertDate()
        self.row_header = table[0]
        self.row_entries = table[1:]
        self.names = self.getColumn("Name")
        self.places = self.getColumn("Place")
        self.marks = self.getColumn("Mark")
        self.names, self.places, self.marks = self.removeDnfs()
        self.places = [int(pl.rstrip(".")) for pl in self.places]

    def getColumn(self, column_name):
        index = self.row_header.index(column_name)
        return [row[index] for row in self.row_entries]

    def removeDnfs(self):
        names, places, marks = [], [], []
        for name, place, mark in zip(self.names, self.places, self.marks):
            if not place:
                continue
            names.append(name)
            places.append(place)
            marks.append(mark)
        return names, places, marks

    def convertDate(self):
        month2number = {month.lower(): index for index, month in enumerate(calendar.month_abbr) if month}
        day, month, year = self.date.split()
        if "-" in day or "–" in day: # multi-day meet
            day = day.split("-")[0].split("–")[0]
        return (int(year), month2number[month.lower()], int(day))

