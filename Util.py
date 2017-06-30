def findSupermaximals(lcptab, suftab, bwttab, minimalMUMSize, splitIndex):
    """
    Method that finds and filters all substring matches that occur in first 
    and second genome, and return just the logest ones. All mathces that are too 
    short or occur in just one genome are ignored. Final array contains tuples 
    where first element is the lenght of the substring, second parameter is 
    start position in first genome, and third parameter is the position in 
    second genome.
    """

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



def bwttabFromSuftab(S, suftab):
    """
    Creates burrows wheeler transormation table in linear time from the given
    suffix table. 
    """

    bwttab = []
    for i in range(len(suftab)):
        if (suftab[i] == 0): 
            bwttab.append('$')
        else: 
            bwttab.append(S[suftab[i] - 1])
    
    return bwttab



def kasaiLCPTable(S, suftab):
    """
    Creates longest common prefix table from the given suffix table 
    in linear time by using kasai algorithm. 
    """

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
    """
    Method takes list of maximas (tuple of (MUM_lenght, position_in_S1, position_in_S2))
    that are sorted ascending by the position_in_S1.
    Algorithm finds longest increasing sequnce of the array represented by 
    the positio_in_S2.
    """

    # T[i] represents index of the smallest element in LIS of length i + 1 
    T = [0] # initialization
    R = [-1] * len(maximas) # used to reconstruct LIS
    L = [0] * len(maximas) # stores length of LIS that ends in i-th element
    L[0] = maximas[0][0] # initialization

    for i in range(1, len(maximas)):
        mum = maximas[i]

        if (mum[2] < maximas[T[0]][2]):
            L[i] = mum[0]
            T[0] = i

        elif (mum[2] > maximas[T[-1]][2]):
            R[i] = T[-1]
            L[i] = L[T[-1]] + mum[0]
            T.append(i)

        else:
            index = ceilIndex(T, mum, maximas)
            R[i] = T[index - 1]
            L[i] = L[T[index - 1]] + mum[0]
            T[index] = i

    # looking for a longest increasing sequence (not neccessery with most MUMs)
    # but the one that is the longest
    index = 0;
    for i in reversed(range(1, len(L))):
        if (L[i] > L[index]):
            index = i

    reversedFilteredMUMs = []

    # reconstruct sequence  
    while(index != -1):
        reversedFilteredMUMs.append(maximas[index])
        index = R[index]

    reversedFilteredMUMs.reverse()
    return reversedFilteredMUMs



def filterOverlappingMUMs(MUMs):
    '''
    Removes MUMs that are overlapping. Method naively filters MUMs with following cases:
    
    1st case: if two MUMs are overlaping, the longer MUM is selected

    2nd case: if first MUM overlaps with the second one, and the second one is
    overlapping with the third one, then the first MUM is selected and the second
    one is skipped.
    '''

    filteredMUMs = []
    skipNextMUM = false

    length = len(MUMs)
    for i in range(length):
        if i + 1 < length:
            pass
            #2nd case
            # if i + 2 < len: ... TO BE CONTINUED ... 





def createAlignedGenomes(S1, S2, MUMs):
    """ 
    Creates final string that is concatenation of the MUMs and aligned 
    parts between MUMs.
    """

    alignedS1 = ""
    alignedS2 = ""

    startIndex1 = 0
    startIndex2 = 0

    for mum in MUMs:
        #first we concat part that is located before mum using SmithWaterman algorithm
        (part1, part2) = SmithWaterman(S1[startIndex1:mum[1]], S2[startIndex2:mum[2]])

        alignedS1 += part1 + " [ " + S1[mum[1]:mum[1] + mum[0]] + " ] "
        alignedS2 += part2 + " [ " + S2[mum[2]:mum[2] + mum[0]] + " ] "

        startIndex1 = mum[1] + mum[0]
        startIndex2 = mum[2] + mum[0]

    #final appending of the parts of the genome that comes after last MUM
    (part1, part2) = SmithWaterman(S1[startIndex1:], S2[startIndex2:])
    alignedS1 += part1
    alignedS2 += part2

    return (alignedS1, alignedS2) 



def SmithWaterman(a, b):
    """
    Method takes two strings, a and b, and aligne them by using 
    Smith Watherman algorithm for local alignment. Insertion and deletion 
    penalizing are simplifyed and their score is set to default value of -2. 
    Scores for mutation and hits are determine in inner method 'mutationCost'. 
    """

 

    def mutationCost(x, y):
        """
        Returns score for alignemnt of two given bases. Default value for 
        hits is set to 2 and default value of miss (mutation) is set to -1.
        """

        hitScore = 2
        missScore = -1

        if (x == y):
            return hitScore
        
        return missScore

    #insertion/deletion socre
    insDelScore = -2

    #initializing matrices to size [a.len + 1][b.len + 1]
    dp = [x[:] for x in [[0] * (len(b) + 1)] * (len(a) + 1)]
    path = [x[:] for x in [[(0, 0)] * (len(b) + 1)] * (len(a) + 1)]

    #initializing path edges
    for i in range(1, len(a) + 1): path[i][0] = (-1, 0)
    for j in range(1, len(b) + 1): path[0][j] = (0, -1)

    #SmithWaterman algorithm (with path reconstruction)
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            #deletion
            deletion = dp[i - 1][j] + insDelScore
            dp[i][j] = deletion # if (deletion > 0) else 0
            path[i][j] = (-1, 0)
            
            #insertsion
            insertion = dp[i][j -1] + insDelScore
            if (insertion > dp[i][j]):
                dp[i][j] = insertion
                path[i][j] = (0, -1)

            #mutation
            mutation = dp[i - 1][j - 1] + mutationCost(a[i - 1], b[j - 1])
            if (mutation > dp[i][j]):
                dp[i][j] = mutation
                path[i][j] = (-1, -1)

    #reconstruction of the path
    aa = ""
    bb = ""
    position = (len(a), len(b))
    while(position != (0, 0)):
        #TODO -> list of concatenating elements insted of string concatenation.
        direction = path[position[0]][position[1]]
        aa = (a[position[0] - 1] if direction[0] == -1 else "-") + aa
        bb = (b[position[1] - 1] if direction[1] == -1 else "-") + bb
        
        position = (position[0] + direction[0], position[1] + direction[1])

    return (aa, bb)