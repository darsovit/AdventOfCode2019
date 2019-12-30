#! python
#
# http://adventofcode.com/2019/day/21/
#

import Intcode

class OutputCollector:
    def __init__(self):
        self.output = ''

    def Output(self, val):
        if val < 128:
            if val == 10:
                print(self.output)
                self.output = ''
            else:
                self.output += chr(val)
        else:
            self.output = val

    def Data(self):
        return self.output

class SpringdroidInput:
    def __init__(self, inputProg):
        self.state = {}
        self.prog = inputProg
        self.step = ''
        self.pos  = 0

    def readInput(self):
        val = self.prog[self.pos]
        self.step += val
        self.pos += 1
        if val == '\n':
            print( self.step )
            self.step = ''
        return ord(val)


if __name__ == '__main__':
    collector = OutputCollector()
    springscript = [
       'NOT A T',
       'NOT B J',
       'OR T J',
       'NOT C T',
       'OR T J',
       'AND D J',
       'WALK',
       ''
    ]
    
    springscript2 = [
       'NOT A T',
       'NOT B J',
       'OR T J',
       'NOT C T',
       'OR T J',
       'AND D J',
       'NOT E T',
       'NOT T T',
       'OR H T',
       'AND T J',
       'RUN',
       ''
    ]
    springdroid = SpringdroidInput('\n'.join(springscript2))
    prog = Intcode.readProgInput('input.txt')
    droid = Intcode.Intcode( prog, outputFunc=collector.Output, inputFunc=springdroid.readInput )
    droid.Run()
    print(collector.Data())
