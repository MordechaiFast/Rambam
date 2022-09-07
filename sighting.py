from sre_compile import dis
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
    lower = round(lower)
    higher = round(higher)
    return (lower + higher) // 2


# 11:16
start_year = Year(4938)
assert(start_year.cycles_to_year == 259)
assert(start_year.place_in_cycle == 17)
start_month = Month(start_year, 1) #Nissan
start_day = Day(start_month, 3)
assert(start_day.day_of_week == 5)

# 12:1
solar_progresion_100_delta = DegreesOfCircle(98, 33, 53)
solar_progresion_delta = solar_progresion_100_delta /10/10
assert(solar_progresion_delta        == Degrees(  0, 59,  8))
assert(solar_progresion_delta *10    == Degrees(  9, 51, 23))
assert(solar_progresion_delta *1000  == Degrees(265, 38, 50))
assert(solar_progresion_delta *10000 == Degrees(136, 28, 20))

#print(*reversed("מהלך השמש האמצעי"), sep='')
#for n in (*range(1, 10), *range(10, 100, 10), *range(100, 1000, 100),
#          *range(1000, 11000, 1000)):
#    print(f"{n:>5}: {solar_progresion_delta * n:>10s}")
solar_progresion_29_delta = solar_progresion_delta * 29
assert(solar_progresion_29_delta == Degrees(28, 35, 1))
solar_progresion_354_delta = solar_progresion_delta * 354
assert(solar_progresion_354_delta == Degrees(348, 55, 9))

# 12:2
solar_hight_100_delta = DegreesOfCircle(0, 0, 15)
solar_hight_delta = solar_hight_100_delta /10/10
assert(solar_hight_delta * 10    == Degrees(0, 0, 1, 30))
assert(solar_hight_delta * 1000  == Degrees(0, 2, 30))
assert(solar_hight_delta * 10000 == Degrees(0, 25))
solar_hight_29_delta = solar_hight_delta * 29
assert(solar_hight_29_delta == Degrees(0, 0, 4))
solar_hight_354_delta = solar_hight_delta * 354
assert(solar_hight_354_delta == Degrees(0, 0, 53))

solar_progresion_start = signs['טלה'] + Degrees(7, 3, 32)
solar_hight_start = signs['תאומים'] + Degrees(26, 45, 8)

wanted_day = Day(Month(start_year, 4), 14)
assert(wanted_day.day_of_week == 7)
delta = wanted_day.date - start_day.date
assert(delta == 100)

#wanted_day = Day(Month(Year(5782), 5), 21)
#delta = wanted_day.date - start_day.date

print(f"Date: {wanted_day} ({wanted_day.day_of_week})")
current_solar_progresion = solar_progresion_start + solar_progresion_delta * delta
print("solar progresion", current_solar_progresion)
current_solar_hight = solar_hight_start + solar_hight_delta * delta
print("solar hight", current_solar_hight)

# 13:1
solar_track = current_solar_progresion - current_solar_hight

# 13:4
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

