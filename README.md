# Calculating-programs

(Should be called Rambam)

My first project, and my most intensive. This project actually needs to do something useful. Most of my projects are basically proof of concept for various python features.

The main function of this project is to do the heavy calculation of when the moon will be visable after sunset as described in the Ramabam, Hilchos Kiddush Hachodesh, chapters 6-19. There is a lot of repetetive addition and multiplication, and working with times given in days hours and parts, dealling with circular positions; calculation of an absolute date; interpolations, and other tedious math. A great project to apply a computer to. This makes it possible to quickly compare many dates, and opens the door for other unexpected applications.

I used this as an avenue to get my feet wet with OOP. The basic calculations lend themselves to classes. The need to optomize lead me to cacheing and the beginings of multiple constructors. I realized that there was a good place for proper inheritance and ABCs. Some of the functions began to form an interface.

The need to be able to acces the calculator brought me to making a CLI. I tried with a tinker interface and Flask website, but have not yet gotten to anything worthy.

While working on the internal logic, which is based heavily on the text of the Rambam, following it more than would be neccessary for the calculaitons themselves, I make much of the logic of the code in a set of Jupyter notebooks.
