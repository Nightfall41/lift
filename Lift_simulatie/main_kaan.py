from SimPyLC import World
from elevator import Elevator, Plotter
from controller import MainController



aantal_liften = (input("Hoeveel liften?")) # bijv 5 liften? tik dit in als 0 1 2 3 4
lijst = list(map(int, aantal_liften.split()))


print("voer alleen integers in.")
print()
lijst_van_lift_objecten=[]
for x in range(len(lijst)):
    floors=int(input("hoeveel vloeren heeft lift {} ?".format(x)))
    print()
    floorheight=int(input("hoogste verdieping die lift {} kan gaan ?".format(x)))
    print()
    expressLift=bool(input("is lift {} een express lift? voer 0 of 1 in. ".format(x)))
    print()
    globals() ['elevator_'+str(x)]= lijst_van_lift_objecten.append(Elevator(x,floors,floorheight,expressLift))

"""
bro hierboven zie je dat er liften worden gemaakt en deze objecten worden in een lijst gegeooit 
maak nu die maincontroller dynamisch dan werkt die rotzooi broer
"""


m = MainController(lijst_van_lift_objecten)

World(lambda x: lijst_van_lift_objecten, m)
