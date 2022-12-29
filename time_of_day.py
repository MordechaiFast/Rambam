from classes.degrees import Degrees

def time_of_degree(degs: Degrees):
    degs_in_day = Degrees(12, 9, 27)
    time = degs / degs_in_day
    hours = time * 24
    hour = int(hours)
    chalakim = int(hours % 1 * 1080)
    return hour, chalakim
