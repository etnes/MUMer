from SAIS import makeSuftab
from Util import *
import sys



def getInputFromFile(fileName):
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
if (len(sys.argv) != 2):
    print('Illegal input! Program takes exactly one argument.')
    exit(1)

S1, S2, S, minimalMUMSize, splitIndex = getInputFromFile(sys.argv[1])

suftab = makeSuftab(S)

# we use ascii character for building suffix table, but for further  
# things we need strings in uft-8 format 
S = S.decode('utf-8')
S1 = S1.decode('utf-8')
S2 = S2.decode('utf-8')

lcptab = kasaiLCPTable(S, suftab)
bwttab = bwttabFromSuftab(S, suftab)
maximas = findSupermaximals(lcptab, suftab, bwttab, minimalMUMSize, splitIndex)

# filteriing MUMs 
#for sorting can be used linear time radix sort
maximas.sort(key = lambda t : t[1])
finalMUMs = longestIncreasingSequence(maximas)

(alignedS1, alignedS2) = createAlignedGenomes(S1, S2, finalMUMs)
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

#formated print for all created datastructures 
# print("\n{0:4s}{1:13s}{2:13s}{4:13s}{3:20s}".format(
#     "i", "suftab[i]", "lcptab[i]", "suffix[i]", "bwttab[i]"))
# for i in range(len(S)):
#     print("{0:<4d}{1:<13d}{2:<13d}{4:13s}{3:20s}".format(
#     i, suftab[i], lcptab[i], S[suftab[i]:], bwttab[i]))
# print()

# print (maximas)

# for tuple in maximas:
#     mum = S[tuple[1] : tuple[1] + tuple[0]]
#     suffix1 = S[tuple[1]:]
#     suffix2 = S[tuple[2]:]
#     print("\n{0:>20s} :: {1:20s}\n{2:20s} :: {3:20s}\n"
#         .format(mum, suffix1, " ", suffix2))

# print ("\nMUMs: ", finalMUMs)

#TODO -> MUM structure/class