from flask import Flask
from flask import request
from calendarUnits import *

app = Flask(__name__)

@app.route("/")
def index():
    year_number = request.args.get("year", "")
    if year_number:
        table = printMonthsOfYear(year_number)
    else:
        table = ""
    return """<form action="" method="get">
                Year: <input type="text" name="year">
                <input type="submit" value="Create table">
              </form>""" + table


def printMonthsOfYear (year, printNextTishrei = False):
    """Prints all of the months of the given year, with their names, molad, and days of Rosh Chodesh."""
    return_string = "<font=mono>"
    aYear = Year(int(year))
    return_string += "<p>The year " + str(aYear.yearsFromCreation) + " is cycle " + str(aYear.cyclesToYear + 1) + " year " + str(aYear.placeInCycle) + "</p><p></p>"
    for thisMonth in aYear:
        if thisMonth.two_day_Rosh_Chodesh():
            if thisMonth.day_of_week() == 1:
                return_string += "<p>" + thisMonth.name + "<t>" + str(thisMonth.molad) + "<t>" + "7 1</p>"
            else:
                return_string += "<p>" + thisMonth.name + "<t>" + str(thisMonth.molad) + "<t>" + str(thisMonth.day_of_week() - 1) + " " + str(thisMonth.day_of_week()) + "</p>"
        else:
            return_string += "<p>" + thisMonth.name + "<t>" + str(thisMonth.molad) + "<t>" + str(thisMonth.day_of_week()) + "</p>"
    if printNextTishrei:
        thisMonth = Month(aYear.yearAfter(), 7)
        return_string += "<p>" + thisMonth.name + "<t>" + str(thisMonth.molad) + "<t>" + str(thisMonth.day_of_week()) + "</p>"
    return return_string

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)