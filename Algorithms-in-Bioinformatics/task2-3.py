# import itertools
#
# seed = "1111000"
# result = itertools.permutations(seed, len(seed))
# x = set(result)
# print(x)
# print(len(x))

import numpy as np
S = "TGTATCTG"
T = "GTTGCATC"
insert_score = deletion_score = -1
mismatch_score = -1
match_score = 2


def xxx(a, b):
    if a == b:
        return match_score
    else:
        return mismatch_score


my_array = np.zeros((len(S) + 1, len(T) + 1))
for i in range(1, len(S) + 1):
    for j in range(1, len(T) + 1):
        insertion = my_array[i - 1, j] + insert_score
        deletion = my_array[i, j - 1] + deletion_score
        my_array[i, j] = max(my_array[i-1, j-1] + xxx(S[i-1], T[j-1]), insertion, deletion)
print(my_array)
