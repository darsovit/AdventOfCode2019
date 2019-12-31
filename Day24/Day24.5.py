#! python
#
# https://adventofcode.com/2019/day/24
#


class BugScan:
    def __init__(self, initialState):
        self.grid = {}
        self.grid[0] = set()
        for y in range(len(initialState)):
            for x in range(len(initialState[y])):
                if '#' == initialState[y][x]:
                    self.grid[0].add((x,y))

    def CalculateNextScan(self):
        #print('CalculateNextScan from:', self.grid)
        nextGrid = {}
        depths = sorted(self.grid.keys())
        assert len(depths) >= 1, 'Expected there to be at least one key to the depths = {}'.format(self.grid.keys())
        depth = depths[0]-1
        for pos in [(1,2),(3,2),(2,1),(2,3)]:
            if self.calcNextLoc(depth,pos):
                if depth not in nextGrid:
                    nextGrid[depth] = set()
                nextGrid[depth].add(pos)
        for depth in range(depths[0],depths[-1]+1):
            nextGrid[depth] = set()
            for y in range(5):
                for x in range(5):
                    if (x,y) != (2,2):
                        if self.calcNextLoc(depth,(x,y)):
                            nextGrid[depth].add((x,y))
        depth = depths[-1]+1
        for pos in [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(3,4),(2,4),(1,4)]:
            if self.calcNextLoc(depth,pos):
                if depth not in nextGrid:
                    nextGrid[depth] = set()
                nextGrid[depth].add(pos)
        self.grid = nextGrid

    def buildScanGrid(self, depth):
        lines = []
        for y in range(5):
            line = ''
            for x in range(5):
                if (2,2) == (x,y):
                    line += '?'
                else:
                    line += '#' if (x,y) in self.grid[depth] else '.'
            lines += [ line ]
        return '\n'.join(lines)

    def printScan(self):
        depths = sorted(self.grid.keys())
        for depth in depths:
            print( 'Depth:', depth )
            print( self.buildScanGrid(depth) )

    def CountBugs(self):
        numBugs = 0
        for depth in self.grid:
            numBugs += len(self.grid[depth])
        return numBugs

    def calcNeighbors(self, depth, pos):
        neighbors = set()
        for neighbor in [(1,0),(-1,0),(0,1),(0,-1)]:
            neighborPos = (pos[0]+neighbor[0],pos[1]+neighbor[1])
            if neighborPos == (2,2):
                # add neighbors from deeper level
                if depth+1 in self.grid:
                    if pos[0] == 1:
                        assert pos[1] == 2
                        for y in range(5):
                            neighbors.add((depth+1,(0,y)))
                    elif pos[0] == 3:
                        assert pos[1] == 2
                        for y in range(5):
                            neighbors.add((depth+1,(4,y)))
                    elif pos[1] == 1:
                        assert pos[0] == 2
                        for x in range(5):
                            neighbors.add((depth+1,(x,0)))
                    else:
                        assert pos == (2,3), 'Expected final of if...else test of pos to be (3,2), but it was {}'.format(pos)
                        for x in range(5):
                            neighbors.add((depth+1,(x,4)))
            elif neighborPos[0] == -1:
                # add neighbor from shallower level
                if depth-1 in self.grid:
                    neighbors.add((depth-1,(1,2)))
            elif neighborPos[0] == 5:
                # add neighbor from shallower level
                if depth-1 in self.grid:
                    neighbors.add((depth-1,(3,2)))
            elif neighborPos[1] == -1:
                # add neighbor from shallower level
                if depth-1 in self.grid:
                    neighbors.add((depth-1,(2,1)))
            elif neighborPos[1] == 5:
                # add neighbor from shallower level
                if depth-1 in self.grid:
                    neighbors.add((depth-1,(2,3)))
            else:
                neighbors.add((depth,neighborPos))
        return neighbors

    def calcNextLoc(self, depth, pos):
        numBugs = 0
        for neighbor in self.calcNeighbors(depth,pos):
            (testDepth,neighborPos) = neighbor
            if testDepth in self.grid:
                numBugs += 1 if neighborPos in self.grid[testDepth] else 0
        if depth in self.grid and pos in self.grid[depth]:
            if numBugs == 1:
                return True
        else:
            if numBugs >= 1 and numBugs <= 2:
                return True
        return False

def RunScenario(initialState,time):
    scan = BugScan(initialState)
    for i in range(time):
        scan.CalculateNextScan()
        #print('Step', i)
        #scan.printScan()
    return scan.CountBugs()

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))


def test1():
    #assert( 2129920 == biodiversity(['.....','.....','.....','#....','.#...']) )
    #assert( 2129920 == biodiversity(findFirstRepeat(['....#','#..#.','#..##','..#..','#....'])) )
    #NumBugsAfterScenario = RunScenario(['....#','#..#.','#..##','..#..','#....'],10)
    #assert 99 == NumBugsAfterScenario, 'Expected 99 bugs, calculated {} bugs'.format(NumBugsAfterScenario)
    pass

if __name__ == '__main__':
    test1()
    NumBugsAfterScenario = RunScenario(readInput(),200)
    print(NumBugsAfterScenario)
    # 957 is too low :(  -- Oops, requested after 100 minutes
