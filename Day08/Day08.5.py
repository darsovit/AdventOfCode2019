#! python

def readInput():
    with open('input.txt') as f:
        inputText = list(map(str.rstrip, f.readlines()))
        assert( 1 == len(inputText) )
        return list( map(int, list( inputText[0] ) ) )

def splitImageToLayers( imageData, width, height ):
    fullSize = len(imageData)
    layerSize = width * height
    assert( fullSize % layerSize == 0 )
    layers = []
    for i in range( int(fullSize/layerSize) ):
        layer = imageData[i*layerSize:(i+1)*layerSize]
        #print( i, layer )
        layers += [layer]
    return layers

def countNumInLayer(layer, num):
    count = 0
    total = 0
    for datum in layer:
        if datum == num:
            count += 1
        total += 1
    #print( 'countNumInLayer: ', count, ', total:', total )
    return count
    
def findFewestZerosInLayers( layers ):
    fewestZeros = None
    layerNo   = None
    for i in range(len(layers)):
        numZeros = countNumInLayer( layers[i], 0 )
        if not fewestZeros or numZeros < fewestZeros:
            fewestZeros = numZeros
            layerNo = i
    return layerNo

def test():
    imageData = [1,2,3,4,5,6,7,8,9,0,1,2]
    assert( [[1,2,3,4,5,6],[7,8,9,0,1,2]] == splitImageToLayers(imageData, 3, 2) )
    
def decodeImage( layers, width, height ):
    finalImage = layers[0]
    for i in range( 1, len(layers) ):
        for j in range( len(finalImage) ):
            if finalImage[j] == 2:
                finalImage[j] = layers[i][j]
    return finalImage
    
def renderImage( layer, width, height ):
    for i in range( height ):
        image = list( map(str, layer[i*width:(i+1)*width]) )
        print( ''.join(image) )
       

test()
print("Test complete")

layers = splitImageToLayers(readInput(), 25, 6)
finalImage = decodeImage( layers, 25, 6 )
renderImage( finalImage, 25, 6 )

    