#! python
import math

def calcPrimeFactors( x ):
    factors = list()
    while ( x > 1 ):
        for i in range(2,x+1):
            if int( x / i ) * i == x:
                factors = factors + [i]
                x = int( x / i )
                break
    return factors

def calcGcd( x, y ):
    factorsForX = calcPrimeFactors( abs(x) )
    factorsForY = calcPrimeFactors( abs(y) )
    gcd = 1
    for factor in factorsForX:
        if factor in factorsForY:
            gcd *= factor
            factorsForY.remove( factor )
    return gcd

def calculateSlope( asteroid, loc ):
    rise = asteroid[1]-loc[1]
    run  = asteroid[0]-loc[0]
    if run == 0:
        return ( 1 if rise>0 else -1, 0, 0 )
    if rise == 0:
        return ( 0, 0, 1 if run>0 else -1 )
    gcd = calcGcd(rise,run)
    calculatedSlope = ( 0, int(rise/gcd), int(run/gcd) )
    if ( (0, 0, 0) == calculatedSlope ):
        print( 'asteroid:', asteroid, 'loc:', loc, 'rise:', rise, 'run:', run, 'commonFactors:', commonFactors, 'gcd:', gcd )
    assert( (0,0,0) != calculatedSlope)
    return calculatedSlope

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
            #print( 'visible slope:', slope, 'asteroid:', asteroid )
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

def test2Input():
    return ([ '......#.#.',
              '#..#.#....',
              '..#######.',
              '.#.#.###..',
              '.#..#.....',
              '..#....#.#',
              '#..#....#.',
              '.##.#..###',
              '##...#..#.',
              '.#....####' ], (5,8), 33)
'''
......#.#.
#..#.#....
..a#####c.
.f.#.###..
.b..#.....
..b....#.#
#..b....#.
.##.b..##d
##...A..#.
.#....##e#

{(0, -2, -1), a (2,2)
 (0, -1, -1), b (4,7),(3,6),(2,5),(1,4)
 (0, -2, 1),  c (8,2)
 (0, -1, 4),  d (9,7)
 (0, 1, 3),   e (8,9)
 (0, -5, -4), f (1,3)
 (0, -8, 3),
 (0, -5, 2),
 (0, 0, -1),
 (0, 0, 1),
 (0, -3, 2),
 (0, -1, -3),
 (0, -2, 3),
 (0, 1, -4),
 (0, -1, 3),
 (0, -7, -2),
 (0, -7, -5),
 (0, 1, 2),
 (0, -5, -2),
 (0, -5, 1),
 (0, 0, 0),   <-- This is problematic
 (0, -3, -1),
 (0, -3, 1),
 (0, -1, -4),
 (0, -3, 4),
 (0, -1, 2),
 (0, 1, 1),
 (0, 1, 4),
 (0, -8, 1),
 (0, -6, -1),
 (0, -6, 1),
 (-1, 0, 0),
 (0, -4, -1),
 (0, -2, -5)}
'''

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def test():
    assert( [3] == calcPrimeFactors( 3 ) )
    return
    assert( set([1,3]) == calcCommonFactors( 3, 3 ) )
    assert( set([1,2]) == calcCommonFactors( 2, 2 ) )
    assert( set([1])   == calcCommonFactors( -2, 1 ) )
    assert( set([1,2]) == calcCommonFactors( -2, -4 ) )
    (input,location,expected) = test1Input()
    field = buildField( input )
    assert (7 == len(getVisibleAsteroidSlopes( (1, 0), field ) ) )
    assert (7 == len(getVisibleAsteroidSlopes( (4, 0), field ) ) )
    assert (6 == len(getVisibleAsteroidSlopes( (0, 2), field ) ) )
    assert (7 == len(getVisibleAsteroidSlopes( (1, 2), field ) ) )
    assert (7 == len(getVisibleAsteroidSlopes( (2, 2), field ) ) )
    assert (7 == len(getVisibleAsteroidSlopes( (3, 2), field ) ) )
    assert (5 == len(getVisibleAsteroidSlopes( (4, 2), field ) ) )
    assert (7 == len(getVisibleAsteroidSlopes( (4, 3), field ) ) )
    assert (7 == len(getVisibleAsteroidSlopes( (4, 4), field ) ) )
    (found,detected) = calculateBestDetector(input)
    #print( found, detected )
    assert( (location,expected) == (found,detected) )
    
    (input, location, expected ) = test2Input()
    (found,detected) = calculateBestDetector(input)
    print( (found, detected ), 'vs', (location, expected) )
    field = buildField(input)
    print( getVisibleAsteroidSlopes( (5, 8), field ) )
    assert( (location, expected) == calculateBestDetector(input) )

if __name__ == '__main__':
    test()
    input = readInput()
    print( calculateBestDetector( input ) )
    # 282 is too high, curious because correct answer for others! oops