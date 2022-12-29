from classes.calendarUnits import Year, Month, Day
from classes.degrees import Degrees, DegreesOfCircle

# 11:9
signs = {
    'טלה': DegreesOfCircle(0),
    'שור': DegreesOfCircle(30),
    'תאומים': DegreesOfCircle(60),
    'סרטן': DegreesOfCircle(90),
    'אריה': DegreesOfCircle(120),
    'בתולה': DegreesOfCircle(150),
    'מאזנים': DegreesOfCircle(180),
    'עקרב': DegreesOfCircle(210),
    'קשת': DegreesOfCircle(240),
    'גדי': DegreesOfCircle(270),
    'דלי': DegreesOfCircle(300),
    'דגים': DegreesOfCircle(330),
}

def mid(sign) -> int:
    lower = None
    higher = 360
    for value in signs.values():
        if value == sign:
            lower = value
            continue
        if lower is not None:
            higher = value
            break
    return (round(lower) + round(higher)) // 2

def find_by_range(place: Degrees, table: dict):
    reference = round(place)
    lower_bound = None
    for bound in table:
        if reference < round(bound):
            break
        else:
            lower_bound = bound
    if lower_bound is None or table[lower_bound] is None:
        raise ValueError(f'{place} is out of range')
    else:
        return table[lower_bound]

def midpoint(start: Degrees, finnish: Degrees) -> DegreesOfCircle:
    start = Degrees(*start)
    finnish = Degrees(*finnish)
    return DegreesOfCircle(*(start + finnish)) / 2

# printing templates
result = "{:29} {:>10}"
sign_result = "{:29}{}{:>10}"

# 11:16
start_year = Year(4938)
assert(start_year.cycles_to_year == 259)
assert(start_year.place_in_cycle == 17)
start_month = Month(start_year, 1) #Nissan
start_day = Day(start_month, 3)
assert(start_day.day_of_week == 5)

# 12:1
solar_progresion_delta = DegreesOfCircle(98, 33, 53) /10/10
assert(solar_progresion_delta        == Degrees(  0, 59,  8))
assert(solar_progresion_delta *10    == Degrees(  9, 51, 23))
assert(solar_progresion_delta *100   == Degrees( 98, 33, 53))
assert(solar_progresion_delta *1000  == Degrees(265, 38, 50))
assert(solar_progresion_delta *10000 == Degrees(136, 28, 20))
#print(*reversed("מהלך השמש האמצעי"), sep='')
#for n in (*range(1, 10), *range(10, 100, 10), *range(100, 1000, 100),
#          *range(1000, 11000, 1000)):
#    print(f"{n:>5}: {solar_progresion_delta * n:>10s}")
assert(solar_progresion_delta *29    == Degrees( 28, 35,  1))
assert(solar_progresion_delta *354   == Degrees(348, 55,  9))

# 12:2
solar_hight_delta = DegreesOfCircle(0, 0, 15) /10/10
assert(solar_hight_delta * 10    == Degrees(0, 0, 1, 30))
assert(solar_hight_delta * 100   == Degrees(0, 0, 15))
assert(solar_hight_delta * 1000  == Degrees(0, 2, 30))
assert(solar_hight_delta * 10000 == Degrees(0, 25))
assert(solar_hight_delta * 29    == Degrees(0, 0,  4))
assert(solar_hight_delta * 354   == Degrees(0, 0, 53))

