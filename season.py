from calendarUnits import *

#9:1
SOLAR_YEAR = TimeInterval(365.25)
"""The length of a year of 365.25 days"""
#9:2
SOLAR_CYCLE = SOLAR_YEAR * CYCLE_YEARS
"""The length of 19 years of 365.25 days"""
SOLAR_CYCLE_EXCESS = SOLAR_CYCLE - CYCLE
"""The movement of the seasons relative to the molad after a 19 year cycle. (0, 1, 485)"""
SEASON_LENGTH = SOLAR_YEAR // 4
"""The length of a season, one quarter of a 365.25 day year. (91, 7, 540)"""

#9:3
SEASON_BEFOR_MOLAD = SEASON_LENGTH * 2 + (1, 23) - LUNAR_MONTH * 6
"""How long before the molad of Nissan in the year 1 of creation was the begining of the Nissan season. (7, 9, 642)"""
#9:4
SOLAR_YEAR_EXCESS = SOLAR_YEAR - LUNAR_YEAR
"""The excess of a 365.25 day year over a 12 month year"""

class season:
	"""Hold the time of a season's starting point"""
	def __init__(self, thisYear: Year, seasonNumber: int = 0) -> None:
    	# First calculate for the first year and season of the cycle
		timeDifference = SOLAR_CYCLE_EXCESS * thisYear.cyclesToYear + SOLAR_YEAR_EXCESS * (thisYear.placeInCycle -1) - SEASON_BEFOR_MOLAD
		while timeDifference >= LUNAR_MONTH:
			timeDifference -= LUNAR_MONTH
		yearStartingCycle = Year(thisYear.yearsFromCreation - thisYear.placeInCycle + 1)
		moladStartingCycle = Month(yearStartingCycle, 1).molad
		self.time = moladStartingCycle + timeDifference
		self.time += SOLAR_YEAR_EXCESS * (thisYear.placeInCycle - 1)

        #self.time + SOLAR_YEAR_EXCESS * (thisYear.placeInCycle-1)
        #self.time + SEASON_LENGTH * seasonNumber

class SolarYear:
    
	def __init__(self, thisYear: Year) -> None:
		season_offset = SOLAR_CYCLE_EXCESS * thisYear.cyclesToYear + SOLAR_YEAR_EXCESS * (thisYear.placeInCycle -1) - SEASON_BEFOR_MOLAD
		while season_offset > LUNAR_MONTH: 
			season_offset -= LUNAR_MONTH
		thisMonth = Month(thisYear, 1)
		self.season_time = season_offset + (0, thisMonth.molad.hours, thisMonth.molad.parts)
		if self.season_time.parts != 0:
			if thisYear.placeInCycle in LEAP_YEARS:
				thisMonth = Month(thisYear, 13)
			else:
				season_offset -= LUNAR_MONTH
			self.season_time = season_offset + (0, thisMonth.molad.hours, thisMonth.molad.parts)
    
	def season(self, seasonNumber):
		return self.season_time + SEASON_LENGTH * seasonNumber