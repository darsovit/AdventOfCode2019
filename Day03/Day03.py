#! python

def buildTrack( grid, origin, path, wire ):
    segments = path.split(',')
    loc = origin
    for segment in segments:
        (direction,distance) = (segment[0], int(segment[1:]))
        if direction == 'R':
            movefunc = lambda x: (x[0]+1, x[1])
        elif direction == 'L':
            movefunc = lambda x: (x[0]-1, x[1])
        elif direction == 'U':
            movefunc = lambda x: (x[0], x[1]+1)
        elif direction == 'D':
            movefunc = lambda x: (x[0], x[1]-1)
    
        for i in range(0,distance):
            newloc = movefunc(loc)
            if newloc not in grid:
                grid[newloc] = wire
            else:
                grid[newloc] += wire
            loc = newloc
    #print( grid )

def calcManhattanDistanceToOrigin( loc ):
    return abs(loc[0]) + abs(loc[1])

def findClosestIntersection( instructions ):
    grid = {}
    buildTrack( grid, (0,0), instructions[0], 1 )
    buildTrack( grid, (0,0), instructions[1], 2 )
    closestLoc = None
    closestDistance = None
    for loc in grid:
        if grid[loc] == 3 and ( not closestDistance or closestDistance > calcManhattanDistanceToOrigin( loc ) ):
            closestLoc = loc
            closestDistance = calcManhattanDistanceToOrigin( loc )
    return closestLoc

def test():
    assert( (3,3) == findClosestIntersection( ['R8,U5,L5,D3', 'U7,R6,D4,L4'] ) )
    assert( 159 == calcManhattanDistanceToOrigin( findClosestIntersection( ['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83' ] ) ) )
    assert( 135 == calcManhattanDistanceToOrigin( findClosestIntersection( ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51','U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'])))
test()

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))
        
print( calcManhattanDistanceToOrigin( findClosestIntersection( readInput() ) ) )