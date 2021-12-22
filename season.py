from timeMeasures import timeInterval
from calendarUnits import Year, LUNAR_YEAR, CYCLE_YEARS, CYCLE, Month

#9:1
SOLAR_YEAR = timeInterval(365.25)
"""The length of a year of 365.25 days"""
#9:2
SOLAR_CYCLE = SOLAR_YEAR * CYCLE_YEARS
"""The length of 19 years of 365.25 days"""
SOLAR_CYCLE_EXCESS = SOLAR_CYCLE - CYCLE
"""The movement of the seasons relative to the molad after a 19 year cycle"""
SEASON_LENGTH = SOLAR_YEAR // 4
"""The length of a season, one quarter of a 365.25 day year"""

#9:3
seasonBeforeMolad = timeInterval(7, 9, 642)
"""How long before the molad of Nissan in the year 1 of creation was the begining of the Nissan season"""
SOLAR_YEAR_EXCESS = SOLAR_YEAR - LUNAR_YEAR
"""The excess of a 365.25 day year over a 12 month year"""

class season:
    """Hold the time of a season's starting point"""
    def __init__(self, thisYear: Year, seasonNumber: int = 0) -> None:
        if thisYear.placeInCycle == 1:
            timeDifference = SOLAR_CYCLE_EXCESS * thisYear.cyclesToYear - seasonBeforeMolad
            yearStartingCycle = Year(thisYear.yearsFromCreation - thisYear.placeInCycle + 1)
            moladStartingCycle = Month(yearStartingCycle, 1).molad
            self.time = moladStartingCycle + timeDifference
        else:
            timeDifference = (SOLAR_YEAR_EXCESS * thisYear.cyclesToYear) + (SOLAR_YEAR_EXCESS * (thisYear.placeInCycle - 1)) - seasonBeforeMolad
          #  while (timeDifference is greater than lunarMunth):

        self.time + SOLAR_YEAR_EXCESS * (thisYear.placeInCycle-1)
        self.time + SEASON_LENGTH * seasonNumber