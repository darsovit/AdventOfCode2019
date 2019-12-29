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
    springdroid = SpringdroidInput('NOT A T\nNOT B J\nOR T J\nNOT C T\nOR T J\nAND D J\nWALK\n')
    prog = Intcode.readProgInput('input.txt')
    droid = Intcode.Intcode( prog, outputFunc=collector.Output, inputFunc=springdroid.readInput )
    droid.Run()
    print(collector.Data())
