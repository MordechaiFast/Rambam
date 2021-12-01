from timeInterval import timeInterval
from year import year, lunarYear, cycleYears, cycle
from month import month

#9:1
solarYear = timeInterval(365,6)
"""The lenght of a year of 365.25 days"""
#9:2
solarCycle = solarYear * cycleYears
"""The lenght of 19 years of 365.25 days"""
solarCycleExcess = solarCycle - cycle
"""The movement of the seasons relative to the molad after a 19 year cycle"""
seasonLength = solarYear // 4
"""The lenght of a season, one quarter of a 365.25 day year"""

#9:3
seasonBeforeMolad = timeInterval(7, 9, 642)
"""How long before the molad of Nissan in the year 1 of creation was the begining of the Nissan season"""
solarYearExcess = solarYear - lunarYear
"""The excess of a 365.25 day year over a 12 month year"""

class season:
    """Hold the time of a season's starting point"""
    def __init__(self, thisYear: year, seasonNumber: int = 0) -> None:
        if thisYear.placeInCycle == 1:
            timeDifference = solarCycleExcess * thisYear.cyclesToYear - seasonBeforeMolad
            yearStartingCycle = year(thisYear.yearsFromCreation - thisYear.placeInCycle + 1)
            moladStartingCycle = month(yearStartingCycle, 1).molad
            self.time = moladStartingCycle + timeDifference
        else:
            timeDifference = (solarYearExcess * thisYear.cyclesToYear) + (solarYearExcess * (thisYear.placeInCycle - 1)) - seasonBeforeMolad
          #  while (timeDifference is greater than lunarMunth):

        self.time + solarYearExcess * (thisYear.placeInCycle-1)
        self.time + seasonLength * seasonNumber