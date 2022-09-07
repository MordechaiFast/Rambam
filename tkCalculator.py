import tkinter as tk
from tkinter.font import Font
from classes.calendarUnits import Month, Year

window = tk.Tk()
window.title("Rambam calculator")

input_frm = tk.Frame()
input_title = tk.Label(master=input_frm, text='Year:')
input_title.grid(row=0, column=0, sticky='e')
input_ent = tk.Entry(master=input_frm)
input_ent.grid(row=0, column=1, sticky='w')
input_frm.grid(row=0)

output_lbl = tk.Label(font=Font(font='monospace'), justify='left', text='')
output_lbl.grid(row=1)

def calculate(event):
    if event.char == '\r':
        output_lbl['text'] = ''
        aYear = Year(int(input_ent.get()))
        for thisMonth in aYear:
            if thisMonth.two_day_Rosh_Chodesh():
                if thisMonth.day_of_week() == 1:
                    output_lbl['text'] += f'{thisMonth.name} \t {thisMonth.molad} \t 7 1\n'
                else:
                    output_lbl['text'] += (f'{thisMonth.name} \t {thisMonth.molad} \t '
                    f'{thisMonth.day_of_week() - 1} {thisMonth.day_of_week()}\n')
            else:
                output_lbl['text'] += f'{thisMonth.name} \t {thisMonth.molad} \t {thisMonth.day_of_week()}\n '
        thisMonth = Month(aYear.year_after(), 7)
        output_lbl['text'] += f'{thisMonth.name} \t {thisMonth.molad} \t {thisMonth.day_of_week()}\n'

window.bind('<Key>', func=calculate)

window.mainloop()