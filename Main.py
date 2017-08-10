from SAIS import makeSuftab
from Util import *
import sys



def getInputFromFile(fileName):
    """
    Gets required input informations from file.
    """
    inputFile = open(fileName, 'rb')

    minimalMUMSize = int(inputFile.readline().strip())
    S1 = inputFile.readline().strip()
    S2 = inputFile.readline().strip()
    S = S1 + b'#' + S2 + b'$'
    splitIndex = len(S1)

    inputFile.close()

    return S1, S2, S, minimalMUMSize, splitIndex



########################################################################
##                                                                    ##
##                       START OF THE PROGRAM                         ##
##                                                                    ##
########################################################################

# getting input file name 
if len(sys.argv) != 2:
    print('Illegal input! Program takes exactly one argument.')
    exit(1)

S1, S2, S, minimalMUMSize, splitIndex = getInputFromFile(sys.argv[1])
suftab = makeSuftab(S)

# we use ascii character for building suffix table, but for further  
# things we need strings in uft-8 format 
S = S.decode('utf-8')
S1 = S1.decode('utf-8')
S2 = S2.decode('utf-8')

''' part one : finding MUMs '''
lcptab = kasaiLCPTable(S, suftab)
bwttab = bwttabFromSuftab(S, suftab)
maximas = findSupermaximals(lcptab, suftab, bwttab, minimalMUMSize, splitIndex)

#=====================================================================================


#====================================================================================

''' part two : selecting MUMs that create longest increasing sequence '''
maximas.sort(key = lambda t : t[1])
finalMUMs = longestIncreasingSequence(maximas)

''' part three : aligning parts between MUMs '''
(alignedS1, alignedS2) = createAlignedGenomes(S1, S2, finalMUMs)

''' printing results ''' 
print()
print(S1)
print(S2, '\n')
print(alignedS1)
print(alignedS2)
print()





########################################################################
##                                                                    ##
##                          DEBUG    PRINTS                           ##
##                                                                    ##
########################################################################
'''
#formated print for all created datastructures 
# print("\n{0:4s}{1:13s}{2:13s}{4:13s}{3:20s}".format(
#     "i", "suftab[i]", "lcptab[i]", "suffix[i]", "bwttab[i]"))
# for i in range(len(S)):
#     print("{0:<4d}{1:<13d}{2:<13d}{4:13s}{3:20s}".format(
#     i, suftab[i], lcptab[i], S[suftab[i]:], bwttab[i]))
# print()



# for tuple in maximas:
#     mum = S[tuple[1] : tuple[1] + tuple[0]]
#     suffix1 = S[tuple[1]:]
#     suffix2 = S[tuple[2]:]
#     print("\n{0:>20s} :: {1:20s}\n{2:20s} :: {3:20s}\n"
#         .format(mum, suffix1, " ", suffix2))

# print ("\nMUMs: ", finalMUMs)





# printing MUMs
print()
print()
print(' i = |', end = '')
for i in range(max(len(S1), len(S2))):
    print('{:2d}|'.format(i), end = '')
print('\n     ' + '-' * (3 * len(S1) + 1))
print('S1 = |', end = '')
for i in range(len(S1)):
    print('{:>2s}|'.format(S1[i]), end = '')
print('\n     ' + '-' * (3 * len(S2) + 1))
print('S2 = |', end = '')
for i in range(len(S2)):
    print('{:>2s}|'.format(S2[i]), end = '')
print()
print()
print("posInS1 | posInS2 |  MUM")
print('-' * 27)
maximas.sort(key = lambda t : t[1])
for x in maximas:
    print('{:^7d} | {:^7d} | {:s}'.format(x[1], x[2], S1[x[1] : x[1] + x[0]]))
print()



exit(0)



'''


########################################################################
##                                                                    ##
##                          TO  DO  LIST                              ##
##                                                                    ##
########################################################################
'''
-> MUM napravi kao klasu
-> ERROR: example6.txt --> iszbrisi zadnja 4 slova iz drugog niza i dobis error!
-> LIS algoritam probaj napraviti za univerzalni slucaj
-> omoguci FASTA input
-> rjesi preklapanje MUM-ova (pogledaj example5.txt)
-> Smith - Waterman --> pozicija kao klasa
-> bez koristenja utf-8 charseta (cisti charovi)
-> reorganizacija koda (getInputFromFile u Util.py, createAlignedGenomes razbij na poziv vise metoda i sl...)
-> findOverlapping MUMs (Util.py)

'''