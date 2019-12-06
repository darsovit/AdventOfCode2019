#! python

def readInput():
    print("Read Input: 1")
    return 1

def sendOutput(val):
    print ("Output:", val)

def halt():
    print( "HALT" )

def store( code, z, val ):
    #print( 'store before:', code[z], val )
    code[z] = val
    #print( 'store after:', code[z], val )

def getInstr( code, ip ):
    instruction = code[ip] % 100
    if instruction == 1:
        return (lambda x,y,z: store(code, z, x + y), 4, 2)
    elif instruction == 2:
        return (lambda x,y,z: store(code, z, x * y), 4, 2)
    elif instruction == 3:
        return (lambda z: store(code, z, readInput()), 2, 0)
    elif instruction == 4:
        return (lambda z: sendOutput( z ), 2, 1)
    elif instruction == 99:
        return (halt, 1)
    else:
        print('Invalid instruction: ', instruction )

def buildCommand( code, ip ):
    (instruction,size,numInput) = getInstr( code, ip )
    immediateLambda = lambda x: x
    addressingLambda = lambda x: code[x]
    
    par1 = immediateLambda if int(code[ip] / 100) % 10   else addressingLambda
    par2 = immediateLambda if int(code[ip] / 1000) % 10  else addressingLambda
    par3 = immediateLambda if int(code[ip] / 10000) % 10 else addressingLambda

    if size == 4 and numInput == 2:
        return (lambda x,y,z: instruction(par1(x), par2(y), z), 4)
    elif size == 2 and numInput == 1:
        return (lambda z: instruction(par1(z)), 2)
    elif size == 2 and numInput == 0:
        return (instruction, size)
    else:
        return (instruction, size)

def Intcode(code):
    ip = 0
    ophalt = 99
    opadd  = 1
    opmul  = 2
    while ( code[ip] != ophalt ):
        (instruction,size) = buildCommand(code, ip)
        #print( ' '.join( map(str, code[ip:ip+size] ) ) )
        if size == 4:
            instruction( code[ip+1], code[ip+2], code[ip+3] )
        elif size == 2:
            instruction( code[ip+1] )
        else:
            instruction()
        ip += size

    print( "Intcode result:", code[0] )
    return code

def PrintProgram( code ):
    print( code )
    ip = 0
    ophalt = 99
    while ( code[ip] != ophalt ):
        (instruction, size) = buildCommand( code, ip )
        print( ' '.join( map(str, code[ip:ip+size] ) ) )
        ip = ip + size


def test():
    assert( [99] == Intcode([99]) )
    assert( [2,0,0,0,99] == Intcode([1,0,0,0,99]) )
    assert( [1, 7, 6, 6, 99, 0, 2, 1] == Intcode([1, 7, 6, 6, 99, 0, 1, 1]) )
    assert( [48,23,25,0,99] == Intcode([1101,23,25,0,99]) )
    assert( [2,3,0,6,99] == Intcode([2,3,0,3,99]) )
    assert( [2,4,4,5,99,9801] == Intcode([2,4,4,5,99,0]) )
    assert( [30,1,1,4,2,5,6,0,99] == Intcode([1,1,1,4,99,5,6,0,99]) )

def readProgInput():
    with open('input.txt') as f:
        line = str.rstrip( f.readline() )
        return list( map(int, line.split(',') ) )

def find_noun_verb_for_output(prog, expected):
    noun = 0
    verb = 0
    for noun in range(0,100):
        for verb in range(0,100):
            progcopy = prog.copy()
            progcopy[1] = noun
            progcopy[2] = verb
            output = Intcode(progcopy)
            if output[0] == expected:
                return (noun,verb)

test()
print("Test complete")
prog = readProgInput()

Intcode( prog )