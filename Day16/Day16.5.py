#! python
#
# https://adventofcode.com/2019/day/16
#
#
#
#
#
'''
12345678901234567890
+0-0+0-0+0-0+0-0+0-0
0++00--00++00--00++0
00+++000---000+++000
000++++0000----0000+
0000+++++00000-----0
00000++++++000000---
000000+++++++0000000
0000000++++++++00000
00000000+++++++++000
000000000++++++++++0
0000000000++++++++++
00000000000+++++++++
000000000000++++++++
0000000000000+++++++
00000000000000++++++
000000000000000+++++
0000000000000000++++
00000000000000000+++
000000000000000000++
0000000000000000000+
'''
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

def getBaseVal(step, i):
    whichBase = int( (i + 1) / (step+1) ) % 4
    if whichBase == 1:
        return 1
    elif whichBase == 3:
        return -1
    return 0
    #base = [0, 1, 0, -1]
    #return base[whichBase]

def calculateFFTStep(input, step, startstep):
    #base = buildBase(len(input),step)
    #print( base )
    #print(len(base),len(input))
    #assert( len(base)==len(input) )
    val = 0
    max = len(input)
    #print('calculateFFTStep:', len(input), ',', step, ',', startstep)
    for i in range(step,len(input)+startstep,step+1):
        baseVal = getBaseVal(step,i)
        #print('baseVal:', baseVal)
        if baseVal == 1:
            if i + step + 1 < max:
                max = i + step + 1
            val += sum(input[i-startstep:max])
        elif baseVal == -1:
            if i + step + 1 < max:
                max = i + step + 1
            val -= sum(input[i-startstep:max])
            #for j in range(i, i + step + 1 if len(input) > (i+step+1) else len(input)):
            #    sum += input[j]*baseVal #base[i]
        # nothing to do for baseVal = 0
    #print( sum, sum % 10 )
    result = abs(val) % 10
    #print('calculateFFTStep:', len(input), ',', step, ',', startstep, ',', result)
    return result
    
def FFT( input, startstep ):
    output = []
    halfwayPoint = int((len(input)+startstep)/2 + 0.6)
    fullLength   = len(input)+startstep
    #print(halfwayPoint)
    #print(fullLength)
    #print(startstep)
    #print(len(input))
    for i in range(startstep, halfwayPoint):
        output += [calculateFFTStep(input, i+startstep, startstep)]
    reversedEnding = []
    newVal = 0
    startval = max(halfwayPoint,startstep)
    for i in range(fullLength-startval):
        #print(i, fullLength - (fullLength - i))
        #print(i, len(input) - 1 - i )
        newVal = (newVal + input[len(input) - 1 - i]) % 10
        reversedEnding += [ newVal ]
    output += reversedEnding[::-1]
    #print(len(output))
    #print(len(input))
    #for i in range(len(input)):
    #    output += [calculateFFTStep(input, i+startstep, startstep)]
        #if 0 == (i % 10000):
            #print( 'Step {}, complete with output {}'.format(i+1,output[-1]) )
    return output

def PerformFFT(inputstr, numPhases):
    input = []
    whichNums = int(inputstr[0:7])
    print(whichNums)
    for i in range(len(inputstr)):
        input += [ int(inputstr[i]) ]
    totalNums = 10000 * len(inputstr) - whichNums
    numRepeats = int( totalNums / len(inputstr) )
    actualVal = input[ whichNums % len(inputstr): ]
    for i in range(numRepeats):
        actualVal += input
    print(len(inputstr) * 10000, len(actualVal))
    #print(input)
    for i in range(numPhases):
        print('Running phase:', i+1)
        actualVal = FFT(actualVal, whichNums)
        print('Result after phase:', i+1, ':', ''.join(list(map(str,actualVal[0:8]))))
    return ''.join(list(map(str,actualVal[0:8])))
    
def test():
    #outputstr = PerformFFT('12345678',1)
    #print(outputstr)
    assert( 1 == getBaseVal(0,0) )
    assert( 0 == getBaseVal(0,1) )
    assert( -1 == getBaseVal(0,2) )
    assert( 0 == getBaseVal(0,3) )
    assert( 1 == getBaseVal(0,4) )
    assert( 0 == getBaseVal(1,0) )
    assert( 1 == getBaseVal(1,1) )
    assert( 1 == getBaseVal(1,2) )
    assert( 0 == getBaseVal(1,3) )
    assert( 0 == getBaseVal(1,4) )
    assert( -1 == getBaseVal(1,5) )
    assert( -1 == getBaseVal(1,6) )
    assert( 0  == getBaseVal(1,7) )
    assert( 0  == getBaseVal(1,8) )
    #assert( '48226158' == PerformFFT('12345678',1) )
    #assert( '34040438' == PerformFFT('12345678',2) )
    #assert( '03415518' == PerformFFT('12345678',3) )
    #assert( '01029498' == PerformFFT('12345678',4) )
    #assert( '24176176' == PerformFFT('80871224585914546619083218645595',100)[0:8] )
    #assert( '73745418' == PerformFFT('19617804207202209144916044189917',100)[0:8] )
    #assert( '52432133' == PerformFFT('69317163492948606335995924319873',100)[0:8] )
    #assert( '88323090' == PerformFFT( readInput(), 100)[0:8] )
    val = PerformFFT( '03036732577212944063491565474664', 100 )
    assert '84462026' == val, 'Expected 84462026, got {}'.format(val)
    
def readInput():
    with open('input.txt') as f:
        return str.rstrip(f.readline())

test()
print( PerformFFT( readInput(), 100 )[0:8] )