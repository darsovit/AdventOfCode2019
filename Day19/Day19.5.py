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
    def CountCoverage(self):
        count = 0
        for coord in self.tractorMap:
            count += self.tractorMap[coord]
        return count

class Coord:
    def __init__(self, x, y):
        self.output = [x, y]
        self.count  = 0
    def provideInput(self):
        self.count += 1
        return self.output[self.count - 1]

class Coverage:
    def __init__(self):
       self.count = 0
       self.valid = 0
    def handleOutput(self, val):
        self.count += 1
        self.valid += val
    def Continue(self):
        return self.count == self.valid

class HoldValue:
    def __init__(self):
        self.val = None
    def handleOutput( self, val ):
        self.val = val
    def GetVal(self):
        return self.val

def getStartOfBeam(prog, y, hint):
    x = hint - 1
    beam = None
    while True:
        value = HoldValue()
        coord = Coord(x,y)
        tractorBeam = Intcode.Intcode( prog.copy(), inputFunc=coord.provideInput, outputFunc=value.handleOutput)
        tractorBeam.Run()
        if value.GetVal() == 1:
            return x
        x += 1

def getEndOfBeam(prog, y, startX):
    x = startX
    while True:
        value = HoldValue()
        coord = Coord(x,y)
        tractorBeam = Intcode.Intcode( prog.copy(), inputFunc=coord.provideInput, outputFunc=value.handleOutput )
        tractorBeam.Run()
        if value.GetVal() == 0:
            return x
        x += 1

def widthOfBeamAtY( prog, y, hint=0 ):
    startOfBeam = getStartOfBeam(prog, y, hint)
    endOfBeam   = getEndOfBeam(prog, y, startOfBeam)
    return (startOfBeam, endOfBeam - startOfBeam)

def testCorner( prog, x, y ):
    value = HoldValue()
    coord = Coord(x,y)
    tractorBeam = Intcode.Intcode( prog.copy(), inputFunc=coord.provideInput, outputFunc=value.handleOutput )
    tractorBeam.Run()
    return value.GetVal() == 1

def CanSantaFitInTractor( prog, y ):
    
    startOfBeam = getStartOfBeam( prog, y, 0 )
    endOfBeam   = getEndOfBeam( prog, y, startOfBeam )
    assert( True == testCorner( prog, endOfBeam-1, y ) )
    
    se = testCorner( prog, endOfBeam-1, y + 99 )
    nw = testCorner( prog, endOfBeam-100, y )
    sw = testCorner( prog, endOfBeam-100, y + 99 )
    print( 'CanSantaFitInTractor: NE:',endOfBeam-1,y, 'se:',endOfBeam-1,y+99,se,'nw:',endOfBeam-100,y,nw,'sw:',endOfBeam-100,y+99,sw )
    
    return sw and nw and se
    #
    #coverage = Coverage()
    #scanner = TractorBeamScanner()
    
    #for thisy in range(y, y+100):
    #    for thisx in range(x, x+100):
    #        coord = Coord(thisx,thisy)
    #        tractorBeam = Intcode.Intcode( prog.copy(), inputFunc=coord.provideInput, outputFunc=coverage.handleOutput )
    #        tractorBeam.Run()
    #        if not coverage.Continue():
    #            return (thisx,thisy)
    #return None
#    if coverage >= (size * size):
#        return True
#    else:
#        return False

if __name__ == '__main__':
    prog = Intcode.readProgInput('input.txt')
    factor = 10000
    lowerBound = None
    yLoc = 500
    hint = 0
    while not lowerBound:
        (hint, width) = widthOfBeamAtY( prog, yLoc, hint )
        print(yLoc, width)
        if 100 == width:
            lowerBound = yLoc
        else:
            yLoc += 1
        
    print(lowerBound)
    upperBound = None
    findUpperBound=lowerBound * 2
    while not upperBound:
        coverage = CanSantaFitInTractor(prog, findUpperBound)
        print(findUpperBound, coverage)
        if coverage:
            upperBound = findUpperBound
            print("Found Upper Bound:", upperBound)
        else:
            lowerBound = findUpperBound
            findUpperBound *= 2
            print("Failed upperBound, adjusting lowerBound:", lowerBound)
    while lowerBound + 1 < upperBound:
        test = int( (lowerBound + upperBound)/2 )
        print("Testing:",test)
        if CanSantaFitInTractor(prog, test):
            upperBound = test
        else:
            lowerBound = test
    print(upperBound)
    (start, width) = widthOfBeamAtY( prog, upperBound, 0 )
    locX = start + width - 100
    locY = upperBound
    nw = testCorner( prog, locX, locY )
    ne = testCorner( prog, (start + width - 1), locY)
    sw = testCorner( prog, locX, locY+99)
    se = testCorner( prog, (start + width - 1), locY+99)
    print( nw, ne, sw, se, locX * 10000 + locY )
    
    # 8451129 is too high
    # 6830936 is too low (was using lowerBound which doesn't fit instead of largest that does fit)
