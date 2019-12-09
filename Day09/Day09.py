#! python

import multiprocessing as mp

def readIntcodeInput():
    print("Read Input: 0")
    return 0

def sendIntcodeOutput(val):
    print ("Output:", val)

class Intcode:

    def halt():
        print( "HALT" )

    def store( self, z, val, newIp ):
        #print( 'store before:', code[z], val )
        if z < len(self.code):
            self.code[z] = val
        else:
            self.mem[z] = val
        return newIp
        #print( 'store after:', code[z], val )

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
        if loadMode == 1:  # Immediate mode
            return lambda x: x
        if loadMode == 2:  # Relative mode
            return lambda x: self.load( self.relativeAddr + x )

    def getCode(self, offset=0):
        return self.code[self.ip+offset]

    def buildCommand(self):
#    code, ip, inputFunc, outputFunc ):
        (instruction,size,numInput) = self.getInstr() # code, ip, inputFunc, outputFunc )
        
        par1 = self.getLoadModeLambda( int(self.getCode() / 100) % 10 )
        par2 = self.getLoadModeLambda( int(self.getCode() / 1000) % 10 )
        par3 = self.getLoadModeLambda( int(self.getCode() / 10000) % 10 )
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
    
def readProgInput():
    with open('input.txt') as f:
        line = str.rstrip( f.readline() )
        return list( map(int, line.split(',') ) )

def sample1Prog():
    return [3,15,         # input[0] -> A(15)
            3,16,          # input[1] -> B(16)
            1002,16,10,16, # B * 10 -> B
            1,16,15,15,    # B + A -> A
            4,15,          # A -> output[0]
            99,            # halt
            0,0            # memory 15 and 16
            ]

def sample1Input():
    return (43210,
            [4,3,2,1,0],sample1Prog )

