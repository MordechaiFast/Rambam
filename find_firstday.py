from classes.calendarUnits import Day, Month, Year
from classes.sighting import sighting


p, n = 0, 0
for y in range(5780, 5800):
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
print(f'{p/n = }')