#! python
#
# http://adventofcode.com/2019/day/14
#
#

def calculateDepths(graph, zeroElements):
    currentDepth = 0
    currentIngredients = set()
    for element in zeroElements:
        graph['depth'][element] = 0
        (ingredients,leftovers) = getIngredientsFor(graph, element, 1)
        for ingredient in ingredients:
            currentIngredients.add(ingredient)
    #print(currentIngredients)
    while( hasReactionsAvailable(graph, currentIngredients ) ):
        nextIngredients = currentIngredients.copy()
        #print(nextIngredients)
        currentIngredients = set()
        #print(nextIngredients)
        currentDepth       += 1
        for element in nextIngredients:
            #print(element)
            graph['depth'][element] = currentDepth
            (ingredients,leftovers) = getIngredientsFor( graph, element, 1)
            for ingredient in ingredients:
                currentIngredients.add(ingredient)
        #print(currentIngredients)
    for element in currentIngredients:
        currentDepth += 1
        graph['depth'][element] = currentDepth

def buildWeightedGraph( input ):
    graph = {}
    graph['elementNodes'] = set()
    ingredients = set()
    graph['depth'] = {}
    graph['reactionNodes'] = []
    #graph['outputNodes'] = {}
    graph['edges'] = {}
    for reaction in input:
        (inputsstr,outputstr) = reaction.split(' => ')
        inputstrlist = inputsstr.split(', ')
        graph['reactionNodes'] += [reaction]
        (outputWeight,outputElement) = outputstr.split(' ')
        graph['edges'][outputElement] = (reaction, int(outputWeight))
        graph['edges'][reaction] = []
        graph['elementNodes'].add(outputElement)
        for inputstr in inputstrlist:
            (inputWeight,inputElement) = inputstr.split(' ')
            graph['elementNodes'].add(inputElement)
            ingredients.add(inputElement)
            graph['edges'][reaction] += [(inputElement,int(inputWeight))]
    calculateDepths(graph, graph['elementNodes'].difference(ingredients))
    return graph

def hasReactionAvailable(graph, element):
    return element in graph['edges']

def hasReactionsAvailable( graph, requiredList ):
    for required in requiredList:
        if hasReactionAvailable(graph, required):
            return True
    return False

def getIngredientsFor(graph, element, units):
    if element in graph['edges']:
        (reaction,produced) = graph['edges'][element]
        ingredients = {}
        multiplier = 1
        if produced < units:
            multiplier = int( units / produced )
            if produced * multiplier < units:
                multiplier += 1
            assert( multiplier * produced >= units )
        for ingredient in graph['edges'][reaction]:
            ingredients[ingredient[0]] = multiplier * ingredient[1]
        return (ingredients,(multiplier*produced) - units)
    else:
        return ([],0)

def calcOrePerFuel( input ):
    graph = buildWeightedGraph( input )
    print( graph )
    spares = {}
    required = {}
    required['FUEL'] = 1
    currentDepth = 0
    while( hasReactionsAvailable( graph, required.keys() ) ):
        print('depth:', currentDepth)
        newRequirements = {}
        for element in required:
            print("\tNeed: {} {} ({})".format(required[element],element,graph['depth'][element]))
            if graph['depth'][element] == currentDepth:
                
                if element in spares:
                    print("\t\tUNEXPECTED, but we HAVE some of",element,"left over:", spares[element])
                    if spares[element] > required[element]:
                        spares[element] -= required[element]
                        if spares[element] == 0:
                            del spares[element]
                        continue
                    else:
                        required[element] = required[element]-spares[element]
                        del spares[element]
                if hasReactionAvailable( graph, element ):
                    (ingredsForFuel,extra) = getIngredientsFor( graph, element, required[element] )
                    print("\tIngredients for {} {}: {}".format(required[element],element,graph['edges'][element]))
                    if extra > 0:
                        if element not in spares:
                            spares[element] = 0
                        spares[element] += extra
                        print("\t\tSpare {}: {} -> {}".format(element, extra, spares[element]))
                    for ingredForFuel in ingredsForFuel:
                        if ingredForFuel not in newRequirements:
                            newRequirements[ingredForFuel] = 0
                        newRequirements[ingredForFuel] += ingredsForFuel[ingredForFuel]
                        print('\t\t{}: {} -> {}'.format(ingredForFuel, ingredsForFuel[ingredForFuel], newRequirements[ingredForFuel]) )
                else:
                    if element not in newRequirements:
                        newRequirements[element] = 0
                    newRequirements[element] += required[element]
                    print('\t\t{}: {} -> {}'.format(element,required[element],newRequirements[element]))
            else:
                if element not in newRequirements:
                    newRequirements[element] = 0
                newRequirements[element] += required[element]
        currentDepth += 1
        required = newRequirements
    print( required )
    assert( 'ORE' in required )
    assert( len(required) == 1 )
    return( required['ORE'] )
 
def readInput():
    with open('input.txt') as f:
        return list( map( str.rstrip, f.readlines() ) )

def test1Input():
    return (31, [ '10 ORE => 10 A', '1 ORE => 1 B', '7 A, 1 B => 1 C', '7 A, 1 C => 1 D', '7 A, 1 D => 1 E', '7 A, 1 E => 1 FUEL' ])

def test():
    ( expected, input ) = test1Input()
    assert( expected == calcOrePerFuel( input ) )
    
test()

print( calcOrePerFuel( readInput() ) )
### 2622156 is too high