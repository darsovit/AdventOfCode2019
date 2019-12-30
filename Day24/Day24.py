#! python
#
# https://adventofcode.com/2019/day/24
#

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))


def CountBug(grid, pos):
    if len(grid) > pos[1] and 0 <= pos[1] and len(grid[0]) > pos[0] and 0 <= pos[0]:
        return 1 if '#' == grid[pos[1]][pos[0]] else 0
    else:
        return 0

def getNumAdjacentBugs(grid,pos):
    numBugs = 0
    for neighbor in [(1,0),(-1,0),(0,1),(0,-1)]:
        numBugs += CountBug(grid, (pos[0]+neighbor[0],pos[1]+neighbor[1]))
    return numBugs

def calcNextLoc(grid,pos):
    numAdjacentBugs = getNumAdjacentBugs(grid,pos)
    if grid[pos[1]][pos[0]] == '#':
        return '#' if numAdjacentBugs == 1 else '.'
    elif numAdjacentBugs >= 1 and numAdjacentBugs <= 2:
        return '#'
    else:
        return '.'

def calcNextGrid(grid):
    nextGrid = []
    for y in range(5):
        nextLine = ''
        for x in range(5):
            nextLine += calcNextLoc(grid,(x,y))
        nextGrid += [ nextLine ]
    return nextGrid

def biodiversity(grid):
    flatgrid = ''.join(grid)
    sum = 0
    for i in range(len(flatgrid)):
        if flatgrid[i] == '#':
            sum += (1<<i)
    return sum

def findFirstRepeat(grid):
    firstRepeatTile = None
    numSteps = 0
    possibilities = {}
    possibilities[biodiversity(grid)] = numSteps
    while not firstRepeatTile:
        numSteps += 1
        grid = calcNextGrid(grid)
        val = biodiversity(grid)
        if val in possibilities:
            firstRepeatTile = grid
        else:
            possibilities[val] = numSteps
    return grid

def test1():
    assert( 2129920 == biodiversity(['.....','.....','.....','#....','.#...']) )
    assert( 2129920 == biodiversity(findFirstRepeat(['....#','#..#.','#..##','..#..','#....'])) )

if __name__ == '__main__':
    test1()
    repeatedGrid = findFirstRepeat(readInput())
    print(repeatedGrid)
    print(biodiversity(repeatedGrid))