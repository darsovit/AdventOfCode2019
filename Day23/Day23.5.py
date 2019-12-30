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
        self.starvedProcesses = []
        self.numProcesses = numProcesses
        for i in range(numProcesses):
            self.pipes[i] = mp.Pipe()
            self.starvedProcesses.append(False)
        assert( len(self.starvedProcesses) == numProcesses )

    def GetChildPipe(self, i):
        return self.pipes[i][1]

    def HandleSwitching(self):
        Done = False
        priorWrittenNatPacket = None
        lastNatPacket = None
        while not Done:
            # Sleep for some short amount of time
            for i in range(self.numProcesses):
                if self.pipes[i][0].poll(0):
                    (address,x,y) = self.pipes[i][0].recv()
                    if address == 254:
                        #print('Message from {} about being starved'.format(i))
                        assert(i == x)
                        self.starvedProcesses[i] = True
                    elif address < self.numProcesses:
                        #print('Message from {} send to {}: {}'.format(i, address, (x,y)))
                        self.pipes[address][0].send((x,y))
                        if self.starvedProcesses[i]:
                            self.starvedProcesses[i] = True
                        if self.starvedProcesses[address]:
                            #print('Clearing starvation from {}'.format(address))
                            self.starvedProcesses[address] = False
                    else:
                        assert( address == 255 )
                        print('Update on last nat packet from {}: {}'.format(i, (x,y)))
                        lastNatPacket = (x,y)
                        if self.starvedProcesses[i]:
                            #print('Clearing starvation from {}'.format(i))
                            self.starvedProcesses[i] = False
            allStarved = True
            for starved in self.starvedProcesses:
                allStarved = allStarved and starved
            if allStarved:
                if priorWrittenNatPacket and priorWrittenNatPacket[1] == lastNatPacket[1]:
                    self.answer = priorWrittenNatPacket[1]
                    Done = True
                self.starvedProcesses[0] = False
                print('NAT: Send off packet {} to 0'.format(lastNatPacket))
                self.pipes[0][0].send(lastNatPacket)
                priorWrittenNatPacket = lastNatPacket
            else:
                #sleep(0.01)
                pass
                
    def GetAnswer(self):
        return self.answer

class MultiProcessIO:
    def __init__(self, pipe, address):
        self.instanceId = address
        self.pipe = pipe
        self.outputMsgState = []
        self.inputMsgState  = [ address ]
        self.inputWithoutOutputCount = 0
        self.flaggedNoInput = False

    def readInput(self):
        if len(self.inputMsgState) == 0:
            if self.pipe.poll(0):
                message = self.pipe.recv()
                #print('readInput[{}]: Inbound message: {}'.format( self.instanceId, message ))
                self.inputMsgState = [ message[0], message[1] ]
                self.flaggedNoInput = False
                self.inputWithoutOutputCount = 0
            else:
                self.inputWithoutOutputCount += 1
                if (self.inputWithoutOutputCount / 200) > 1 and not self.flaggedNoInput:
                    message = (254,self.instanceId,self.inputWithoutOutputCount)
                    self.pipe.send(message)
                    self.flaggedNoInput = True
                if self.flaggedNoInput:
                    sleep(0.001)
                return -1
        return self.inputMsgState.pop(0)

    def writeOutput(self, val):
        self.outputMsgState += [ val ]
        if len(self.outputMsgState) == 3:
            message = tuple(self.outputMsgState)
            #print('writeOutput[{}]: Outbound message: {}'.format( self.instanceId, message ) )
            self.pipe.send(message)
            self.outputMsgState = []
            self.flaggedNoInput = False
            self.inputWithoutOutputCount = 0

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
    # 19481 is too high, increased count of input w/o output to 20
    # 19453 is too low, increased count of input w/o output to 30, adjusted some consideration of idle
    # 19460 is too low, increased count of input w/o output to 40
    # 19461 is incorrect, 5 min delay
    # 19463 for 60, 400 with 0.01 delays and fixing to address unmarking the id that sent something
    # 19464 for 100
    # 19444 for 200?
    # 19461 for 400
    # 19463 for 400, with 0.01 delays and a fix to address unarking the id that sent something
    # 19473 for 100
    # 19477 for 200
    # Settled on 19463 after removing delay for NAT computer
