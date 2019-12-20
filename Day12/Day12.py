#! python

class MoonGravitySimulation:
    def __init__( self, moonPositions ):
        self.moons = []
        for moonPos in moonPositions:
            newMoon = {}
            newMoon['pos'] = moonPos
            newMoon['vel'] = (0,0,0)
            self.moons += [ newMoon ]
        self.steps = 0

    def CalcVelocityDiff( moon1pos, moon2pos):
        diffFor1 = [0,0,0]
        diffFor2 = [0,0,0]
        for axis in range(3):
            if moon1pos[axis] > moon2pos[axis]:
                diffFor1[axis] += -1
                diffFor2[axis] +=  1
            elif moon1pos[axis] < moon2pos[axis]:
                diffFor1[axis] +=  1
                diffFor2[axis] += -1
        return (tuple(diffFor1), tuple(diffFor2))
        
    def Add3DTuples( x, y ):
        return ( x[0]+y[0], x[1]+y[1], x[2]+y[2] )

    def UpdateVelocities(self):
        velocityUpdates = []
        for i in range(len(self.moons)):
            velocityUpdates += [ (0,0,0) ]
        for i in range(len(self.moons)):
            for j in range(i+1,len(self.moons)):
                (diffForI,diffForJ) = MoonGravitySimulation.CalcVelocityDiff(self.moons[i]['pos'], self.moons[j]['pos'])
                #print('CalcDiffs for moon {} to moon {}: {}, {}'.format( i, j, diffForI, diffForJ ) )
                velocityUpdates[i] = MoonGravitySimulation.Add3DTuples( velocityUpdates[i], diffForI )
                velocityUpdates[j] = MoonGravitySimulation.Add3DTuples( velocityUpdates[j], diffForJ )
        for i in range(len(self.moons)):
            #print(self.moons[i]['vel'], velocityUpdates[i])
            self.moons[i]['vel'] = MoonGravitySimulation.Add3DTuples( self.moons[i]['vel'], velocityUpdates[i])
    
    def ApplyVelocities(self):
        for i in range(len(self.moons)):
            self.moons[i]['pos'] = MoonGravitySimulation.Add3DTuples( self.moons[i]['pos'], self.moons[i]['vel'] )
            #posUpdate = [self.moons[i]['pos'][0],self.moons[i]['pos'][1],self.moons[i]['pos'][2]]
            #for axis in range(3):
            #    posUpdate[axis] += self.moons[i]['vel'][axis]
            #self.moons[i]['pos'] = (posUpdate[0],posUpdate[1],posUpdate[2])
    
    def PerformStep(self):
        self.steps += 1
        self.UpdateVelocities()
        self.ApplyVelocities()
        #self.PrintDetails()

    def Run(self, steps):
        for i in range(steps):
            self.PerformStep()

    def EnergyCalc( self, pos ):
        return abs(pos[0])+abs(pos[1])+abs(pos[2])
        
    def CalculateTotalEnergy(self):
        totalEnergy = 0
        for moon in self.moons:
            totalEnergy += self.EnergyCalc(moon['pos']) * self.EnergyCalc(moon['vel'])
        return totalEnergy

    def PrintDetails(self):
        count = 1
        for moon in self.moons:
            print('Step: {}: Moon {}: Pos: {}, Velocity: {}'.format(self.steps, count, moon['pos'], moon['vel']))
        print(self.CalculateTotalEnergy())

if __name__ == '__main__':
    simulation = MoonGravitySimulation( [(-19,-4,2),(-9,8,-16),(-4,5,-11),(1,9,-13)] )
    simulation.PrintDetails()
    simulation.Run( 1000 )
    simulation.PrintDetails()
    
# Answer: 2184873 is too high