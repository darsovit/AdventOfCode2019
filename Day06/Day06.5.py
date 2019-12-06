#! python

def createOrbitGraph( orbits ):
    graph = {}
    graph['Nodes'] = set()
    graph['Edges'] = {}
    for orbit in orbits:
        (orbitee,orbiter) = orbit.split(')')
        graph['Nodes'].add(orbitee)
        graph['Nodes'].add(orbiter)
        graph['Edges'][orbiter] = orbitee
    return graph

def calcOrbitChecksum( graph ):
    count = 0
    for node in graph['Nodes']:
        depth = 0
        parent = node
        while parent in graph['Edges']:
            depth += 1
            parent = graph['Edges'][parent]
        count += depth
    return count

def buildChainSet( graph, sourceNode ):
    chain = set()
    parent = sourceNode
    while parent in graph['Edges']:
        gp = graph['Edges'][parent]
        chain.add(gp)
        parent = gp
    return chain

def calcOrbitTransferDistance(graph, sourceNode, destNode):
    sourceChain = buildChainSet( graph, sourceNode )
    destChain = buildChainSet( graph, destNode )
    sourceChain.symmetric_difference_update( destChain )
    return len(sourceChain)

def test():
    testData = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L','K)YOU','I)SAN']
    graph = createOrbitGraph( testData )
    print( graph )
    print( calcOrbitTransferDistance(graph, 'YOU', 'SAN') )

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

test()
graph = createOrbitGraph( readInput() )
print( calcOrbitChecksum( graph ) )
print( calcOrbitTransferDistance( graph, 'YOU', 'SAN') )