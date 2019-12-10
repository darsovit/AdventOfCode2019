def readIntcodeInput():
    print("Read Input: 0")
    return 0

def sendIntcodeOutput(val):
    print ("Output:", val)

class Intcode:

    def halt():
        print( "HALT" )

    def store( self, z, val, newIp ):
        print( 'store before:', z, self.load(z), '->', val )
        if z < len(self.code):
            self.code[z] = val
        else:
            self.mem[z] = val
        print( 'store after:', z, self.load(z), '==', val )
        return newIp

    def load( self, z ):
        if z < len(self.code):
            return self.code[z]
        elif z in self.mem:
            return self.mem[z]
        else:
            return 0

    def adjustRelativeAddr( self, x, newIp ):
        self.relativeAddr += x
        return newIp

    def IntcodeOutputWrapper( self, func, z, ip ):
        func(z)
        return ip

    def getInstr( self ):
    #code, ip, inputFunc, outputFunc ):
        instruction = self.code[self.ip] % 100
        if instruction == 1:
            return (lambda x,y,z: self.store( z, x + y, self.ip+4 ), 4, 2)
        elif instruction == 2:
            return (lambda x,y,z: self.store( z, x * y, self.ip+4 ), 4, 2)
        elif instruction == 3:
            return (lambda z: self.store( z, self.inputFunc(), self.ip+2 ), 2, 0)
        elif instruction == 4:
            return (lambda z: self.IntcodeOutputWrapper( self.outputFunc, z, self.ip+2 ), 2, 1)
        elif instruction == 5:
            return (lambda x,y: y if x!=0 else self.ip+3, 3, 2)
        elif instruction == 6:
            return (lambda x,y: y if x==0 else self.ip+3, 3, 2)
        elif instruction == 7:
            return (lambda x,y,z: self.store( z, 1 if x < y else 0, self.ip+4 ), 4, 2)
        elif instruction == 8:
            return (lambda x,y,z: self.store( z, 1 if x == y else 0, self.ip+4 ), 4, 2)
        elif instruction == 9:
            return ( lambda x: self.adjustRelativeAddr( x, self.ip+2 ), 2, 1 )
        elif instruction == 99:
            return (halt, 1)
        else:
            print('Invalid instruction: ', instruction )

    def getLoadModeLambda( self, loadMode ):
        if loadMode == 0:  # Addressing mode
            return lambda x: self.load(x)
        elif loadMode == 1:  # Immediate mode
            return lambda x: x
        elif loadMode == 2:  # Relative mode
            return lambda x: self.load( self.relativeAddr + x )
    def getStoreModeLambda( self, loadMode ):
        if loadMode == 0:
            return lambda x: x
        elif loadMode == 2:
            return lambda x: self.relativeAddr + x
        assert( False )

    def getCode(self, offset=0):
        return self.code[self.ip+offset]

    def buildCommand(self):
