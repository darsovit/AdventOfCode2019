#! python

def Intcode(code):
    ip = 0
    ophalt = 99
    opadd  = 1
    while ( code[ip] != ophalt ):
        (opcode,par1,par2,par3) = code[ip:ip+4]
        if opcode == opadd:
            code[par3] = code[par1] + code[par2]
            oplength = 4
        elif opcode == 2:
            code[par3] = code[par1] * code[par2]
            oplength = 4
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
test()

# 337106 is too low
input = readInput()
input[1] = 12  # Replaced per direction in puzzle
input[2] = 2   # Replaced per direction in puzzle
print( Intcode( input ) )