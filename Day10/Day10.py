#! python
import math

def calcFactors( x ):
    factors = set()
    for i in range(1,x+1):
        if int(x / i) * i == x:
            factors.add(i)
    return factors

def calcCommonFactors( x, y ):
    factorsForX = calcFactors( abs(x) )
    factorsForY = calcFactors( abs(y) )
    return factorsForX.intersection( factorsForY )

def calculateSlope( asteroid, loc ):
    rise = asteroid[1]-loc[1]
    run  = asteroid[0]-loc[0]
    if run == 0:
        return ( 1 if rise>0 else -1, 0, 0 )
    if rise == 0:
        return ( 0, 0, 1 if rise>0 else -1 )
    commonFactors = calcCommonFactors(rise,run)
    gcd = 1
    for factor in commonFactors:
        gcd *= factor
    return ( 0, int(rise / gcd), int(run / gcd) )

def buildField( input ):
    field = set()
    width = None
    for y in range( len(input) ):
        if not width:
            width = len(input[y])
        assert( width == len(input[y]) )
        for x in range( len(input[y]) ):
            if input[y][x] == '#':
                field.add( (x,y) )
    return field

def getVisibleAsteroidSlopes( loc, field ):
    slopes = set()
    for asteroid in field:
        if loc != asteroid:
            slope = calculateSlope( asteroid, loc )
            slopes.add(slope)
    return slopes

def calculateBestDetector( input ):
    field = buildField( input )
    bestCount = None
    bestLoc   = None
    for asteroid in field:
        slopes = getVisibleAsteroidSlopes( asteroid, field )
        count = len(slopes)
        if not bestCount or count > bestCount:
            bestCount = count
            bestLoc   = asteroid
    return (bestLoc,bestCount)

def test1Input():
    return ([ '.#..#',
              '.....',
              '#####',
              '....#',
              '...##' ], (3,4), 8)

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def test():
    assert( set([1,3]) == calcFactors( 3 ) )
    assert( set([1,3]) == calcCommonFactors( 3, 3 ) )
    assert( set([1,2]) == calcCommonFactors( 2, 2 ) )
    assert( set([1])   == calcCommonFactors( -2, 1 ) )
    assert( set([1,2]) == calcCommonFactors( -2, -4 ) )
    (input,location,expected) = test1Input()
    (found,detected) = calculateBestDetector(input)
    #print( found, detected )
    assert( (location,expected) == (found,detected) )

if __name__ == '__main__':
    test()
    input = readInput()
    print( calculateBestDetector( input ) )
    # 282 is too high, curious because correct answer for others! oops