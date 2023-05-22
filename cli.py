from classes.calendarUnits import Year, Month, Day
from classes.degrees import Degrees
from sighting import (solar_position, lunar_position, lunar_lattitude, 
    distance, annalisys, sighting)
from argparse import ArgumentParser

parser = ArgumentParser(
    description='A command-line script for determining if the moon will be'
    ' visable on a given month'
)
parser.add_argument(
    'day',
    nargs='?',
    default=0,
    type=int,
    help='The day of the month to calculate for. 0 or left blank will search '
    'for the first day of the month when the moon is visable',
)
parser.add_argument(
    'month',
    type=int,
    help='The number for the month (1=Nissan, 13=Addar II)',
)
parser.add_argument(
    'year',
    type=int,
    help='The year to calculate for (1=BHRD)',
)
parser.add_argument(
    '-v', '--verbose',
    action='count',
    default=0,
    help='Display the intermediary calculations. '
    'Double for dipalaying all of the intermediary steps.'
)

args = parser.parse_args()
if args.day == 0:
    month = Month(Year(args.year), args.month)
    print(f'Molad {month}: {month.molad}')
    for day in month:
        if sighting(day):
            print(f'The moon will be see on {day} ({day.day_of_week})')
            wanted_day = day
            break
else:
    wanted_day = Day(Month(Year(args.year), args.month), args.day)
    print(f"Date: {wanted_day} ({wanted_day.day_of_week})")

if args.verbose > 1:
    solar_position(wanted_day, verbose=True)
    print()
    lunar_position(wanted_day, verbose=True)
    print()
    lunar_lattitude(wanted_day, verbose=True)
    print()
    annalisys(wanted_day, verbose=True)
    print()
elif args.verbose == 1:
    print(f'solar position  {str(solar_position(wanted_day)):>10}')
    print(f'lunar position  {str(lunar_position(wanted_day)):>10}')
    lattitude = lunar_lattitude(wanted_day)
    print('lunar lattitude',
        ('N' if lattitude > Degrees(0) else 'S'), abs(lattitude))
    print(f'distance        {str(distance(wanted_day)):>10}')
    print(f'viewing arc     {str(annalisys(wanted_day)):>10}')
    
if args.day != 0:
    sighting(wanted_day, verbose=True)
print()