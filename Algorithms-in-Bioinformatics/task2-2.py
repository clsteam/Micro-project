# -*- coding: utf-8 -*-
import itertools


class Hunter(object):

    def __init__(self, string):
        """
        :param string: "111100"
        由seed的权重weight得到几个1，几个0作为输入
        """
        self.string = string
        self.all_seed = None

    def _get_seed_permutations(self):
        """
        得到所有的seed插入排列组合
        :return:
        """
        return set(itertools.permutations(self.string, len(self.string)))

    def compare(self):
        self.all_seed = list()
        for seed in self._get_seed_permutations():
            judge = True
            for i in range(1, len(seed)):
                """
                i: seed与自身错位i个位子, 例如i=1
                1001011
                 1001011
                number_overlap: 当前seed与自身错位i个位子的seed权重
                    只有1和1算overlap，0和0不算
                """
                number_overlap = (1 if seed[j] == seed[j-i] == "1" else 0 for j in range(i, len(seed)))
                if sum(number_overlap) > 1:
                    judge = False

                    """
                    如果当前seed与自身错位i个位子的seed权重 > 1，则当前seed已经不符合条件不符合，跳出循环
                    """
                    break
            if judge:
                self.all_seed.append(seed)


weight = 4
for i in range(20):
    string = "1" * weight + "0" * i
    h = Hunter(string)
    h.compare()
    if h.all_seed:
        print(string)
        print(h.all_seed)
        break

# Xuqian's Code
# import numpy as np
# def compare(seed):
#     l = len(seed)
#     for i in range(1, l):
#         a = np.zeros(i)
#         a = np.append(a, seed)
#         sum = 0
#         for j in range(i, l):
#             if(a[j] == 1 & seed[j] == 1):
#                 sum += 1
#             if(sum > 1):
#                 return False
#     return True
#
#
# def insert_one_zero(list_a):
#     a = list_a.copy()
#     for i in range(1, len(list_a)):
#         list_a.insert(i, 0)
#         if(i == 1):
#             x = [list_a]
#         else:
#             x.append(list_a)
#         list_a = a.copy()
#     return x
#
#
# if __name__ == '__main__':
#     seed = [1, 1, 1, 1]
#     result = False
#     k = 4  # assume when insert size is 3/4, will get correct answer
#     x = insert_one_zero(seed)
#     y = [[]] + x
#     for i in range(2, k):  # i is insert_size
#         z = [[]]
#         for j in range(1, len(y)):
#             x = insert_one_zero(y[j])
#             z = z + x
#         y = z.copy()
#         for k in range(1, len(y)):
#             result = compare(y[k])
#             if (result == True):
#                 print("final reult is", y[k])
