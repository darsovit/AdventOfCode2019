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
    state = {}
    state['slopes'] = set()
    state['front']  = {}
    state['back']   = {}
    for asteroid in field:
        if loc != asteroid:
            slope = calculateSlope( asteroid, loc )
            #print( 'visible slope:', slope, 'asteroid:', asteroid )
            if slope not in state['slopes']:
                state['slopes'].add(slope)
                state[slope] = list()
                key = None
                if slope[0] == 0 and slope[2] > 0:
                    key = 'front'
                elif slope[0] == 0:
                    assert( slope[2] < 0 )
                    key = 'back'
                if key:
                    state[key][slope[1]/slope[2]] = slope
            state[slope] += [ asteroid ]
    if len( state['front'] ):
        state['frontkeys'] = sorted(state['front'].keys())
    if len( state['back'] ):
        state['backkeys'] = sorted(state['back'].keys())
    return state

def calculateBestDetector( input ):
    field = buildField( input )
    bestCount = None
    bestLoc   = None
    for asteroid in field:
        state = getVisibleAsteroidSlopes( asteroid, field )
        count = len(state['slopes'])
        print( 'calculateBestDetector:', asteroid, count )
        if not bestCount or count > bestCount:
            bestCount = count
            bestLoc   = asteroid
    bestState = getVisibleAsteroidSlopes( asteroid, field )
    return (bestLoc,bestCount,bestState)


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

#def selectClosestAsteroid( loc, state, slope ):
    

def setupLaserInStateZero(state):
    zeroDegrees = (-1,0,0)
    if zeroDegrees in state['slopes']:
        state['laserAngle']['pos'] = zeroDegrees
        state['laserAngle']['state'] = 0
        return True
    return False

def setupLaserInStateOne(state):
    if len( state['frontkeys'] ) > 0:
        state['laserAngle']['pos'] = state['frontkeys'][0]
        state['laserAngle']['state'] = 1
        return True
    return False

def setupLaserInStateTwo(state):
    negZeroDegrees = (1,0,0)
    if negZeroDegrees in state['slopes']:
        state['laserAngle']['pos'] = negZeroDegrees
        state['laserAngle']['state'] = 2
        return True
    return False

def setupLaserInStateThree(state):
    if len(state['back']) > 0:
        state['laserAngle']['pos'] = state['backkeys'][0]
        state['laserAngle']['state'] = 3
        return True
    return False

def findNextInStateOne(state, slope):
    indexOfSlope = None
    #print( 'Slope: ', slope, 'Frontkeys:', state['frontkeys'] )
    for i in range(len(state['frontkeys'])):
        if state['front'][state['frontkeys'][i]] == slope:
            indexOfSlope = i
    assert( indexOfSlope != None )
    if indexOfSlope+1 >= len(state['frontkeys']):
        return False
    state['laserAngle']['pos'] = state['frontkeys'][indexOfSlope+1]
    if state['front'][state['frontkeys'][indexOfSlope]] not in state:
        print('No more entries of: ',slope,', removing', indexOfSlope, ' from frontkeys')
        del state['frontkeys'][ indexOfSlope ]
    #print('Next slope in state 1:', state['laserAngle']['pos'], state['front'][state['laserAngle']['pos']] )
    return True
        
def findNextInStateThree(state, slope):
    indexOfSlope = None
    for i in range(len(state['backkeys'])):
        if state['back'][state['backkeys'][i]] == slope:
            indexOfSlope = i
    assert( indexOfSlope != None )
    if indexOfSlope+1 >= len(state['backkeys']):
        return False
    state['laserAngle']['pos'] = state['backkeys'][indexOfSlope+1]
    if state['back'][state['backkeys'][indexOfSlope]] not in state:
        del state['backkeys'][indexOfSlope]
    return True
    
