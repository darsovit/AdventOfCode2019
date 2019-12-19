#! python

import Intcode

class PaintingRobot:
    def __init__(self, prog):
        self.state = {}
        self.pos = (0,0)
        self.dir = 'U'
        self.panels = {}
        self.outputs = [ self.paintLoc, self.turn ]
        self.outputcount = 0
        self.io = []
        self.prog = prog
        self.comp = Intcode.Intcode( self.prog, inputFunc=self.readCurrentPanel, outputFunc=self.handleOutput )
        
    def readCurrentPanel(self):
        if self.pos in self.panels:
            self.io += [('input',self.pos,self.panels[self.pos])]
            return self.panels[self.pos]
        else:
            self.io += [('input',self.pos,'.')]
            return 0

    def handleOutput(self, val):
        func = self.outputs[self.outputcount%2]
        func(val)
        self.outputcount += 1

    def paintLoc(self, val):
        self.panels[self.pos] = val
        self.io += [('output-paint',self.pos,self.panels[self.pos])]
    
    def turnLeft(self):
        if 'U' == self.dir:
            self.dir = 'L'
        elif 'L' == self.dir:
            self.dir = 'D'
        elif 'D' == self.dir:
            self.dir = 'R'
        elif 'R' == self.dir:
            self.dir = 'U'

    def turnRight(self):
        if 'U' == self.dir:
            self.dir = 'R'
        elif 'R' == self.dir:
            self.dir = 'D'
        elif 'D' == self.dir:
            self.dir = 'L'
        elif 'L' == self.dir:
            self.dir = 'U'

    def moveForward(self):
        if 'U' == self.dir:
            self.pos = (self.pos[0], self.pos[1]+1)
        elif 'D' == self.dir:
            self.pos = (self.pos[0], self.pos[1]-1)
        elif 'L' == self.dir:
            self.pos = (self.pos[0]-1, self.pos[1])
        elif 'R' == self.dir:
            self.pos = (self.pos[0]+1, self.pos[1])

    def turn(self, val):
        if val == 0:
            self.turnLeft()
        elif val == 1:
            self.turnRight()
        self.moveForward()
        self.io += [('output-turn',self.pos,val)]
    
    def Run(self):
        self.comp.Run()

    def DebugStats(self):
        print(len(self.panels))
        #print(self.io)
        
if __name__ == '__main__':
    robot = PaintingRobot(Intcode.readProgInput('input.txt'))
    robot.Run()
    robot.DebugStats()