def tracking_correction(track: Degrees, tracking: dict) -> Degrees:
    track = round(track)
    # 13:2
    if track < 180:
        sign = -1
    elif track == 180:
        return Degrees(), 1
    else:
        track = 360 - track
        sign = 1
    # 13:7
    upper_track = tracking[track // 10 * 10 + 10]
    lower_track = tracking[track // 10 * 10]
    track_average = (upper_track - lower_track) / 10
    return (lower_track + track_average * (track % 10)), sign
# 12-13 summary
def solar_progresion(date: Day) -> DegreesOfCircle:
    solar_progresion_delta = DegreesOfCircle(98, 33, 53) /10/10
    solar_progresion_start = signs['טלה'] + Degrees(7, 3, 32)
    days = date.date - start_day.date
    return solar_progresion_start + solar_progresion_delta * days

def solar_position(date: Day, verbose=False) -> DegreesOfCircle:
    solar_hight_delta = DegreesOfCircle(0, 0, 15) /10/10
    solar_hight_start = signs['תאומים'] + Degrees(26, 45, 8)
    solar_tracking = {
        0:   Degrees(),
        10:  Degrees(0, 20),
        20:  Degrees(0, 40),
        30:  Degrees(0, 58),
        40:  Degrees(1, 15),
        50:  Degrees(1, 29),
        60:  Degrees(1, 41),
        70:  Degrees(1, 51),
        80:  Degrees(1, 57),
        90:  Degrees(1, 59),
        100: Degrees(1, 58),
        110: Degrees(1, 53),
        120: Degrees(1, 45),
        130: Degrees(1, 33),
        140: Degrees(1, 19),
        150: Degrees(1,  1),
        160: Degrees(0, 42),
        170: Degrees(0, 21),
        180: Degrees()
    }

    current_solar_progresion = solar_progresion(date)
    days = date.date - start_day.date
    current_solar_hight = solar_hight_start + solar_hight_delta * days
    solar_track = current_solar_progresion - current_solar_hight
    solar_correction, sign = tracking_correction(solar_track, solar_tracking)
    true_solar_position = current_solar_progresion + solar_correction * sign
    if verbose:
        print(result.format('solar progresion', str(current_solar_progresion)))
        print(result.format('solar hight', str(current_solar_hight)))
        print(result.format('solar track distance', str(solar_track)))
        print(sign_result.format('solar correction',
            ('-' if sign == -1 else '+'), str(solar_correction)))
        print(result.format('true solar position', str(true_solar_position)))
    return true_solar_position

# 14:1-2
lunar_progresion_delta = DegreesOfCircle(*(Degrees(1317, 38, 23) /10/10))
assert(lunar_progresion_delta        == Degrees( 13, 10, 35))
assert(lunar_progresion_delta *10    == Degrees(131, 45, 50))
assert(lunar_progresion_delta *100   == Degrees(237, 38, 23))
assert(lunar_progresion_delta *1000  == Degrees(216, 23, 50))
assert(lunar_progresion_delta *10000 == Degrees(  3, 58, 20))
assert(lunar_progresion_delta *29    == Degrees( 22,  6, 56))
assert(lunar_progresion_delta *354   == Degrees(344, 26, 41))
#14:3-4
lunar_track_progresion_delta = DegreesOfCircle(*(Degrees(1306, 29, 53) /10/10))
assert(lunar_track_progresion_delta        == Degrees( 13,  3, 54))
assert(lunar_track_progresion_delta *10    == Degrees(130, 38, 59))
assert(lunar_track_progresion_delta *100   == Degrees(226, 29, 53))
assert(lunar_track_progresion_delta *1000  == Degrees(104, 58, 50))
assert(lunar_track_progresion_delta *10000 == Degrees(329, 48, 20))
assert(lunar_track_progresion_delta *29    == Degrees( 18, 53,  4))
assert(lunar_track_progresion_delta *354   == Degrees(305,  0, 11))

# summary of 14-15
def lunar_position(date: Day, verbose=False) -> DegreesOfCircle:
    lunar_progresion_delta = DegreesOfCircle(*(Degrees(1317, 38, 23) /10/10))
    lunar_progresion_start = signs['שור'] + Degrees(1, 14, 43)
    lunar_track_progresion_delta = DegreesOfCircle(
        *(Degrees(1306, 29, 53) /10/10))
    lunar_track_start = DegreesOfCircle(84, 28, 42)
    seasonal_adjustments = {
        round(signs['טלה']): Degrees(),
        mid(signs['טלה']): Degrees(0, 15),
        round(signs['תאומים']): Degrees(0, 30),
        round(signs['אריה']): Degrees(0, 15),
        mid(signs['בתולה']): Degrees(),
        mid(signs['מאזנים']): Degrees(0, 15) * -1,
        round(signs['קשת']): Degrees(0, 30) * -1,
        round(signs['דלי']): Degrees(0, 15) * -1,
        mid(signs['דגים']): Degrees(),
        361: None
    }
    track_correction = {
        5:  Degrees(),
        6:  Degrees(1),
        12: Degrees(2),
        19: Degrees(3),
        25: Degrees(4),
        32: Degrees(5),
        39: Degrees(6),
        46: Degrees(7),
        52: Degrees(8),
        60: Degrees(9),
        64: None
    }
    lunar_tracking = {
        0:   Degrees(),
        10:  Degrees(0, 50),
        20:  Degrees(1, 38),
        30:  Degrees(2, 24),
        40:  Degrees(3,  6),
        50:  Degrees(3, 44),
        60:  Degrees(4, 16),
        70:  Degrees(4, 41),
        80:  Degrees(5,  0),
        90:  Degrees(5,  5),
        100: Degrees(5,  8),
        110: Degrees(4, 59),
        120: Degrees(4, 20),
        130: Degrees(4, 11),
        140: Degrees(3, 33),
        150: Degrees(2, 48),
        160: Degrees(1, 56),
        170: Degrees(0, 59),
        180: Degrees()
    }

    days = date.date - start_day.date
    current_lunar_progresion = lunar_progresion_start + (
        lunar_progresion_delta * days)
    current_solar_progresion = solar_progresion(date)
    timed_lunar_progresion = current_lunar_progresion + find_by_range(
        current_solar_progresion, seasonal_adjustments)
    distance = timed_lunar_progresion - current_solar_progresion
    double_distance = distance * 2
    current_lunar_track_progresion = lunar_track_start + (
        lunar_track_progresion_delta * days)
    try:
        corrected_lunar_track = current_lunar_track_progresion + find_by_range(
            double_distance, track_correction)
    except ValueError:
        corrected_lunar_track = current_lunar_track_progresion
    lunar_position_correction, sign = tracking_correction(
        corrected_lunar_track, lunar_tracking)
    true_lunar_position = timed_lunar_progresion + (
        lunar_position_correction * sign)
    if verbose:
        print(result.format('lunar progresion', str(current_lunar_progresion)))
        print(result.format('timed lunar progresion',
            str(timed_lunar_progresion)))
        print(result.format('distance', str(distance)))
        print(result.format('double distance', str(double_distance)))
        print(result.format('lunar track progresion',
            str(current_lunar_track_progresion)))
        print(result.format('corrected lunar track',
            str(corrected_lunar_track)))
        print(sign_result.format('lunar position correction',
            ('-' if sign == -1 else ' '), str(lunar_position_correction)))
        print(result.format('true lunar position', str(true_lunar_position)))
    return true_lunar_position

#16:2
headpoint_progresion_delta = DegreesOfCircle(*(Degrees(5, 17, 43) /10/10))
assert(headpoint_progresion_delta        == Degrees(  0,  3, 11))
assert(headpoint_progresion_delta *10    == Degrees(  0, 31, 46)) # 47
assert(headpoint_progresion_delta *100   == Degrees(  5, 17, 43))
assert(headpoint_progresion_delta *1000  == Degrees( 52, 57, 10))
assert(headpoint_progresion_delta *10000 == Degrees(169, 31, 40))
assert(headpoint_progresion_delta *29    == Degrees(  1, 32,  8)) # 9
assert(headpoint_progresion_delta *354   == Degrees( 18, 44, 43)) # 42

# Summary of 16
def lunar_lattitude(date: Day, verbose=False) -> Degrees:
    headpoint_progresion_delta = DegreesOfCircle(*(Degrees(5, 17, 43) /10/10))
    headpoint_progresion_start = DegreesOfCircle(180, 57, 28)
    width_tracking = {
        0:   Degrees(),
        10:  Degrees(0, 52),
        20:  Degrees(1, 43),
        30:  Degrees(2, 30),
        40:  Degrees(3, 13),
        50:  Degrees(3, 50),
        60:  Degrees(4, 20),
        70:  Degrees(4, 42),
        80:  Degrees(4, 55),
        90:  Degrees(5,  0),
        100: Degrees(4, 55),
        110: Degrees(4, 42),
        120: Degrees(4, 20),
        130: Degrees(3, 50),
        140: Degrees(3, 13),
        150: Degrees(2, 30),
        160: Degrees(1, 43),
        170: Degrees(0, 52),
        180: Degrees()
    }
    days = date.date - start_day.date
    current_headpoint_progresion = headpoint_progresion_start + (
        headpoint_progresion_delta * days)
    headpoint = Degrees(360) - current_headpoint_progresion
    width_track = lunar_position(date) - headpoint
    width, interm_sign = tracking_correction(width_track, width_tracking)
    direction = interm_sign * -1
    if verbose:
        print(result.format('headpoint progresion',
            str(current_headpoint_progresion)))
        print(result.format('headpoint', str(headpoint)))
        print(result.format('lattitude track', str(width_track)))
        print(sign_result.format('lunar lattitude',
            ('N' if direction == 1 else 'S'), str(width)))
    return width * direction
# Summary of 17
def distance(date: Day) -> Degrees:
    #17:1
    current_solar_position = Degrees(*solar_position(date))
    current_lunar_position = Degrees(*lunar_position(date))
    difference = current_lunar_position - current_solar_position
    if abs(difference) < Degrees(180):
        return difference
    else:
        return DegreesOfCircle(*difference)

def annalisys(date: Day, verbose=False) -> Degrees:
    perspective_length_adjustments = {
        signs['טלה']: Degrees(0, 59),
        signs['שור']: Degrees(1,  0),
        signs['תאומים']: Degrees(0, 58),
        signs['סרטן']: Degrees(0, 52),
        signs['אריה']: Degrees(0, 43),
        signs['בתולה']: Degrees(0, 37),
        signs['מאזנים']: Degrees(0, 34),
        signs['עקרב']: Degrees(0, 34),
        signs['קשת']: Degrees(0, 36),
        signs['גדי']: Degrees(0, 44),
        signs['דלי']: Degrees(0, 53),
        signs['דגים']: Degrees(0, 58),
        361: None
    }
    perspective_width_adjustments = {
        signs['טלה']: Degrees(0, 9),
        signs['שור']: Degrees(0, 10),
        signs['תאומים']: Degrees(0, 16),
        signs['סרטן']: Degrees(0, 27),
        signs['אריה']: Degrees(0, 38),
        signs['בתולה']: Degrees(0, 44),
        signs['מאזנים']: Degrees(0, 46),
        signs['עקרב']: Degrees(0, 45),
        signs['קשת']: Degrees(0, 44),
        signs['גדי']: Degrees(0, 36),
        signs['דלי']: Degrees(0, 24),
        signs['דגים']: Degrees(0, 12),
        361: None
    }
    lunar_twist = {
        signs['טלה'] + Degrees(0): -2/5,
        signs['טלה'] + Degrees(20): -1/3,
        signs['שור'] + Degrees(10): -1/4,
        signs['שור'] + Degrees(20): -1/5,
        signs['תאומים'] + Degrees(0): -1/6,
        signs['תאומים'] + Degrees(10): -1/6/2,
        signs['תאומים'] + Degrees(20): -1/6/4,
        signs['תאומים'] + Degrees(25): 0,
        signs['סרטן'] + Degrees(5): 1/6/4,
        signs['סרטן'] + Degrees(10): 1/6/2,
        signs['סרטן'] + Degrees(20): 1/6,
        signs['אריה'] + Degrees(0): 1/5,
        signs['אריה'] + Degrees(10): 1/4,
        signs['אריה'] + Degrees(20): 1/3,
        signs['בתולה'] + Degrees(10): 2/5,
        signs['מאזנים'] + Degrees(0): 2/5,
        signs['מאזנים'] + Degrees(20): 1/3,
        signs['עקרב'] + Degrees(10): 1/4,
        signs['עקרב'] + Degrees(20): 1/5,
        signs['קשת'] + Degrees(0): 1/6,
        signs['קשת'] + Degrees(10): 1/6/2,
        signs['קשת'] + Degrees(20): 1/6/4,
        signs['קשת'] + Degrees(25): 0,
        signs['גדי'] + Degrees(5): -1/6/4,
        signs['גדי'] + Degrees(10): -1/6/2,
        signs['גדי'] + Degrees(20): -1/6,
        signs['דלי'] + Degrees(0): -1/5,
        signs['דלי'] + Degrees(10): -1/4,
        signs['דלי'] + Degrees(20): -1/3,
        signs['דגים'] + Degrees(10): -2/5,
        361: None
    }
    final_length_adjustment = {
        signs['טלה']: 1/6,
        signs['שור']: 1/5,
        signs['תאומים']: 1/6,
        signs['סרטן']: 0,
        signs['אריה']: -1/5,
        signs['בתולה']: -1/3,
        signs['מאזנים']: -1/3,
        signs['עקרב']: -1/5,
        signs['קשת']: 0,
        signs['גדי']: 1/6,
        signs['דלי']: 1/5,
        signs['דגים']: 1/6,
        361: None
    }
    first_length = distance(date)
    if first_length < Degrees(0) or first_length > Degrees(180):
        if verbose:
            print('The moon is ahead of the sun')
        return Degrees()

    first_width = lunar_lattitude(date)
    #17:2
    current_lunar_position = lunar_position(date)
    #17:5
    second_length = first_length - find_by_range(
        current_lunar_position, perspective_length_adjustments)
    #17:7-9
    second_width = first_width - find_by_range(
        current_lunar_position, perspective_width_adjustments)
    #17:10
    lunar_curve = second_width * find_by_range(
        current_lunar_position, lunar_twist)
    #17:11
    third_length = second_length + lunar_curve
    #17:12
    final_length = third_length + third_length * find_by_range(
        midpoint(solar_position(date), current_lunar_position), 
        final_length_adjustment)
    correction_for_lattitude = 2/3 * first_width
    viewing_arc = final_length + correction_for_lattitude
    if verbose:
        #17:3 - 4
        print(result.format('first distance', str(first_length)))
        """if (current_lunar_position > signs['גדי'] 
        or  current_lunar_position < signs['סרטן']):
            if first_length < Degrees(9):
                print('The new moon will not be seen this night')
            elif first_length > Degrees(15):
                print('The new moon will be seen this night')
        elif signs['סרטן'] < current_lunar_position < signs['גדי']:
            if first_length < Degrees(10):
                print('The new moon will not be seen this night')
            elif first_length > Degrees(24):
                print('The new moon will be seen this night')
        """
        print(result.format('perspective distance', str(second_length)))
        print(sign_result.format(
            'perspective lattitude',
            ('N' if second_width > Degrees(0) else 'S'),
            str(abs(second_width))
        ))
        print(sign_result.format(
            'lunar curve',
            ('-' if lunar_curve < Degrees(0) else '+'),
            str(abs(lunar_curve))
        ))
        print(result.format('third distance', str(third_length)))
        print(result.format('fourth distance', str(final_length)))
        print(sign_result.format(
            'correction for lattitude', 
            ('-' if correction_for_lattitude < Degrees(0) else '+'),
            str(abs(correction_for_lattitude))
        ))
        print(result.format('viewing arc', str(viewing_arc)))
    return viewing_arc

def sighting(date: Day, verbose=False) -> bool:
    viewing_arc = annalisys(date)
    if viewing_arc < Degrees(9):
        sight = False
    elif viewing_arc > Degrees(14):
        sight = True
    else:
        sight = (viewing_arc + distance(date)) > Degrees(22)
    if verbose:
        print(f"The new moon will{'' if sight else ' not'} be seen this night")
    return sight

if __name__ == '__main__':
    #15:8-9
    wanted_day = Day(Month(start_year, 2), 2)
    assert(wanted_day.day_of_week == 6)
    assert(wanted_day.date - start_day.date == 29)
    print(f"\nDate: {wanted_day} ({wanted_day.day_of_week})")
    solar_position(wanted_day, verbose=True)
    print()
    lunar_position(wanted_day, verbose=True)
    print()
    #16:19
    lunar_lattitude(wanted_day, verbose=True)
    print()
    #17:13
    annalisys(wanted_day, verbose=True)
    print()
    #17:22
    sighting(wanted_day, verbose=True)