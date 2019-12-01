#! python

def calcFuel(mass):
    return int(mass / 3) - 2
    #return -2

def test():
    assert( -2 == calcFuel(0) )
    assert( -1 == calcFuel(3) )
    assert( 2 == calcFuel(12) )
    assert( 2 == calcFuel(14) )
    assert( 654 == calcFuel(1969) )
    assert( 33583 == calcFuel(100756) )

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

test()
input = readInput()
print( sum( [ calcFuel(int(mass)) for mass in input ] ) )
