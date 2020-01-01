#! python
#
# http://adventofcode.com/2019/day/15
#

import Intcode
import click

class Input:
    def __init__(self):
        self.calibrate()

    def SetOutput( self, mapOutput ):
        self.mapOutput = mapOutput

    def calibrate(self):
        print('Calibrate by pressing left arrow:')
        self.west = click.getchar()
        print('Calibrate by pressing right arrow:')
        self.east = click.getchar()
        print('Calibrate by pressing up arrow:')
        self.north = click.getchar()
        print('Calibrate by pressing down arrow:')
        self.south = click.getchar()
        print('Calibration complete, press enter:')
        self.done  = click.getchar()

    def readInput(self):
        valid = False
        while not valid:
            self.dir = click.getchar()
            if self.dir == self.north:
                return 1
            if self.dir == self.south:
                return 2
            if self.dir == self.east:
                return 4
            if self.dir == self.west:
                return 3
            if self.dir == self.done:
                valid = self.mapOutput.ValidateAndCalculateOxygenFill()
                if not valid:
                    print('Haven\'t found all locations, keep exploring')
        return None

    def lastDirection(self):
        if self.dir == self.north:
            return (0,1)
        if self.dir == self.south:
            return (0,-1)
        if self.dir == self.east:
            return (1,0)
        if self.dir == self.west:
            return (-1,0)

class MapOutput:
    def __init__(self, input):
        self.map = {}
        self.input = input
        self.pos = (0,0)
        self.distance = {}
        self.distance[self.pos] = 0
        self.map[self.pos] = '.'
        self.walkables = [(0,0)]
        self.oxygenPos = None
        self.minX = None
        self.maxX = None
        self.minY = None
        self.maxY = None

    def HandleOutput(self, val):
        attemptedDirection = self.input.lastDirection()
        if val == 0:
            self.AddWall( attemptedDirection )
        elif val == 1:
            self.MovePos( attemptedDirection )
        elif val == 2:
            self.MovePos( attemptedDirection )
            self.map[self.pos] = 'O'
            self.oxygenPos = self.pos
        self.Render()

    def MovePos( self, delta ):
        distance = self.distance[self.pos]
        self.pos = MapOutput.AddPos( self.pos, delta )
        self.map[self.pos] = '.'
        self.walkables += [self.pos]
        if self.pos not in self.distance or (self.distance[self.pos] > distance+1):
            self.distance[self.pos] = distance+1

    def AddPos( pos1, pos2 ):
        return ( pos1[0]+pos2[0], pos1[1]+pos2[1] )

    def AddWall( self, delta ):
        self.map[MapOutput.AddPos(self.pos,delta)] = '#'

    def Render( self ):
        lines = []
        for y in range( self.pos[1]+10, self.pos[1]-10, -1):
            line = ''
            for x in range( self.pos[0]-10, self.pos[0]+10, 1):
                line += self.GetMap( (x,y) )
            lines += [ line ]
        print("\n\n\n")
        print( '\n'.join(lines) )
        print( 'Distance:', self.distance[self.pos] )

    def GetMap( self, pos ):
        if pos == self.oxygenPos and pos == self.pos:
            return 'X'
        if pos == self.pos:
            return 'D'
        if pos in self.map:
            return self.map[pos]
        return ' '
    
    def AllNeighborsFound(self, pos):
        neighbors = [(1,0),(-1,0),(0,1),(0,-1)]
        found = True
        for neighbor in neighbors:
            found = found and ' ' != self.GetMap( MapOutput.AddPos( pos, neighbor ) )
        return found

    def Validate(self):
        for walkable in self.walkables:
            if not self.AllNeighborsFound(walkable):
                return False
        return True

    def CalculateOxygenFill(self):
        posMap = self.map.copy()
        addedOxygen = [self.oxygenPos]
        round       = 0
        posMap[self.oxygenPos] = 'O'
        neighbors = [(1,0),(-1,0),(0,1),(0,-1)]
        while len(addedOxygen) > 0:
            lastOxygen = addedOxygen.copy()
            addedOxygen = []
            round += 1
            for oxygen in lastOxygen:
                for neighbor in neighbors:
                    possiblePos = MapOutput.AddPos( oxygen, neighbor )
                    if posMap[possiblePos] == '.':
                        posMap[possiblePos] = 'O'
                        addedOxygen += [possiblePos]
        print("Took {} rounds to fill the space with Oxygen".format( round - 1 ))

    def ValidateAndCalculateOxygenFill(self):
        if not self.Validate():
            return False
        self.CalculateOxygenFill()
        return True
class RobotIO:
    def __init__(self):
        self.state = {}
        print('Calibrate the RobotIO by hitting enter:', end='')
        self.done  = click.getchar()
        print(self.done)
        
    def handleOutput(self, val):
        print(chr(val), end='')
    
    def handleInput(self):
        charval = click.getchar()
        if charval == self.done:
            print(self.done)
            return 10
        
        print(charval, end='')
        return ord(charval)


if __name__ == '__main__':
    io = RobotIO()
    #input = Input()
    
    #mapOutput = MapOutput( input )
    #input.SetOutput( mapOutput )
    prog = Intcode.Intcode( Intcode.readProgInput('input.txt'), inputFunc=io.handleInput, outputFunc=io.handleOutput )
    #mapOutput.Render()
    prog.Run()