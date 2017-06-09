S_TYPE = ord('S')
L_TYPE = ord('L')

def buildTypeMap(source):
    """
    Builds a map marking each suffix of the data as S_TYPE of L_TYPE.
    """

    typemap = bytearray(len(source))

    #we know that last charactes is always S type
    typemap[-1] = S_TYPE
    
    for i in range(len(source) - 2, -1, -1):
        if source[i] > source[i + 1]:
            typemap[i] = L_TYPE
        elif source[i] == source[i + 1] and  typemap[i + 1] == L_TYPE:
            typemap[i] = L_TYPE
        else:
            typemap[i] = S_TYPE

    return  typemap


def isLMSChar(offset, typemap):
    """
    Retruns true if the character at the given offset is 
    left-most S-type character.
    """

    #first character can't be LMS char
    if offset <= 0: 
        return False
    if typemap[offset] == S_TYPE and typemap[offset - 1] == L_TYPE: 
        return True

    return False



def lmsSubstringAreEqual(string, typemap, offsetA, offsetB):
    """
    Returns True if LMS substring at offsetA and offsetB are euqal.
    """

    #if one of the substring is last '$', then we know that substrings
    #cant be equal
    if offsetA == len(string) or offsetB == len(string):
        return False

    i = 0
    while True:
        aIsLMS = isLMSChar(i + offsetA, typemap)
        bIsLMS = isLMSChar(i + offsetB, typemap)

        # if we found the start of the next LMS substring
        # then we found equal substrings
        if (i > 0 and aIsLMS and bIsLMS):
            return True

        # substring has difference
        if aIsLMS != bIsLMS:
            return False

        # substings has different character, so they are not equal
        if string[i + offsetA] != string[i + offsetB]:
            return False

        i += 1



def findBucketSizes(string, alphabetSize = 256):
    res = [0] * alphabetSize

    for char in string:
        res[char] += 1

    return res



def findBucketHeads(bucketSizes):
    offset = 0
    res = []

    for size in bucketSizes:
        res.append(offset)
        offset += size

    return res



def findBucketTails(bucketSizes):
    offset = 0
    res = []
    for size in bucketSizes:
        offset += size
        res.append(offset - 1)

    return res



def guessLMSSort(string, bucketSizes, typemap):
    """
    Make a suffix array with LMS-substrings approximately right.
    """

    guessedSuffixArray = [-1] * len(string)

    bucketTails = findBucketTails(bucketSizes)

    # bucket sort all the LMS suffices into their bucket
    for i in range(len(string)):
        # not start of the LMS suffix
        if not isLMSChar(i, typemap):
            continue

        bucketIndex = string[i]
        guessedSuffixArray[bucketTails[bucketIndex]] = i
        bucketTails[bucketIndex] -= 1

    return guessedSuffixArray



def induceSortL(string, guessedSuffixArray, bucketSizes, typemap):
    """
    Slot L-type suffixes into place.
    """

    bucketHeads = findBucketHeads(bucketSizes)

    # for each cell in suffix array
    for i in range(len(guessedSuffixArray)):
        if guessedSuffixArray[i] == -1: 
            continue

        # index of neighbour suffix left to the current one
        j = guessedSuffixArray[i] - 1

        if j < 0 or typemap[j] != L_TYPE:
            continue
        
        bucketIndex = string[j]
        guessedSuffixArray[bucketHeads[bucketIndex]] = j
        bucketHeads[bucketIndex] += 1

        

def induceSortS(string, guessedSuffixArray, bucketSizes, typemap):
    """
    Slot S-type suffixes into place.
    """

    bucketTails = findBucketTails(bucketSizes)

    # for each cell in suffix array
    for i in range(len(guessedSuffixArray) - 1 , -1, -1):
        # index of neighbour suffix left to the current one
        j = guessedSuffixArray[i] - 1

        if j < 0 or typemap[j] != S_TYPE:
            continue
        
        bucketIndex = string[j]
        guessedSuffixArray[bucketTails[bucketIndex]] = j
        bucketTails[bucketIndex] -= 1
        


