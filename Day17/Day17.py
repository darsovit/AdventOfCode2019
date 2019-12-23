#! python
#
# http://adventofcode.com/2019/day/17
#

import Intcode

class ScaffoldingImage:
    def __init__(self):
        self.image = []
        self.maxX = None
        self.maxY = None
        self.image += ['']
    
    def collectImage( self, val ):
        if val == 10:
            self.image += ['']
        else:
            self.image[-1] += chr(val)

    def Render(self):
        print( '\n'.join(self.image) )

    def FindIntersections(self):
        neighbors = [(1,0),(-1,0),(0,1),(0,-1)]
        intersections = []
        for y in range(len(self.image)):
            for x in range(len(self.image[y])):
                if self.image[y][x] != '.':
                    isIntersection = True
                    for neighbor in neighbors:
                        if y+neighbor[1] >= 0 and y+neighbor[1] < len(self.image) and x+neighbor[0] >= 0 and x+neighbor[0] < len(self.image[neighbor[1]+y]):
                            isIntersection = isIntersection and self.image[y+neighbor[1]][x+neighbor[0]] != '.'
                    if isIntersection:
                        intersections += [(x,y)]
        return intersections
        
    def DrawIntersections(self, intersections):
        intersected = self.image.copy()
        for intersection in intersections:
            print(intersection)
            line = intersected[intersection[1]]
            newline = line[:intersection[0]] + 'O' + line[intersection[0]+1:]
            intersected[intersection[1]] = newline
            print(newline)
        print( '\n'.join(intersected) )

def GetAlignmentParams( intersections ):
    sum = 0
    for intersection in intersections:
        sum += (intersection[0] * intersection[1])
    return sum

if __name__ == '__main__':
    scaffoldingImage = ScaffoldingImage()
    asciiProg = Intcode.Intcode(Intcode.readProgInput('input.txt'), outputFunc=scaffoldingImage.collectImage)
    asciiProg.Run()
    scaffoldingImage.Render()
    intersections = scaffoldingImage.FindIntersections()
    print( GetAlignmentParams( intersections ) )
    #scaffoldingImage.DrawIntersections( intersections )
    print(intersections)