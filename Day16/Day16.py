#! python
#
# http://adventofcode.com/2019/day/16
#

def buildBase(length, step):
    base = [0, 1, 0, -1]
    builtBase = []
    for j in range(1, step+1):
        builtBase += [base[0]]
    baseIndex = 1
    while len(builtBase) < length:
        stepCount = 0
        for j in range(stepCount,step+1):
            builtBase += [base[baseIndex]]
        baseIndex = (baseIndex + 1)%len(base)
    return builtBase[0:length]

def calculateFFTStep(input, step):
    base = buildBase(len(input),step)
    #print( base )
    #print(len(base),len(input))
    assert( len(base)==len(input) )
    sum = 0
    for i in range(step,len(input)):
        sum += input[i]*base[i]
    #print( sum, sum % 10 )
    return abs(sum) % 10
    
def FFT( input, phase ):
    output = []
    for i in range(len(input)):
        output += [calculateFFTStep(input, i)]
    return output

def PerformFFT(inputstr, numPhases):
    input = []
    for i in range(len(inputstr)):
        input += [ int(inputstr[i]) ]
    #print(input)
    for i in range(numPhases):
        input = FFT(input, i)
    return ''.join(list(map(str,input)))
    
def test():
    #outputstr = PerformFFT('12345678',1)
    #print(outputstr)
    assert( '48226158' == PerformFFT('12345678',1) )
    assert( '34040438' == PerformFFT('12345678',2) )
    assert( '03415518' == PerformFFT('12345678',3) )
    assert( '01029498' == PerformFFT('12345678',4) )
    assert( '24176176' == PerformFFT('80871224585914546619083218645595',100)[0:8] )
    assert( '73745418' == PerformFFT('19617804207202209144916044189917',100)[0:8] )
    assert( '52432133' == PerformFFT('69317163492948606335995924319873',100)[0:8] )

def readInput():
    with open('input.txt') as f:
        return str.rstrip(f.readline())

test()
print( PerformFFT( readInput(), 100 )[0:8] )