from classes.calendarUnits import Day, Month, Year
from sighting import sighting


p, n = 0, 0
first_year, last_year = 5750, 5780
for y in range(first_year, last_year):
    year = Year(y)
    #print(f'Year {year}: {year.molad}, {year.Rosh_Hashana}')
    for month in year:
        n += 1
        day = Day(month, 1)
        if sighting(day):
            p += 1
        else:
            day += 1
            if sighting(day):
                p += 1
    #        print(day.month.name, end=', ')
    #print()
print(f'{first_year = } {last_year = }')
print(f'{p/n = }') 