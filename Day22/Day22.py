#! python
#
# http://adventofcode.com/2019/day/22/
#


def performCut( deck, cutPos ):
    if ( cutPos > 0 ):
        deck = deck[cutPos:] + deck[:cutPos]
    else:
        deck = deck[cutPos:] + deck[:cutPos]
    return deck

def performReverse(deck):
    deck.reverse()
    return deck

def performShuffle(deck, increment):
    newdeck = deck.copy()
    pos = 0
    for card in deck:
        newdeck[pos] = card
        pos = ( pos + increment ) % len(newdeck)
    return newdeck

def shuffle( deck, instructions ):
    for instruction in instructions:
        cutordeal = instruction.split(' ')
        if 2 == len(cutordeal):
            assert( 'cut'==cutordeal[0] )
            deck = performCut( deck, int(cutordeal[1]) )
        else:
            assert( 4 == len(cutordeal) )
            if 'into' == cutordeal[1]:
                deck = performReverse( deck )
            elif 'with' == cutordeal[1]:
                deck = performShuffle(deck, int(cutordeal[3]))
            else:
                assert( False )
    return deck

def test1():
    deck = list(range(10))
    instructions = ["deal with increment 7","deal into new stack",'deal into new stack']
    newdeck = shuffle(deck, instructions)
    assert( [0,3,6,9,2,5,8,1,4,7] == newdeck )
    
    deck = list(range(10))
    instructions = ['cut 6','deal with increment 7','deal into new stack']
    newdeck = shuffle(deck, instructions)
    assert( [3,0,7,4,1,8,5,2,9,6] == newdeck )
    
    deck = list(range(10))
    instructions = ['deal with increment 7', 'deal with increment 9', 'cut -2']
    assert( [6,3,0,7,4,1,8,5,2,9] == shuffle(deck, instructions) )

    deck = list(range(10))
    instructions = ['deal into new stack', 'cut -2', 'deal with increment 7', 'cut 8', 'cut -4', 'deal with increment 7', 'cut 3', 'deal with increment 9', 'deal with increment 3', 'cut -1']
    assert( [9,2,5,8,1,4,7,0,3,6] == shuffle(deck, instructions) )

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip,f.readlines()))

if __name__ == "__main__":
    test1()
    print('Starting shuffle')
    newdeck = shuffle(list(range(10007)), readInput())
    print('Completed shuffle')
    print(newdeck)
    for i in range(len(newdeck)):
        if newdeck[i] == 2019:
            print(i)
    