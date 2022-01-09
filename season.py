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
SEASON_BEFOR_FIRST_MOLAD = SEASON_LENGTH * 2 + TimeInWeek(1, 23) - LUNAR_MONTH * 6
"""How long before the molad of Nissan in the year 1 of creation was the begining of the Nissan season. (7, 9, 642)"""
#9:4b
SOLAR_YEAR_EXCESS = SOLAR_YEAR - LUNAR_YEAR
"""The excess of a 365.25 day year over a 12 month year (10, 21, 204)"""
#9:4d
LONG_CYCLE_LENGTH = 7 * 4
"""The number of years it takes for the seasons to return their beginings to the same time of week, if the length of a solar year is exactly 365.25 days. (28)"""
FIRST_MOLAD_TIME_OF_WEEK = TimeInWeek(4,0)
"""The time of week of the begining of the Nissan season in the year of creation. (4, 0)"""
SOLAR_YEAR_REMAINDER = TimeInWeek(*SOLAR_YEAR)
"""The offset of a solar year within the week. (1, 6)"""
#9:5
SEASON_LENGTH_REMAINDER = TimeInWeek(*SEASON_LENGTH)
"""The offset of a season within the week. (0, 7, 540)"""

class SolarYear:
    
	def __init__(self, year: Year) -> None:
		# Save the year
		self.my_year = year
		self.calc_season()

	def calc_season(self):
		# Calculate the time relative to the day of the molad for the first season of this 19 year cycle.
		season_offset = self.my_year.cyclesToYear * SOLAR_CYCLE_EXCESS - SEASON_BEFOR_FIRST_MOLAD
		# Add the offset of each year
		season_offset += (self.my_year.placeInCycle -1) * SOLAR_YEAR_EXCESS
		# Take away the full months (in place of the leap months of the lunar years).
		while season_offset > LUNAR_MONTH: 
			season_offset -= LUNAR_MONTH
		# Add this offset to the molad Nissan of that year.
		thisMonth = Month(self.my_year, 1)
		self.season_time = season_offset + (0, thisMonth.molad.hours, thisMonth.molad.parts)
		# When the season time is before molad Nissan, there are two possible reasons.
		if self.season_time.parts != 0:
			# Sometimes it is because the season is this many days after the molad of Addar II.
			if self.my_year.placeInCycle in LEAP_YEARS:
				thisMonth = Month(self.my_year, 13)
			# Other times (until the year 3000 from creation) it is bacause the offset is negative, and we need to take away another month.
			else:
				season_offset -= LUNAR_MONTH
			self.season_time = season_offset + (0, thisMonth.molad.hours, thisMonth.molad.parts)
    
	def season(self, seasonNumber=0):
		"""Gives the time of the specified season's start, in days from the day of molad Nissan."""
		return self.season_time + SEASON_LENGTH * seasonNumber

	def season_time_of_week(self, seasonNumber=0):
		"""Gives the day of the week and time of the season's start."""
		# Look at the number of year into the current cycle of 28 years.
		place_in_long_cycle = (self.my_year.yearsFromCreation -1) % LONG_CYCLE_LENGTH
		# Multiply that by the offset of a solar year within the week.
		season0_offset = place_in_long_cycle * SOLAR_YEAR_REMAINDER
		# Add the time of week of the first season of the cycle.
		season0_time = season0_offset + FIRST_MOLAD_TIME_OF_WEEK
		# Add the offset of each of the intervening seasons. 
		return season0_time + seasonNumber * SEASON_LENGTH_REMAINDER