def tracking_delta(track: Degrees, tracking: dict) -> Degrees:
    track = round(track)
    # 13:2
    if track < 180:
        sign = -1
    elif track == 180:
        return Degrees()
    else:
        track = 360 - track
        sign = 1
    # 13:7
    upper_track = tracking[track // 10 * 10 + 10]
    lower_track = tracking[track // 10 * 10]
    track_average = (upper_track - lower_track) / 10
    return sign * (lower_track + track_average * (track % 10))

solar_tracking_delta = tracking_delta(solar_track, solar_tracking)

# 13:2
true_solar_position = current_solar_progresion + solar_tracking_delta

# 13:9
print("solar track distance", solar_track)
print("solar track delta", solar_tracking_delta)
print("solar position", true_solar_position)

# The date of a lunar sighting, from 15:8
wanted_day = Day(Month(start_year, 2), 2)
delta = wanted_day.date - start_day.date
current_solar_progresion = solar_progresion_start + (
    solar_progresion_delta * delta)

# 14:1-2
lunar_progresion_100_delta = Degrees(1317, 38, 23)
lunar_progresion_delta = DegreesOfCircle(*(lunar_progresion_100_delta /10/10))
assert(lunar_progresion_delta        == Degrees( 13, 10, 35))
assert(lunar_progresion_delta *10    == Degrees(131, 45, 50))
assert(lunar_progresion_delta *100   == Degrees(237, 38, 23))
assert(lunar_progresion_delta *1000  == Degrees(216, 23, 50))
assert(lunar_progresion_delta *10000 == Degrees(  3, 58, 20))
lunar_progresion_29_delta = lunar_progresion_delta * 29
assert(lunar_progresion_29_delta == Degrees(22, 6, 56))
lunar_progresion_354_delta = lunar_progresion_delta * 354
assert(lunar_progresion_354_delta == Degrees(344, 26, 41))

#14:3-4
lunar_track_progresion_100_delta = Degrees(1306, 29, 53)
lunar_track_progresion_delta = DegreesOfCircle(
    *(lunar_track_progresion_100_delta /10/10))
assert(lunar_track_progresion_delta        == Degrees( 13,  3, 54))
assert(lunar_track_progresion_delta *10    == Degrees(130, 38, 59))
assert(lunar_track_progresion_delta *100   == Degrees(226, 29, 53))
assert(lunar_track_progresion_delta *1000  == Degrees(104, 58, 50))
assert(lunar_track_progresion_delta *10000 == Degrees(329, 48, 20))
lunar_track_progresion_29_delta = lunar_track_progresion_delta * 29
assert(lunar_track_progresion_29_delta == Degrees(18, 53, 4))
lunar_track_progresion_354_delta = lunar_track_progresion_delta * 354
assert(lunar_track_progresion_354_delta == Degrees(305, 0, 11))

#14:4
lunar_progresion_start = signs['שור'] + Degrees(1, 14, 43)
lunar_track_start = Degrees(84, 28, 42)

current_lunar_progresion = lunar_progresion_start + (
    lunar_progresion_delta * delta)

#14:5
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
    360: None
}

def find_by_range(place: Degrees, table: dict) -> Degrees:
    reference = round(place)
    lower_bound = None
    for bound in table:
        if reference < bound:
            break
        else:
            lower_bound = bound
    if lower_bound is None or table[round(lower_bound)] is None:
        raise ValueError(f'{place} is out of range')
    else:
        return table[round(lower_bound)]
    
#14:6
timed_lunar_progresion = current_lunar_progresion + find_by_range(
    current_solar_progresion, seasonal_adjustments)

#15:1
current_lunar_track_progresion = lunar_track_start + (
    lunar_track_progresion_delta * delta)

double_distance = (current_lunar_progresion - current_solar_progresion) * 2

#15:3
tracking_correction ={
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

corrected_lunar_track = current_lunar_track_progresion + find_by_range(
    double_distance, tracking_correction)

#15:6
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

#15:4
true_lunar_position = timed_lunar_progresion + tracking_delta(
    corrected_lunar_track, lunar_tracking)

#15:8
wanted_day = Day(Month(start_year, 2), 2)
assert(wanted_day.day_of_week == 6)
delta = wanted_day.date - start_day.date
assert(delta == 29)
print(f"\nDate: {wanted_day} ({wanted_day.day_of_week})")
current_solar_progresion = solar_progresion_start + (
    solar_progresion_delta * delta)
print(f"{'solar progresion':22} {str(current_solar_progresion):>10}")
current_solar_hight = solar_hight_start + solar_hight_delta * delta
print(f"{'solar hight':22} {str(current_solar_hight):>10}")
solar_track = current_solar_progresion - current_solar_hight
print(f"{'solar track distance':22} {str(solar_track):>10}")
solar_tracking_delta = tracking_delta(solar_track, solar_tracking)
print(f"{'solar track delta':22} {str(solar_tracking_delta):>10}")
true_solar_position = current_solar_progresion + solar_tracking_delta
print(f"{'true solar position':22} {str(true_solar_position):>10}")
current_lunar_progresion = lunar_progresion_start + (
    lunar_progresion_delta * delta)
print(f"{'lunar progresion':22} {str(current_lunar_progresion):>10}")
current_lunar_track_progresion = lunar_track_start + (
    lunar_track_progresion_delta * delta)
print(f"{'lunar track progresion':22} {str(current_lunar_track_progresion):>10}")
timed_lunar_progresion = current_lunar_progresion + find_by_range(
    current_solar_progresion, seasonal_adjustments)
print(f"{'timed lunar progresion':22} {str(timed_lunar_progresion):>10}")
distance = current_lunar_progresion - current_solar_progresion
print(f"{'distance':22} {str(distance):>10}")
double_distance = distance * 2
print(f"{'double distance':22} {str(double_distance):>10}")
corrected_lunar_track = current_lunar_track_progresion + find_by_range(
    double_distance, tracking_correction)
print(f"{'corrected lunar track':22} {str(corrected_lunar_track):>10}")
true_lunar_position = timed_lunar_progresion + tracking_delta(
    corrected_lunar_track, lunar_tracking)
print(f"{'true lunar position':22} {str(true_lunar_position):>10}")