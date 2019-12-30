#! python
#
# https://adventofcode.com/2019/day/23
#

import Intcode
import multiprocessing as mp
from time import sleep

class NetworkBackbone:
    def __init__(self, numProcesses):
        self.pipes = {}
        self.numProcesses = numProcesses
        for i in range(numProcesses):
            self.pipes[i] = mp.Pipe()

    def GetChildPipe(self, i):
        return self.pipes[i][1]

    def HandleSwitching(self):
        OutOfSizeMessage = False
        while not OutOfSizeMessage:
            # Sleep for some short amount of time
            for i in range(self.numProcesses):
                if self.pipes[i][0].poll(0):
                    (address,x,y) = self.pipes[i][0].recv()
                    if address < self.numProcesses:
                        print('Message from {} send to {}: {}'.format(i, address, (x,y)))
                        self.pipes[address][0].send((x,y))
                    else:
                        assert( address == 255 )
                        self.answer = (x,y)
                        OutOfSizeMessage = True

    def GetAnswer(self):
        return self.answer

class MultiProcessIO:
    def __init__(self, pipe, address):
        self.instanceId = address
        self.pipe = pipe
        self.outputMsgState = []
        self.inputMsgState  = [ address ]

    def readInput(self):
        if len(self.inputMsgState) == 0:
            if self.pipe.poll(0):
                message = self.pipe.recv()
                print('readInput[{}]: Inbound message: {}'.format( self.instanceId, message ))
                self.inputMsgState = [ message[0], message[1] ]
            else:
                sleep(0.05)
                return -1
        return self.inputMsgState.pop(0)

    def writeOutput(self, val):
        self.outputMsgState += [ val ]
        if len(self.outputMsgState) == 3:
            message = tuple(self.outputMsgState)
            print('writeOutput[{}]: Outbound message: {}'.format( self.instanceId, message ) )
            self.pipe.send(message)
            self.outputMsgState = []

def Intcode_mp( codefunc, instanceId, pipe ):
    code = codefunc()
    try:
        ioHandler = MultiProcessIO(pipe, instanceId)
        prog = Intcode.Intcode( code, inputFunc=ioHandler.readInput, outputFunc=ioHandler.writeOutput )
        prog.Run()
    except:
        print( 'Failed to run Intcode for instance: {}'.format(instanceId) )
        raise

def RunNetworkSequence( codefunc ):
    numProcesses = 50
    backbone = NetworkBackbone( numProcesses )
    processes = []
    for i in range( numProcesses ):
        pipe = backbone.GetChildPipe(i)
        processes += [mp.Process( target=Intcode_mp, args=(codefunc, i, pipe) )]
    for p in processes:
        p.start()
    backbone.HandleSwitching()
    print(backbone.GetAnswer())
    for p in processes:
        p.join()

def readProg():
    return Intcode.readProgInput('input.txt')

if __name__ == '__main__':
    RunNetworkSequence( readProg )
