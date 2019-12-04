#! python

def contains6digits( password ):
    return len(password) == 6

def hasTwoAdjacentDigitsSame( password ):
    return ( password[0] == password[1]
          or password[1] == password[2]
          or password[2] == password[3]
          or password[3] == password[4] 
          or password[4] == password[5] )
          
def alwaysIncreases( password ):
    return ( password[5] >= password[4]
          and password[4] >= password[3]
          and password[3] >= password[2]
          and password[2] >= password[1]
          and password[1] >= password[0] )
          
def validPassword( password ):
    return ( contains6digits( password )
         and hasTwoAdjacentDigitsSame( password )
         and alwaysIncreases( password ) )

validPasswordCount = 0
for password in range( 254032,789861 ):
    if validPassword( str( password ) ):
        validPasswordCount += 1

print( validPasswordCount )