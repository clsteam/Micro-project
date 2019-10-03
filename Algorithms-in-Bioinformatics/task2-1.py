#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author  : Yao

""" Title

This file(script) can also be imported as a module and contains the following
functions:

    * main - the main function of the script
    * function - returns the column headers of the file
"""

# Standard library

# Third party library

# Private module
import matplotlib.pyplot as plt


class Pos(object):

    def __init__(self, s, t, hit, x, match_score=5, mismatch_score=-4):
        """
        :param s: "TCTCACCGTGCACGACATC"
        :param t: "CGGAACTGTGAACAATCCT"
        :param hit: "GTG"
        """
        self.s = s
        self.t = t
        self.hit = hit
        self.x = x
        self.match_score = match_score
        self.mismatch_score = mismatch_score

        # 初始化
        self.l = self.t.index(hit)
        self.r = self.t.index(hit) + len(hit) - 1
        self.msp = [len(self.hit) * self.match_score, self.l, self.r]
        self.score = [self.msp[0], ]

    def match(self, a, b):
        if a == b:
            return self.match_score
        else:
            return self.mismatch_score

    def _print(self):
        print("-" * (len(self.t) + 2))
        print("S:{0}".format(self.s))
        print("T:{0}".format(" " * self.l + self.t[self.l:self.r + 1]))

    def stop(self):
        self._print()
        if (self.l == 0) and (self.r == len(self.t) - 1):
            return True
        if self.msp[0] - self.score[-1] > self.x:
            return True
        return False

    def move_left(self):
        """
        从T的左边移一个位子，并且修改相应的值
        :return:
        """
        if self.l == 0:
            self.move_right()
        else:
            self.l -= 1
            self.score.append(self.score[-1] + self.match(self.s[self.l], self.t[self.l]))
            if self.score[-1] > self.msp[0]:
                self.msp = [self.score[-1], self.l, self.r]

    def move_right(self):
        """
        从T的右边移一个位子，并且修改相应的值
        :return:
        """
        if self.r == len(self.t) - 1:
            self.move_left()
        else:
            self.r += 1
            self.score.append(self.score[-1] + self.match(self.s[self.r], self.t[self.r]))
            if self.score[-1] > self.msp[0]:
                self.msp = [self.score[-1], self.l, self.r]

    def move(self):
        """
        左右同时移动！
        :return:
        """
        if self.r == len(self.t) - 1 or self.l == 0:
            self.move_left()
        else:
            self.r += 1
            self.l -= 1
            self.score.append(self.score[-1] + self.match(self.s[self.r], self.t[self.r]) + self.match(self.s[self.l], self.t[self.l]))
            if self.score[-1] > self.msp[0]:
                self.msp = [self.score[-1], self.l, self.r]


if __name__ == '__main__':
    S = "TCTCACCGTGCACGACATC"
    T = "CGGAACTGTGAACAATCCT"
    hit = "GTG"
    X = 13
    pos = Pos(S, T, hit, X)
    while not pos.stop():
        pos.move()
    print("MSP: {0}\tscore:{1}".format(pos.t[pos.msp[1]:(pos.msp[2]+1)], pos.msp[0]))
    print(pos.score)

# Data for plotting

fig, ax = plt.subplots()
plt.stem(range(len(pos.score)), pos.score)

ax.set(xlabel='extend', ylabel='score',
       title='extending')
ax.grid()

plt.show()

