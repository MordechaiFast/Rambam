#!/usr/bin/env python
from flask import Flask
from flask import request
import sys; sys.path.append('../Rambam/')
from classes.calendarUnits import *

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


def printMonthsOfYear (year, printNextTishrei=False):
    """Prints all of the months of the given year, with their names, molad, and days of Rosh Chodesh."""
    aYear = Year(int(year))
    return_string = f"""<p>The year {aYear.years_from_creation} is cycle {
        aYear.cycles_to_year + 1} year {aYear.place_in_cycle}</p><p></p>"""
    return_string += "<table>"
    for thisMonth in aYear:
        Rosh_Chodesh = Day(thisMonth)
        if thisMonth.two_day_Rosh_Chodesh:
            if thisMonth.day_of_week == 1:
                return_string += f"""<tr><td>{thisMonth.name}</td>
                <td>{thisMonth.molad.days}</td><td>{thisMonth.molad.hours}</td>
                <td>{thisMonth.molad.parts}</td><td></td>
                <td>7 1</td></tr>"""
            else:
                return_string += f"""<tr><td>{thisMonth.name}</td>
                <td>{thisMonth.molad.days}</td><td>{thisMonth.molad.hours}</td>
                <td>{thisMonth.molad.parts}</td><td></td>
                <td>{Rosh_Chodesh.day_of_week - 1} {Rosh_Chodesh.day_of_week}</td>
                </tr>"""
        else:
            return_string += f"""<tr><td>{thisMonth.name}</td>
            <td>{thisMonth.molad.days}</td><td>{thisMonth.molad.hours}</td>
            <td>{thisMonth.molad.parts}</td></td><td>
            <td>{Rosh_Chodesh.day_of_week}</td></tr>"""
    if printNextTishrei:
        thisMonth = Month(aYear.year_after, 7)
        return_string += f"""<tr><td>{thisMonth.name}</td>
        <td>{thisMonth.molad.days}</td><td>{thisMonth.molad.hours}</td>
        <td>{thisMonth.molad.parts}</td></td><td>
        <td>{Rosh_Chodesh.day_of_week}</td></tr>"""
    return_string += "</table>"
    return return_string

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)