def sample2Prog():
    return [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
def sample2Input():
    return (54321,[0,1,2,3,4], sample2Prog)

def sample3Prog():
    return [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
def sample3Input():
    return (65210,[1,0,4,3,2], sample3Prog)

def readInputFunc( state, inputName ):
    return state[inputName].pop(0)

def buildInputFunc( state, inputName, newval ):
    state[inputName] += [ newval ]

def readInputQueue( instanceId, inputQueue ):
    #print(instanceId, ": Reading input queue" )
    val = inputQueue.get()
    #print(instanceId, ": Read input queue: ", val )
    return val

def writeOutputQueue( instanceId, outputQueue, newval ):
    #print(instanceId+1, ": Writing to output queue:", newval )
    outputQueue.put( newval )
    #print(instanceId+1, ": Finished write to output queue" )

def Intcode_mp( progfunc, instanceId, inputQueue, outputQueue, haltQueue ):
    prog = progfunc()
    program = Intcode( prog, lambda : readInputQueue( instanceId, inputQueue ), lambda x: writeOutputQueue( instanceId, outputQueue, x ) )
    try:
        program.Run()
        writeOutputQueue( instanceId+5, haltQueue, prog[0] )
    except:
        print( program )
        writeOutputQueue( instanceId+5, haltQueue, -1 )
    

def runAmplifierSequence( phaseSeq, progfunc ):
    state = {}
    state['pipes'] = {}
    state['pipes'][0] = mp.Queue()
    state['pipes'][1] = mp.Queue()
    state['pipes'][2] = mp.Queue()
    state['pipes'][3] = mp.Queue()
    state['pipes'][4] = mp.Queue()

    state['halt'] = {}
    state['halt'][0] = mp.Queue()
    state['halt'][1] = mp.Queue()
    state['halt'][2] = mp.Queue()
    state['halt'][3] = mp.Queue()
    state['halt'][4] = mp.Queue()
    
    state['pipes'][0].put( phaseSeq[0] )
    state['pipes'][0].put( 0 )
    state['pipes'][1].put( phaseSeq[1] )
    state['pipes'][2].put( phaseSeq[2] )
    state['pipes'][3].put( phaseSeq[3] )
    state['pipes'][4].put( phaseSeq[4] )
    
    state['status'] = {}
    
#    state[0] = [ phaseSeq[0], 0 ]
#    state[1] = [ phaseSeq[1] ]
#    state[2] = [ phaseSeq[2] ]
#    state[3] = [ phaseSeq[3] ]
#    state[4] = [ phaseSeq[4] ]
#    state[5] = []
    processes = []
    for i in range(0,5):
        #print( 'Input start: ', state[i] )
        processes += [mp.Process( target=Intcode_mp, args=( progfunc, i, state['pipes'][i], state['pipes'][(i+1)%5], state['halt'][i]) ) ]
        #print( state[i+1] )
        #print( state[5] )
    for p in processes:
        p.start()
    failed = False

    for i in range(0,5):
        state['status'][i] = readInputQueue( i+6, state['halt'][i] )
        if state['status'][i] == -1:
            failed = True
    if not failed:
        #print( 'processing didn\'t fail, read result' )
        rc = readInputQueue( -1, state['pipes'][0] )
    else:
        print( 'processing failed, return -1')
        rc = -1
    for p in processes:
        #print( 'joining process' )
        p.join()

    return rc

def heapPermutation( state, a, size, n ):
    if size == 1:
        state['permutations'] = state['permutations'] + [ a.copy() ]
    else:
        for i in range( size ):
            heapPermutation( state, a, size-1, n )
            swapper = i
            if size & 1:
                swapper = 0
            tmp = a[swapper]
            a[swapper] = a[size-1]
            a[size-1] = tmp

def findBestAmplifierSequence( progfunc, amplifierSettings=[0,1,2,3,4] ):
    state = {}
    state['permutations'] = list()
    heapPermutation( state, amplifierSettings, 5, 5 )
    bestPermutation = None
    loudestOutput = None
    for permutation in state['permutations']:
        output = runAmplifierSequence( permutation, progfunc )
        if not loudestOutput or loudestOutput < output:
            loudestOutput = output
            bestPermutation = permutation
    return (loudestOutput, bestPermutation)

def test3():
    (output,phaseSeq,progfunc) = sample1Input()
    assert( output == runAmplifierSequence( phaseSeq, progfunc ) )
    (output,phaseSeq,progfunc) = sample2Input()
    assert( output == runAmplifierSequence( phaseSeq, progfunc ) )
    (output,phaseSeq,progfunc) = sample3Input()
    assert( output == runAmplifierSequence( phaseSeq, progfunc ) )

def test2():
    output = Intcode([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]).Run()
    output = Intcode([1102,34915192,34915192,7,4,7,99,0]).Run()
    output = Intcode([104,1125899906842624,99]).Run()

def testInputFunc():
    state = {}
    state['input1'] = [4, 0]
    readFunc = lambda : readInputFunc( state, 'input1' )
    
    print( readFunc() )
    print( readFunc() )

def testOutputFunc():
    state = {}
    state['input'] = [3]
    outputFunc = lambda x: buildInputFunc( state, 'input', x )
    outputFunc( 245 )
    print( state )

def test3():
    (output,phaseSeq,prog) = sample1Input()
    assert( (output, phaseSeq) == findBestAmplifierSequence( prog ) )
    (output,phaseSeq,prog) = sample2Input()
    assert( (output, phaseSeq) == findBestAmplifierSequence( prog ) )
    (output,phaseSeq,prog) = sample3Input()
    assert( (output, phaseSeq) == findBestAmplifierSequence( prog ) )

def BOOST():
    code = readProgInput()
    boostProg = Intcode( code, lambda : 1 )
    boostProg.Run()
    

if __name__ == '__main__':
    testInputFunc()
    testOutputFunc()
    test()
    test2()
    #test3()

    print("Test complete")
    BOOST()
    #(output, phaseSeq) = findBestAmplifierSequence( readProgInput, [5,6,7,8,9] )
    
    
#prog = readProgInput()
#testprog = prog.copy()
#Intcode( testprog )
#testprog = prog.copy()
#(output, phaseSeq) = findBestAmplifierSequence( prog )
#print( output, phaseSeq )
#def overrideoutput(x):
#    print("Override output:", x)

#Intcode( testprog, lambda : 3, lambda z: print("Override output:", z) )