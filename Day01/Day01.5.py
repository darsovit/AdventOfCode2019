#! python

def calcFuel(mass):
    fuel = int(mass / 3) - 2
    return 0 if (fuel < 0) else fuel
    #return -2

def calcAllFuel(module):
    fuel = calcFuel(module)
    additionalFuel = calcFuel( fuel )
    while ( 0 < additionalFuel ):
        newAdditionalFuel = calcFuel( additionalFuel )
        fuel += additionalFuel
        additionalFuel = newAdditionalFuel
    return fuel
    
def test():
    assert( 0 == calcAllFuel(0) )
    assert( 0 == calcAllFuel(3) )
    assert( 2 == calcAllFuel(12) )
    assert( 2 == calcAllFuel(14) )
    assert( 966 == calcAllFuel(1969) )
    assert( 50346 == calcAllFuel(100756) )
    
def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

test()
input = readInput()
# 4893493 is too high
#
# This is tricky, because the instructions are to calculate fuel for all'
# modules before summing together
fuel = sum([ calcAllFuel(int(mass)) for mass in input ])
print( fuel )


