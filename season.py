from timeInterval import timeInterval
from year import Year, LUNAR_YEAR, CYCLE_YEARS, CYCLE
from month import Month

#9:1
solarYear = timeInterval(365,6)
"""The length of a year of 365.25 days"""
#9:2
solarCycle = solarYear * CYCLE_YEARS
"""The length of 19 years of 365.25 days"""
solarCycleExcess = solarCycle - CYCLE
"""The movement of the seasons relative to the molad after a 19 year cycle"""
seasonLength = solarYear // 4
"""The length of a season, one quarter of a 365.25 day year"""

#9:3
seasonBeforeMolad = timeInterval(7, 9, 642)
"""How long before the molad of Nissan in the year 1 of creation was the begining of the Nissan season"""
solarYearExcess = solarYear - LUNAR_YEAR
"""The excess of a 365.25 day year over a 12 month year"""

class season:
    """Hold the time of a season's starting point"""
    def __init__(self, thisYear: Year, seasonNumber: int = 0) -> None:
        if thisYear.placeInCycle == 1:
            timeDifference = solarCycleExcess * thisYear.cyclesToYear - seasonBeforeMolad
            yearStartingCycle = Year(thisYear.yearsFromCreation - thisYear.placeInCycle + 1)
            moladStartingCycle = Month(yearStartingCycle, 1).molad
            self.time = moladStartingCycle + timeDifference
        else:
            timeDifference = (solarYearExcess * thisYear.cyclesToYear) + (solarYearExcess * (thisYear.placeInCycle - 1)) - seasonBeforeMolad
          #  while (timeDifference is greater than lunarMunth):

        self.time + solarYearExcess * (thisYear.placeInCycle-1)
        self.time + seasonLength * seasonNumber