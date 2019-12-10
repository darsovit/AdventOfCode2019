#! python

import multiprocessing as mp
import Intcode

def test():
    assert( [99] == Intcode.Intcode([99]).Run() )
    #assert( [2,0,0,0,99] == Intcode([1,0,0,0,99]).Run() )
    #assert( [1, 7, 6, 6, 99, 0, 2, 1] == Intcode([1, 7, 6, 6, 99, 0, 1, 1]).Run() )
    #assert( [48,23,25,0,99] == Intcode([1101,23,25,0,99]).Run() )
    #assert( [2,3,0,6,99] == Intcode([2,3,0,3,99]).Run() )
    #assert( [2,4,4,5,99,9801] == Intcode([2,4,4,5,99,0]).Run() )
    #assert( [30,1,1,4,2,5,6,0,99] == Intcode([1,1,1,4,99,5,6,0,99]).Run() )
    #assert( [1105,0,2,99] == Intcode([1105,0,2,99]).Run() )
    #assert( [2,1,2,1,2,0,99] == Intcode([1105,1,2,1,2,0,99]).Run() )
    #assert( [1106,1,2,99] == Intcode([1106,1,2,99]).Run() )
    #assert( [0,0,2,1,2,0,99] == Intcode([1106,0,2,1,2,0,99]).Run() )
    #assert( [1,1,2,0,99] == Intcode([1107,1,2,0,99]).Run() )
    #assert( [0,2,1,0,99] == Intcode([1107,2,1,0,99]).Run() )
    #assert( [0,2,2,0,99] == Intcode([1107,2,2,0,99]).Run() )
    #assert( [1,2,2,0,99] == Intcode([1108,2,2,0,99]).Run() )
    #assert( [0,1,2,0,99] == Intcode([1108,1,2,0,99]).Run() )
    #assert( [0,0,4,0,99] == Intcode([8,0,4,0,99]).Run() )
    #assert( [1,0,4,0,99] == Intcode([7,0,4,0,99]).Run() )


def Intcode_mp( progfunc, instanceId, inputQueue, outputQueue, haltQueue ):
    prog = progfunc()
    program = Intcode( prog, lambda : readInputQueue( instanceId, inputQueue ), lambda x: writeOutputQueue( instanceId, outputQueue, x ) )
    try:
        program.Run()
        writeOutputQueue( instanceId+5, haltQueue, prog[0] )
    except:
        print( program )
        writeOutputQueue( instanceId+5, haltQueue, -1 )
    
def addToList( state, name, x ):
    state[name] = state[name] + [ x ]

def storeOutput( state, name, x ):
    state[name] = x

def test2():
    state = {}
    state['output']    = list()
    code = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    codeCopy = code.copy()
    output = Intcode.Intcode(codeCopy, outputFunc=lambda x : addToList(state, 'output', x) ).Run()
    print( state )
    assert( state['output'] == code and output[0] == code[0] )
    state['expected'] = 34915192 * 34915192
    
    output = Intcode.Intcode([1102,34915192,34915192,7,4,7,99,0], outputFunc=lambda x : storeOutput( state, 'output', x ) ).Run()
    assert( state['expected'] == state['output'] )

    code = [104,1125899906842624,99]
    output = Intcode.Intcode(code, outputFunc=lambda x : storeOutput( state, 'output', x ) ).Run()
    assert( state['output'] == code[1] )
    
def BOOST():
    code = Intcode.readProgInput('input.txt')
    boostProg = Intcode.Intcode( code, lambda : 2 )
    boostProg.Run()
    

if __name__ == '__main__':
    Intcode.test()
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