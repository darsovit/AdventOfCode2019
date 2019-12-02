#! python

def Intcode(code):
    ip = 0
    ophalt = 99
    opadd  = 1
    opmul  = 2
    while ( code[ip] != ophalt ):
        if code[ip] == opadd:
            (opcode,par1,par2,par3) = code[ip:ip+4]
            code[par3] = code[par1] + code[par2]
            oplength = 4
        elif code[ip] == opmul:
            (opcode,par1,par2,par3) = code[ip:ip+4]
            code[par3] = code[par1] * code[par2]
            oplength = 4
        else:
            assert( False )
        ip += oplength
    return code

def test():
    assert( [99] == Intcode([99]) )
    assert( [2,0,0,0,99] == Intcode([1,0,0,0,99]) )
    assert( [2,3,0,6,99] == Intcode([2,3,0,3,99]) )
    assert( [2,4,4,5,99,9801] == Intcode([2,4,4,5,99,0]) )
    assert( [30,1,1,4,2,5,6,0,99] == Intcode([1,1,1,4,99,5,6,0,99]) )

def readInput():
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

prog = readInput()

noun = 0
verb = 0
output = []

print( find_noun_verb_for_output( prog, 19690720 ) )
