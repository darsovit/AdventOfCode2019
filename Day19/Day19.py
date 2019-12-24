#! python
#
# http://adventofcode.com/2019/day/19
#

import Intcode

class TractorBeamScanner:
    def __init__(self):
        self.tractorMap = {}
        self.currentInput = 0
        self.lastInputCoord = None

    def handleOutput(self, x, y, val):
        self.tractorMap[(x,y)] = val

    def RenderAndCount(self):
        print(self.tractorMap)
        lines = []
        count = 0
        for y in range(50):
            line = ''
            for x in range(50):
                if self.tractorMap[(x,y)] == 1:
                    line += '#'
                    count += 1
                else:
                    line += '.'
            lines += [ line ]
        print( '\n'.join(lines) )
        return count

class Coord:
    def __init__(self, x, y):
        self.output = [x, y]
        self.count  = 0
    def provideInput(self):
        self.count += 1
        return self.output[self.count - 1]
    

if __name__ == '__main__':
    scanner = TractorBeamScanner()
    prog = Intcode.readProgInput('input.txt')
    for y in range(50):
        for x in range(50):
            coord = Coord(x,y)
            tractorBeam = Intcode.Intcode( prog.copy(), inputFunc=coord.provideInput, outputFunc=lambda val : scanner.handleOutput(x, y, val) )
            tractorBeam.Run()
    print( scanner.RenderAndCount() )
    
    