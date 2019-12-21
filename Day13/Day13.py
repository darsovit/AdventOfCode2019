#! python

import Intcode

class Screen:
    def __init__(self):
        self.screen = {}
        self.inputGather = []

    def addElement( self, pos, type ):
        if pos[0] not in self.screen.keys():
            self.screen[pos[0]] = {}
        self.screen[pos[0]][pos[1]] = type
        
        
    def input( self, val ):
        self.inputGather += [ val ]
        if len(self.inputGather) == 3:
            self.addElement( (self.inputGather[0], self.inputGather[1]), self.inputGather[2] )
            self.inputGather = []

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
    game = Intcode.Intcode( Intcode.readProgInput( 'input.txt'), outputFunc=myscreen.input )
    game.Run()
    myscreen.countObjects()