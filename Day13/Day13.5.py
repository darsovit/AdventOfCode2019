#! python

import Intcode
import time

class Screen:
    def __init__(self):
        self.screen = {}
        self.inputGather = []
        self.maxY = None
        self.maxX = None
        self.ballX = None
        self.paddleX = None
        self.score = 0

    def addElement( self, pos, type ):
        if pos[0] == -1 and pos[1] == 0:
            self.score = type
        else:
            if pos[1] not in self.screen.keys():
                self.screen[pos[1]] = {}
            self.screen[pos[1]][pos[0]] = type
            if not self.maxX or self.maxX < pos[0]:
                self.maxX = pos[0]
            if not self.maxY or self.maxY < pos[1]:
                self.maxY = pos[1]
        if type == 4:
            self.ballX = pos[0]
        if type == 3:
            self.paddleX = pos[0]
        
    def input( self, val ):
        self.inputGather += [ val ]
        if len(self.inputGather) == 3:
            self.addElement( (self.inputGather[0], self.inputGather[1]), self.inputGather[2] )
            self.inputGather = []

    def getInput( self ):
        #input("Press Enter to continue...")
        self.render()
        time.sleep(.05)
        if self.paddleX > self.ballX:
            return -1
        elif self.paddleX < self.ballX:
            return 1
        return 0

    def getItem( val ):
        if 0 == val:
            return ' '
        if 1 == val:
            return '#'
        if 2 == val:
            return 'X'
        if 3 == val:
            return '-'
        if 4 == val:
            return 'o'
        return None

    def renderLine( self, y ):
        if y not in self.screen:
            return ''
        
        line = ''
        for x in range( self.maxX + 1):
            if x in self.screen[y]:
                line += Screen.getItem( self.screen[y][x] )
        return line

    def render(self):
        print( "\n\n\n\nScore: {}\nSCREEN:".format( self.score ) )
        lines = []
        for y in range(self.maxY+1):
           lines += [self.renderLine(y)]
        print('\n'.join(lines))
        
    def countObjects(self):
        numWalls = 0
        numBlocks = 0
        numHorizontalPaddle = 0
        numBall = 0
        numEmpty = 0
        for y in self.screen:
            for x in self.screen[y]:
                val = self.screen[y][x]
                if 0 == val:
                    numEmpty += 1
                elif 1 == val:
                    numWalls += 1
                elif 2 == val:
                    numBlocks += 1
                elif 3 == val:
                    numHorizontalPaddle += 1
                elif 4 == val:
                    numBall += 1
        print( numEmpty, numWalls, numBlocks, numHorizontalPaddle, numBall )


if __name__ == '__main__':
    myscreen = Screen()
    code = Intcode.readProgInput('input.txt')
    code[0] = 2
    game = Intcode.Intcode( code, inputFunc=myscreen.getInput, outputFunc=myscreen.input )
    game.Run()
    myscreen.render()
    myscreen.countObjects()