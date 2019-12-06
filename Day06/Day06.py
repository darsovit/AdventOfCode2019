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

def test():
    testData = ['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L']
    graph = createOrbitGraph( testData )
    print( calcOrbitChecksum( graph ) )
    print( graph )

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

test()
print( calcOrbitChecksum( createOrbitGraph( readInput() ) ) )