import Util
import SAIS

input = [4, 7, 1, 2, 0, 4, 8, 2, 9]
Util.longestIncreasingSequence(input)

S = "BANANA$"
result = SAIS.buildTypeMap(S)

print()
for i in range(len(S)):
    print(S[i], end = '  ')
print()

for i in range(len(S)):
    print('|', end = '  ')
print()

for i in range(len(S)):
    print(chr(result[i]), end = ' e ')
print()
print()