#    code, ip, inputFunc, outputFunc ):
        (instruction,size,numInput) = self.getInstr() # code, ip, inputFunc, outputFunc )

        
        if ( numInput > 0 )
            par1 = self.getLoadModeLambda( int(self.getCode() / 100) % 10 )
            par2 = self.getLoadModeLambda( int(self.getCode() / 1000) % 10 )
            par3 = self.getLoadModeLambda( int(self.getCode() / 10000) % 10 )
        elif ( numInput < 0 ):
            par1 = lambda x: self.relativeAddr + x
        #immediateLambda = lambda x: x
        #addressingLambda = lambda x: self.load(x)
        
        #par1 = immediateLambda if int(self.code[self.ip] / 100) % 10   else addressingLambda
        #par2 = immediateLambda if int(self.code[self.ip] / 1000) % 10  else addressingLambda
        #par3 = immediateLambda if int(self.code[self.ip] / 10000) % 10 else addressingLambda

        if size == 4 and numInput == 2:
            return (lambda x,y,z: instruction(par1(x), par2(y), z), 4)
        elif size == 3 and numInput == 2:
            return (lambda x,y: instruction(par1(x),par2(y)), 3)
        elif size == 2 and numInput == 1:
            return (lambda z: instruction(par1(z)), 2)
        elif size == 2 and numInput == -1:
            return (lambda z: instruction(
        elif size == 2 and numInput == 0:
            return (instruction, size)
        else:
            return (instruction, size)

    def __init__(self, code, inputFunc = readIntcodeInput, outputFunc = sendIntcodeOutput):
        self.ip         = 0
        self.code       = code
        self.inputFunc  = inputFunc
        self.outputFunc = outputFunc
        self.relativeAddr = 0
        self.mem        = {}
    
    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def Run(self):
        ophalt = 99
        while ( self.getCode() != ophalt ):
            (instruction,size) = self.buildCommand() #self.code, self.ip, inputFunc, outputFunc)
            #print( ' '.join( map(str, code[ip:ip+size] ) ) )
            if size == 4:
                self.ip = instruction( self.getCode(1), self.getCode(2), self.getCode(3) )
            elif size == 3:
                self.ip = instruction( self.getCode(1), self.getCode(2) )
            elif size == 2:
                self.ip = instruction( self.getCode(1) )
            else:
                self.ip = instruction()

        #print( "Intcode result:", code[0] )
        return self.code
    
    def Step(self):
        ophalt = 99
        if ( self.getCode() != ophalt ):
            (instruction,size) = self.buildCommand()
            if size == 4:
                print( "DEBUG (IP:{},RelAddr:{}): ".format(self.ip, self.relativeAddr), self.getCode(), self.getCode(1), self.getCode(2), self.getCode(3) )
                newip = instruction( self.getCode(1), self.getCode(2), self.getCode(3) )
            elif size == 3:
                print( "DEBUG (IP:{},RelAddr:{}): ".format(self.ip, self.relativeAddr), self.getCode(), self.getCode(1), self.getCode(2) )
                newip = instruction( self.getCode(1), self.getCode(2) )
            elif size == 2:
                print( "DEBUG (IP:{},RelAddr:{}): ".format(self.ip, self.relativeAddr), self.getCode(), self.getCode(1) )
                newip = instruction( self.getCode(1) )
            else:
                print( "DEBUG (IP:{},RelAddr:{}): ".format(self.ip, self.relativeAddr), self.getCode() )
                newip = instruction()
            self.ip = newip
            print("DEBUG (IP:{},RelAddr:{})".format(self.ip, self.relativeAddr) )

def readProgInput( file ):
    with open( file ) as f:
        line = str.rstrip( f.readline() )
        return list( map( int, line.split(',') ) )

def addToList( state, name, x ):
    state[name] = state[name] + [ x ]

def storeOutput( state, name, x ):
    state[name] = x


def test():
    assert( [99] == Intcode([99]).Run() )
    assert( [2,0,0,0,99] == Intcode([1,0,0,0,99]).Run() )
    assert( [1, 7, 6, 6, 99, 0, 2, 1] == Intcode([1, 7, 6, 6, 99, 0, 1, 1]).Run() )
    assert( [48,23,25,0,99] == Intcode([1101,23,25,0,99]).Run() )
    assert( [2,3,0,6,99] == Intcode([2,3,0,3,99]).Run() )
    assert( [2,4,4,5,99,9801] == Intcode([2,4,4,5,99,0]).Run() )
    assert( [30,1,1,4,2,5,6,0,99] == Intcode([1,1,1,4,99,5,6,0,99]).Run() )
    assert( [1105,0,2,99] == Intcode([1105,0,2,99]).Run() )
    assert( [2,1,2,1,2,0,99] == Intcode([1105,1,2,1,2,0,99]).Run() )
    assert( [1106,1,2,99] == Intcode([1106,1,2,99]).Run() )
    assert( [0,0,2,1,2,0,99] == Intcode([1106,0,2,1,2,0,99]).Run() )
    assert( [1,1,2,0,99] == Intcode([1107,1,2,0,99]).Run() )
    assert( [0,2,1,0,99] == Intcode([1107,2,1,0,99]).Run() )
    assert( [0,2,2,0,99] == Intcode([1107,2,2,0,99]).Run() )
    assert( [1,2,2,0,99] == Intcode([1108,2,2,0,99]).Run() )
    assert( [0,1,2,0,99] == Intcode([1108,1,2,0,99]).Run() )
    assert( [0,0,4,0,99] == Intcode([8,0,4,0,99]).Run() )
    assert( [1,0,4,0,99] == Intcode([7,0,4,0,99]).Run() )


def test2():
    state = {}
    state['output']    = list()
    code = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    codeCopy = code.copy()
    output = Intcode(codeCopy, outputFunc=lambda x : addToList(state, 'output', x) ).Run()
    assert( state['output'] == code and output[0] == code[0] )
    state['expected'] = 34915192 * 34915192
    
    output = Intcode([1102,34915192,34915192,7,4,7,99,0], outputFunc=lambda x : storeOutput( state, 'output', x ) ).Run()
    assert( state['expected'] == state['output'] )

    code = [104,1125899906842624,99]
    output = Intcode(code, outputFunc=lambda x : storeOutput( state, 'output', x ) ).Run()
    assert( state['output'] == code[1] )

if __name__ == '__main__':
    test()
    test2()
    #test3()
    print("Intcode test complete")

