from SAIS import makeSuftab
from Util import *

def getInput(n):
    S = ''
    S1 = ''
    S2 = ''
    minimalMUMSize = 2

    if n == 1:
        minimalMUMSize = 6
        S1 = b'ATCCGATCATTGGCAGTGCATCGGCGTAACAGTTCCACCGATCTAATGGC'
        S2 = b'CGGCGTTTACTCCGATGGTTGGCAGTGCACCACCGATCTAATGGCCACTG' 

    elif n == 2:
        minimalMUMSize = 6
        S1 = b'ACTGGTAGCCAGTCCGTAATCGATTCGCGAACGTCAGTAATTTGGCCATCGATCC'
        S2 = b'GGCTGGTAGCGTACGATTCGCGCCGTAAACTGGAGGCCATCGATACGTCAGGCCC'

    elif n == 3:
        minimalMUMSize = 5
        S1 = b'ATTCTAGGATTCAAGTCCAGTCGGCCGGAGGAATCGACGTAGCCATTATGCATTC'
        S2 = b'GCAAGTGGAGTAGGAAGGCCGGTTATGCAACTCGACCAAGCCAACTCGGGGCCCC'

    elif n == 4:
        minimalMUMSize = 6
        S1 = b'ACTTAGACTCAACCTGGCTATAATCCGATTCGGCATCACTAACTGACGTAATACG'
        S2 = b'ACCTCCGATTCGGCATCACTAACTGACGTAATACGGTAGTTAGACCATCTGGCTA'

    elif n == 5:
        # output of this example is incorrect because MUMs are overlapping!
        minimalMUMSize = 17
        S1 = b'ACTTCAGTCAGGACTACCGATTAACGATTACGCGATCAAC'
        S2 = b'CAGTCAGGACTACCGATTGGATACCGATTAACGATTACGCGGCTCA'

    else: return getInput(1) # default input 

    S = S1 + b'#' + S2 + b'$'
    splitIndex = len(S1)

    return S1, S2, S, minimalMUMSize, splitIndex



########################################################################
##                                                                    ##
##                       START OF THE PROGRAM                         ##
##                                                                    ##
########################################################################

input = 2
S1, S2, S, minimalMUMSize, splitIndex = getInput(input)

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
maximas.sort(key = lambda t : t[1])
finalMUMs = longestIncreasingSequence(maximas)

(alignedS1, alignedS2) = createAlignedGenomes(S1, S2, finalMUMs)
print('\n', alignedS1)
print('\n', alignedS2, '\n')



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