def summariseSuffixArray(string, guessedSuffixArray, typemap):
    """
    Construct a 'summary string' of the positions of LMS substrings.
    """

    # initialization
    lmsNames = [-1] * (len(string))
    currentName = 1
    lastLMSSuffixOffset = None

    # first suffix is always sentinel ('$' char)
    lmsNames[guessedSuffixArray[0]] = currentName
    lastLMSSuffixOffset = guessedSuffixArray[0]

    for i in range(1, len(guessedSuffixArray)):
        suffixOffset = guessedSuffixArray[i]

        # we are looking only for LMS sufficex
        if not isLMSChar(suffixOffset, typemap):
            continue

        if not lmsSubstringAreEqual(
            string, typemap, lastLMSSuffixOffset, suffixOffset):
            currentName += 1

        # remember the last LMS suffix we looked at
        lastLMSSuffixOffset = suffixOffset

        # store the name of this LMS suffix in lmsNames in the same
        # place this suffix occurs in the original string.
        lmsNames[suffixOffset] = currentName

    summarySuffixOffsets = []
    summaryString = []

    for index, name in enumerate(lmsNames):
        if name == -1:
            continue
        
        summarySuffixOffsets.append(index)
        summaryString.append(name)
        
    # we add 0 as a sentinel
    summaryString.append(0)

    summaryAlphabetSize = currentName + 1

    return summaryString, summaryAlphabetSize, summarySuffixOffsets



def makeSummarySuffixArray(summaryString, summaryAlphabetSize):
    """
    construct a sorted suffix array of the summary string.
    """

    if summaryAlphabetSize == len(summaryString):
        # every character of this summary string appears once and only 
        # once, se we can make the suffix array with a bucket sort.
        summarySuffixArray = [-1] * (len(summaryString) + 1)

        # sentinel '$'
        summarySuffixArray[0] = len(summaryString)

        for x in range(len(summaryString)):
            y = summaryString[x]
            summarySuffixArray[y] = x

    else:
        # otherwise, we have to do recursion
        summarySuffixArray = makeSuffixArrayByInducedSorting(
            summaryString,
            summaryAlphabetSize
        )
        
    return summarySuffixArray



def accurateLMSSort(string, bucketSizes, typemap, 
    summarySuffixArray, summarySuffixOffsets):
    """
    Makes a suffix array with LMS suffixes exactly right.
    """

    suffixOffsets = [-1] * len(string)

    bucketTails = findBucketTails(bucketSizes)
    for i in range(len(summarySuffixArray) - 1, 0, -1):
        stringIndex = summarySuffixOffsets[summarySuffixArray[i]]

        bucketIndex = string[stringIndex]
        suffixOffsets[bucketTails[bucketIndex]] = stringIndex
        bucketTails[bucketIndex] -= 1

    return suffixOffsets



########################################################################
##                                                                    ##
##                        SA - IS   ALGORITHM                         ##
##                                                                    ##
########################################################################

def makeSuffixArrayByInducedSorting(string, alphabetSize):
    """
    Comnpute the suffix array of the given string with SA-IS algorithm.
    """

    # classify each character of the string as S-YTPE or L-TYPE
    typemap = buildTypeMap(string)

    # slots suffixes into the buckets according to their start character
    bucketSizes = findBucketSizes(string, alphabetSize)

    # By using simple bucket sort, we insert all the LMS suffixes into 
    # approximately the right place in the suffix array
    guessedSuffixArray = guessLMSSort(string, bucketSizes, typemap)

    # slot all the other suffixes into guessedSuffixArray by using induce sorting.
    induceSortL(string, guessedSuffixArray, bucketSizes, typemap)
    induceSortS(string, guessedSuffixArray, bucketSizes, typemap)

    # create a new string that summarises the relative order of the LMS 
    # suffixes in the guessed suffix array.
    summaryString, summaryAlphabetSize, summarySuffixOffsets = \
        summariseSuffixArray(string, guessedSuffixArray, typemap)

    # make a sorted suffix array of the summary string.
    summarySuffixArray = makeSummarySuffixArray(
        summaryString, summaryAlphabetSize)

    # using the suffix array of the summary string, determine exactly
    # where the LMS suffixes should go in our final array.
    result = accurateLMSSort(string, bucketSizes, typemap, 
        summarySuffixArray, summarySuffixOffsets)

    # slotting all the other suffixes into place
    induceSortL(string, result, bucketSizes, typemap)
    induceSortS(string, result, bucketSizes, typemap)

    return result



def makeSuftab(source):
    """
    Creats suffix array from the given text with default
    alphabet size of 256 (we use ascii characters)
    """
    return makeSuffixArrayByInducedSorting(source, 256)