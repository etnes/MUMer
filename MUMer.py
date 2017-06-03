def adHocSuffixArray(source):
    suffixes = []
    for offset in range(len(source)):
        suffixes.append(source[offset:])

    suffixes.sort()

    suffixArray = []
    for suffix in suffixes:
        offset = len(source) - len(suffix)
        suffixArray.append(offset)

    return suffixArray



def adHocLCPTable(source, suftab):
    lcptab = []
    lcptab.append(-1) #lcptab is not defined for first element

    for i in range(1, len(source)):
        lcp = 0
        suffix0 = source[suftab[i - 1]:]
        suffix1 = source[suftab[i]:]

        while(suffix0[lcp] == suffix1[lcp]):
            lcp += 1
        
        lcptab.append(lcp)
    
    return lcptab



def findSupermaximals(lcptab, suftab, bwttab, minimalMUMSize, splitIndex):
    maximas = []

    #searching for supermaximal suffixes
    for i in range(2, len(lcptab) - 1):
        if (lcptab[i] >= minimalMUMSize and bwttab[i] != bwttab[i - 1]):

            #case where suffix of the first string is smaller (in sorting sense)
            if (suftab[i] < splitIndex and suftab[i - 1] > splitIndex):
                maximas.append((lcptab[i], suftab[i], suftab[i - 1] - (splitIndex + 1)))

            #case where suffis of the second string is smaller (in sorting sense)
            elif (suftab[i] > splitIndex and suftab[i - 1] < splitIndex):
                maximas.append((lcptab[i], suftab[i - 1], suftab[i] - (splitIndex + 1)))
    
    return maximas



def bwttabFromSuftab(suftab):
    bwttab = []
    for i in range(len(suftab)):
        if (suftab[i] == 0): 
            bwttab.append(' ')
        else: 
            bwttab.append(S[suftab[i] - 1])
    
    return bwttab



def kasaiLCPTable(S, suftab):
    rank = [None] * len(suftab)

    height = [None] * len(suftab)
    height[0] = -1
    height[1] = 0

    for i in range(len(S)):
        rank[suftab[i]] = i

    h = 0
    for i in range(len(suftab)):
        if rank[i] > 1:
            j = suftab[rank[i] - 1]
            while S[i + h] == S[j + h]:
                h += 1

            height[rank[i]] = h
            if h > 0: h -= 1


    return height
    


def ceilIndex(T, mum, maximas):
    lo = 0
    hi = len(T) - 1
    
    while(lo <= hi):
        mid = (lo + hi) // 2

        if (maximas[T[mid]][2] <= mum[2]):
            lo = mid + 1

        else:
            hi = mid - 1
        
    return lo



def longestIncreasingSequence(maximas):
    T = [0] # T[i] represents index of the smallest element in LIS of length i + 1
    R = [-1] * len(maximas)

    for i in range(1, len(maximas)):
        mum = maximas[i]

        if (mum[2] < maximas[T[0]][2]):
            T[0] = i

        elif (mum[2] > maximas[T[-1]][2]):
            R[i] = T[-1]
            T.append(i)

        else:
            index = ceilIndex(T, mum, maximas)
            print(index)
            R[i] = T[index - 1]
            T[index] = i

    reversedFilteredMUMs = []
    index = T[-1]
    while(index != -1):
        reversedFilteredMUMs.append(maximas[index])
        index = R[index]

    reversedFilteredMUMs.reverse()
    return reversedFilteredMUMs



def SmithWaterman(a, b):
    #TODO -> position kao klasa
    def mutationCost(x, y):
        if (x == y):
            return 2
        
        return -1

    #insertion/deletion cost
    d = -2

    #initializing matrix[a.len + 1][b.len + 1]
    dp = [x[:] for x in [[0] * (len(b) + 1)] * (len(a) + 1)]
    path = [x[:] for x in [[(0, 0)] * (len(b) + 1)] * (len(a) + 1)]

    #initializing path edges
    for i in range(1, len(a) + 1): path[i][0] = (-1, 0)
    for j in range(1, len(b) + 1): path[0][j] = (0, -1)

    #SmithWaterman algorithm (with path reconstruction)
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            #deletion
            deletion = dp[i - 1][j] + d
            dp[i][j] = deletion # if (deletion > 0) else 0
            path[i][j] = (-1, 0)
            
            #insertsion
            insertion = dp[i][j -1] + d
            if (insertion > dp[i][j]):
                dp[i][j] = insertion
                path[i][j] = (0, -1)

            #mutation
            mutation = dp[i - 1][j - 1] + mutationCost(a[i - 1], b[j - 1])
            if (mutation > dp[i][j]):
                dp[i][j] = mutation
                path[i][j] = (-1, -1)

    #reconstruction
    aa = ""
    bb = ""
    position = (len(a), len(b))
    while(position != (0, 0)):
        #TODO -> lista za konkatenaciju stringova
        direction = path[position[0]][position[1]]
        aa = (a[position[0] - 1] if direction[0] == -1 else "-") + aa
        bb = (b[position[1] - 1] if direction[1] == -1 else "-") + bb
        
        position = (position[0] + direction[0], position[1] + direction[1])

    return (aa, bb)



