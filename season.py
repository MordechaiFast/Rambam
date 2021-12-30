from timeMeasures import TimeInterval
from calendarUnits import Year, LUNAR_YEAR, CYCLE_YEARS, CYCLE, Month

#9:1
SOLAR_YEAR = TimeInterval(365.25)
"""The length of a year of 365.25 days"""
#9:2
SOLAR_CYCLE = SOLAR_YEAR * CYCLE_YEARS
"""The length of 19 years of 365.25 days"""
SOLAR_CYCLE_EXCESS = SOLAR_CYCLE - CYCLE
"""The movement of the seasons relative to the molad after a 19 year cycle"""
SEASON_LENGTH = SOLAR_YEAR // 4
"""The length of a season, one quarter of a 365.25 day year"""

#9:3
SEASON_BEFOR_MOLAD = TimeInterval(7, 9, 642)
"""How long before the molad of Nissan in the year 1 of creation was the begining of the Nissan season"""
#9:4
SOLAR_YEAR_EXCESS = SOLAR_YEAR - LUNAR_YEAR
"""The excess of a 365.25 day year over a 12 month year"""

class season:
    """Hold the time of a season's starting point"""
    def __init__(self, thisYear: Year, seasonNumber: int = 0) -> None:
        # First calculate for the first year and season of the cycle
        timeDifference = SOLAR_CYCLE_EXCESS * thisYear.cyclesToYear - SEASON_BEFOR_MOLAD
        yearStartingCycle = Year(thisYear.yearsFromCreation - thisYear.placeInCycle + 1)
        moladStartingCycle = Month(yearStartingCycle, 1).molad
        self.time = moladStartingCycle + timeDifference
        #self.time += SOLAR_YEAR_EXCESS * (thisYear.placeInCycle - 1)
          #  while (timeDifference is greater than lunarMunth):

        #self.time + SOLAR_YEAR_EXCESS * (thisYear.placeInCycle-1)
        #self.time + SEASON_LENGTH * seasonNumber