def findNextSlope( state, slope ):
    if state['laserAngle']['state'] == 0:
        return setupLaserInStateOne(state) or setupLaserInStateTwo(state) or setupLaserInStateThree(state)
    elif state['laserAngle']['state'] == 1:
        return findNextInStateOne(state,slope) or setupLaserInStateTwo(state) or setupLaserInStateThree(state) or setupLaserInStateZero(state)
    elif state['laserAngle']['state'] == 2:
        return setupLaserInStateThree(state) or setupLaserInStateZero(state) or setupLaserInStateOne(state)
    elif state['laserAngle']['state'] == 3:
        return findNextInStateThree(state,slope) or setupLaserInStateZero(state) or setupLaserInStateOne(state) or setupLaserInStateTwo(state)

def manhattanDistance( loc, asteroid ):
    return abs(asteroid[0]-loc[0])+abs(asteroid[1]-loc[1])

def selectAsteroid( loc, state, slope ):
    closestAsteroid = None
    distanceToClosest = None
    print( 'selectAsteroid: Asteroids at slope: ', slope, state[slope] )
    for asteroid in state[slope]:
        distanceToAsteroid = manhattanDistance( loc, asteroid )
        print( 'selectAsteroid: ', asteroid, ', distance:', distanceToAsteroid )
        if not distanceToClosest or distanceToAsteroid < distanceToClosest:
            distanceToClosest = distanceToAsteroid
            closestAsteroid   = asteroid
    return closestAsteroid
    
def selectAndDestroyAsteroid( loc, state ):
    asteroid = None
    currentState = state['laserAngle']['state']
    if 0 == state['laserAngle']['state'] or 2 == state['laserAngle']['state']:
        slope = state['laserAngle']['pos']
        asteroid = selectAsteroid( loc, state, slope )
        print("Removing asteroid at slope: ", asteroid, slope )
        if len( state[slope] ) > 1:
            state[slope].remove( asteroid )
        else:
            del state[ slope ]
        foundNextSlope = findNextSlope( state, slope )
    elif 1 == state['laserAngle']['state']:
        slope = state['front'][state['laserAngle']['pos']]
        asteroid = selectAsteroid( loc, state, slope )
        print("Removing asteroid at slope: ", asteroid, slope )
        if len( state[slope] ) > 1:
            state[slope].remove( asteroid )
        else:
            del state[ slope ]
        foundNextSlope = findNextSlope( state, slope )
    elif 3 == state['laserAngle']['state']:
        slope = state['back'][state['laserAngle']['pos']]
        asteroid = selectAsteroid( loc, state, slope )
        print("Removing asteroid at slope: ", asteroid, slope )
        if len( state[slope] ) > 1:
            state[slope].remove( asteroid )
        else:
            del state[ slope ]
        foundNextSlope = findNextSlope( state, slope )
    return ( asteroid, foundNextSlope )


def destroyAsteroids( loc, state, count ):
    print( loc )
    if 'laserAngle' not in state:
        state['laserAngle'] = {}
        foundNextSlope = setupLaserInStateZero(state) or setupLaserInStateOne(state) or setupLaserInStateTwo(state) or setupLaserInStateThree(state)
    destroyedAsteroids = list()
    for i in range( count ):
        (asteroid, foundNextSlope) = selectAndDestroyAsteroid( loc, state )
        if asteroid:
            destroyedAsteroids += [ asteroid ]
        if not foundNextSlope:
            break
    return destroyedAsteroids

if __name__ == '__main__':
    test()
    input = readInput()
    #(pos, uniqueSlopes, state) = calculateBestDetector( input )
    pos = (20, 18)
    state = getVisibleAsteroidSlopes( pos, buildField( input ) )
    #print( "Best Detector Loc:", pos, ", Num Unique Slopes:", uniqueSlopes )
    print( state )
    print( destroyAsteroids( pos, state, 200 ) )
    # -304 is not correct
    # 319 is too low; concern about coordinate system being flipped providing incorrect slopes for rotating algorithm