def createAlignedGenomes(S1, S2, MUMs):
    alignedS1 = ""
    alignedS2 = ""

    startIndex1 = 0
    startIndex2 = 0

    for mum in MUMs:
        #first we concat part that is located before mum using SmithWaterman algorithm
        (part1, part2) = SmithWaterman(S1[startIndex1:mum[1]], S2[startIndex2:mum[2]])

        #TODO -> zajednicki substring? (da ne vuces dva puta isti substring)
        alignedS1 += part1 + " [ " + S1[mum[1]:mum[1] + mum[0]] + " ] "
        alignedS2 += part2 + " [ " + S2[mum[2]:mum[2] + mum[0]] + " ] "

        startIndex1 = mum[1] + mum[0]
        startIndex2 = mum[2] + mum[0]

    #final appending
    (part1, part2) = SmithWaterman(S1[startIndex1:], S2[startIndex2:])
    alignedS1 += part1
    alignedS2 += part2

    return (alignedS1, alignedS2) 








########################################################################
##                                                                    ##
##                       START OF THE PROGRAM                         ##
##                                                                    ##
########################################################################

# SIMPLE EXAMPLES
# S = 'BANANA$'
# S = 'ACAAACATAT$'

# S1 = 'CCAGCTTATCTAGCTTATCTG'
# S2 = 'CGCTTATCTCCGATACGGCAA'

# S1 = 'CGATTAGCTTAGG'
# S2 = 'TAGCTCCTTAGCC'

#example1
# minimalMUMSize = 6
# S1 = 'ATCCGATCATTGGCAGTGCATCGGCGTAACAGTTCCACCGATCTAATGGC'
# S2 = 'CGGCGTTTACTCCGATGGTTGGCAGTGCACCACCGATCTAATGGCCACTG'

#example2
# minimalMUMSize = 6
# S1 = 'ACTGGTAGCCAGTCCGTAATCGATTCGCGAACGTCAGTAATTTGGCCATCGATCC'
# S2 = 'GGCTGGTAGCGTACGATTCGCGCCGTAAACTGGAGGCCATCGATACGTCAGGCCC'

#example3
# minimalMUMSize = 5
# S1 = 'ATTCTAGGATTCAAGTCCAGTCGGCCGGAGGAATCGACGTAGCCATTATGCATTC'
# S2 = 'GCAAGTGGAGTAGGAAGGCCGGTTATGCAACTCGACCAAGCCAACTCGGGGCCCC'

#example4
# minimalMUMSize = 6
# S1 = 'ACTTAGACTCAACCTGGCTATAATCCGATTCGGCATCACTAACTGACGTAATACG'
# S2 = 'ACCTCCGATTCGGCATCACTAACTGACGTAATACGGTAGTTAGACCATCTGGCTA'

#example5
# minimalMUMSize = 17
# S1 = 'ACTTCAGTCAGGACTACCGATTAACGATTACGCGATCAAC'
# S2 = 'CAGTCAGGACTACCGATTGGATACCGATTAACGATTACGCGGCTCA'

S = S1 + '#' + S2 + '$'
splitIndex = len(S1)

#data structures
suftab = adHocSuffixArray(S)
lcptab = adHocLCPTable(S, suftab)
lcptab = kasaiLCPTable(S, suftab)
bwttab = bwttabFromSuftab(suftab)
maximas = findSupermaximals(lcptab, suftab, bwttab, minimalMUMSize, splitIndex)

# print("\n{0:4s}{1:13s}{2:13s}{4:13s}{3:20s}".format(
#     "i", "suftab[i]", "lcptab[i]", "suffix[i]", "bwttab[i]"))
# for i in range(len(S)):
#     print("{0:<4d}{1:<13d}{2:<13d}{4:13s}{3:20s}".format(
#     i, suftab[i], lcptab[i], S[suftab[i]:], bwttab[i]))
# print()

maximas.sort(key = lambda t : t[1])
# print (maximas)

# for tuple in maximas:
#     mum = S[tuple[1] : tuple[1] + tuple[0]]
#     suffix1 = S[tuple[1]:]
#     suffix2 = S[tuple[2]:]
#     print("\n{0:>20s} :: {1:20s}\n{2:20s} :: {3:20s}\n"
#         .format(mum, suffix1, " ", suffix2))


finalMUMs = longestIncreasingSequence(maximas)
print ("\nMUMs: ", finalMUMs)


(alignedS1, alignedS2) = createAlignedGenomes(S1, S2, finalMUMs)
(SW1, SW2) = SmithWaterman(S1, S2)

print()
print(alignedS1)
print(alignedS2)
print()
print(SW1)
print(SW2)
print()


#TODO -> struktura za final MUM (odnosno struktura mum)