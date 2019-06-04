#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author  : Yao

""" Algorithm in bioinformatics
Dependency package:
    Package    Version
    ---------- -------
    biopython  1.73
    numpy      1.16.4

The functional classes included in the script
    * GlobalAlign:
        - Model: Affine gap model
        - Additional parameters: Slope = Gap penalty/Gap size
"""

# Standard library
import sys
import os
import collections
import itertools
import logging
import textwrap

# Third party library
from Bio.SeqIO.FastaIO import SimpleFastaParser
import numpy as np


# 日志输出
logger_1 = logging.getLogger("GlobalAlign")
loggers = (logger_1, )
try:
    import coloredlogs
    for logger in loggers:
        coloredlogs.install(logger=logger_1, level='INFO')  # INFO
except ImportError:
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.DEBUG)

# Recursive depth limit	修改递归深度限制
sys.setrecursionlimit(10000)  # 10000 is an example, try with different values
# Memory limit 修改内存大小限制
if os.name == "posix":  # Linux
    os.system("ulimit -Sv 250000")
elif os.name == "nt":  # Windows
    pass
else:
    pass


class ParameterError(Exception):
    pass

# from collections import defaultdict
# import weakref
# class KeepRefs(object):
#     """
#     reference：https://stackoverflow.com/questions/328851/printing-all-instances-of-a-class#comment167339_328851
#     """
#     __refs__ = defaultdict(list)
#
#     def __init__(self):
#         self.__refs__[self.__class__].append(weakref.ref(self))
#
#     @classmethod
#     def get_instances(cls):
#         for inst_ref in cls.__refs__[cls]:
#             inst = inst_ref()
#             if inst is not None:
#                 yield inst


class ResultSeq(object):
    """
    存储比对的结果（two reads）
    """
    _all_instances = []

    def __init__(self, seq1="", seq2=""):
        self._all_instances.append(self)
        self.seq1 = seq1
        self.seq2 = seq2

    def del_ins(self):
        """
        delete instance
        """
        self._all_instances.remove(self)


class ExternalParameters(object):
    """
    This class is used to read external input in a specific format.
        such as the parameters file.
    """
    def __init__(self, file):
        """
        :param file: parameters file, format like this:
            0; score for initiating a gap
            -1; score for each base insert/delete

            ; Below is the alphabet
            a c g t

            ; Below is the similarity matrix for the alphabet
            2 -1 -1 -1
            -1 2 -1 -1
            -1 -1 2 -1
            -1 -1 -1 2
        """
        self.gap_init_score = None
        self.indel_score = None
        self.list_alphabet = None
        self.similarity_matrix = None
        i = 0
        with open(file, "r") as handle:
            """
            count:
                * ?: 已经读到第?个parameter啦
            """
            count = 1
            for line in handle:
                if not line.strip():  # 空行跳过
                    continue
                else:
                    if count == 1:
                        self.gap_init_score = float(line.split(";")[0])
                        count = 2
                    elif count == 2:
                        self.indel_score = float(line.split(";")[0])
                        count = 3
                    elif count == 3:
                        if not locals().get("comment3"):  # 保存该parameter注释, 并初始化
                            comment3 = line.strip().split(";")[1]
                        else:
                            self.list_alphabet = line.strip().split()
                            self.similarity_matrix = np.zeros((len(self.list_alphabet), len(self.list_alphabet)))
                            count = 4
                    elif count == 4:
                        if not locals().get("comment4"):  # 保存该parameter注释, 并初始化
                            comment4 = line.strip().split(";")[1]
                        else:
                            self.similarity_matrix[i] = line.strip().split()
                            i += 1


class GlobalAlign(object):
    """
    In this assignment, you need to implement a space efficient algorithm to compute the global alignment between two sequences.
    The programs should be flexible, i.e., it should be possible to:
         Align sequences over any alphabet. The alphabet can be {A, C, G, T} for DNA or 20 letters alphabet for amino acids, or any alphabet. The alphabet is specified in the parameter file.
         Use any score matrix. The score matrix is specified in the parameter file.
         Output the optimal alignment score and the optimal alignment.
    When you run your program, you need to limit your memory usage by 'ulimit -Sv 250000'
    """

    def __init__(self, parameter_txt, input_fa, output_txt, slope=6.0, multi=0):
        """
        Affine gap model.
            * slope = Gap penalty/Gap size
            * multi
                - 0 Only one optimal alignment (default)
                - 1 Output multiple optimal alignments
        """
        self.parameter_txt = parameter_txt
        self.input_fa = input_fa
        self.output_txt = output_txt

        self.origin_seq = None
        self.param = None
        self.array_V = None
        self.array_E = None
        self.array_F = None

        # Additional parameters: Slope(Gap penalty/Gap size)
        self.slope = slope
        self.multi = multi

        # result
        self.max_score = None
        self.result_seq = ResultSeq()

    def _match_score(self, element1, element2):
        """
        :param element1: Single base or single amino acid
        :param element2: Single base or single amino acid
        :return: score of match of mismatch
        """
        return self.param.similarity_matrix[self.param.list_alphabet.index(element1), self.param.list_alphabet.index(element2)]

    def _write_file(self):
        """
        Generate result file
        """
        with open(self.output_txt, "w") as handle:
            for instance in ResultSeq._all_instances:
                handle.writelines("score = {0}\n".format(self.max_score))
                handle.writelines(">{seq_name}\n{seq}\n".format(seq_name=self.origin_seq.seq1_name, seq=instance.seq1))
                handle.writelines(">{seq_name}\n{seq}\n".format(seq_name=self.origin_seq.seq2_name, seq=instance.seq2))

    def run(self):
        """
        :return:
        """
        logger_1.info("Loading parameters")
        sequence = collections.namedtuple("sequence", ["seq1_name", "seq1", "seq2_name", "seq2"])
        with open(self.input_fa, "r") as handle:
            self.origin_seq = sequence._make(itertools.chain.from_iterable(SimpleFastaParser(handle)))
        self.param = ExternalParameters(self.parameter_txt)
        # Determine whether the input case is consistent
        if not "".join(self.param.list_alphabet).isupper() == self.origin_seq.seq1.isupper():
            logger_1.warning("The input case is not consistent")
            if self.origin_seq.seq1.isupper():
                self.param.list_alphabet = [x.upper() for x in self.param.list_alphabet]
            else:
                self.param.list_alphabet = [x.lower() for x in self.param.list_alphabet]
        len_seq1 = len(self.origin_seq.seq1)
        len_seq2 = len(self.origin_seq.seq2)

        logger_1.info("h: {0}\ts: {1}".format(self.param.gap_init_score, self.slope))

        logger_1.info("Initialization matrix")
        self.array_V = np.zeros((len_seq1 + 1, len_seq2 + 1))
        self.array_E = np.zeros((len_seq1 + 1, len_seq2 + 1))
        self.array_F = np.zeros((len_seq1 + 1, len_seq2 + 1))

        self.array_V[0, 1:] = [(0 + self.param.gap_init_score - i * self.slope) for i in range(1, len_seq2 + 1)]
        self.array_V[:, 0][1:] = [(0 + self.param.gap_init_score - i * self.slope) for i in range(1, len_seq1 + 1)]
        self.array_E[:, 0][1:] = float("-inf")
        self.array_F[0, 1:] = float("-inf")

        logger_1.info("filling matrix of V,E,F")
        for i in range(1, len_seq1 + 1):
            for j in range(1, len_seq2 + 1):
                self.array_E[i, j] = max(self.array_E[i, j-1] - self.slope, self.array_V[i, j-1] + self.param.gap_init_score - self.slope)
                self.array_F[i, j] = max(self.array_F[i-1, j] - self.slope, self.array_V[i-1, j] + self.param.gap_init_score - self.slope)
                self.array_V[i, j] = max(self.array_V[i-1, j-1] + self._match_score(self.origin_seq.seq1[i-1], self.origin_seq.seq2[j-1]), self.array_E[i, j], self.array_F[i, j])

        self.max_score = max(self.array_V[len_seq1, len_seq2], self.array_E[len_seq1, len_seq2], self.array_F[len_seq1, len_seq2])

        self.chose_result(len_seq1, len_seq2)

        logger_1.info("Generate result file with detailed content")
        self._write_file()
        logger_1.info("score = {0}".format(self.max_score))
        if len(ResultSeq._all_instances) < 5:
            for instance in ResultSeq._all_instances:
                logger_1.info(textwrap.shorten("S: " + instance.seq1, width=30, placeholder="..."))
                logger_1.info(textwrap.shorten("T: " + instance.seq2, width=30, placeholder="..."))
        else:
            logger_1.info("There are {0} optimal alignment paths".format(len(ResultSeq._all_instances)))
        logger_1.info("Congratulations! ^*_*^")

    def chose_result(self, len_seq1, len_seq2):
        if self.multi:
            logger_1.info("Backtracking [Multi]")
            if self.max_score == self.array_V[len_seq1, len_seq2]:
                self.multi_backtracking(self.array_V, len_seq1, len_seq2, self.result_seq)
            elif self.max_score == self.array_E[len_seq1, len_seq2]:
                self.multi_backtracking(self.array_E, len_seq1, len_seq2, self.result_seq)
            else:
                self.multi_backtracking(self.array_F, len_seq1, len_seq2, self.result_seq)
        else:
            logger_1.info("Backtracking")
            if self.max_score == self.array_V[len_seq1, len_seq2]:
                self.backtracking(self.array_V, len_seq1, len_seq2)
            elif self.max_score == self.array_E[len_seq1, len_seq2]:
                self.backtracking(self.array_E, len_seq1, len_seq2)
            else:
                self.backtracking(self.array_F, len_seq1, len_seq2)

    def backtracking(self, array, i, j):
        """
        :param array: V, E, F
        :param i: row
        :param j: col
        :return: Single alignment result
        """
        if i+j == 0:
            pass
        elif i+j < 0:
            pass
        else:
            if array is self.array_V:
                logger_1.debug("POSITION: V[{0},{1}]".format(i, j))
                if self.array_V[i, j] == self.array_V[i-1, j-1] + self._match_score(self.origin_seq.seq1[i-1], self.origin_seq.seq2[j-1]):
                    self.result_seq.seq1 = self.origin_seq.seq1[i - 1] + self.result_seq.seq1
                    self.result_seq.seq2 = self.origin_seq.seq2[j - 1] + self.result_seq.seq2
                    self.backtracking(self.array_V, i - 1, j - 1)
                elif self.array_V[i, j] == self.array_E[i, j]:
                    self.backtracking(self.array_E, i, j)
                else:
                    self.backtracking(self.array_F, i, j)
            elif array is self.array_E:
                logger_1.debug("POSITION: E[{0},{1}]".format(i, j))
                self.result_seq.seq1 = "-" + self.result_seq.seq1
                self.result_seq.seq2 = self.origin_seq.seq2[j-1] + self.result_seq.seq2
                if self.array_E[i, j] == self.array_E[i, j-1] - self.slope:
                    self.backtracking(self.array_E, i, j - 1)
                else:
                    self.backtracking(self.array_V, i, j - 1)
            else:
                logger_1.debug("POSITION: F[{0},{1}]".format(i, j))
                self.result_seq.seq1 = self.origin_seq.seq1[i-1] + self.result_seq.seq1
                self.result_seq.seq2 = "-" + self.result_seq.seq2
                if self.array_F[i, j] == self.array_F[i-1, j] - self.slope:
                    self.backtracking(self.array_F, i - 1, j)
                else:
                    self.backtracking(self.array_V, i - 1, j)

    def multi_backtracking(self, array, i, j, result_seq ):
        """
        :param array: V, E, F
        :param i: row
        :param j: col
        :param result_seq: new instance of the class ResultSeq
        :return: Multiple alignment results
        """
        if i+j == 0:
            pass
        elif i+j < 0:
            pass
        else:
            if array is self.array_V:
                logger_1.debug("POSITION: V[{0},{1}]".format(i, j))
                pass_judgement = list(map(lambda x: 1 if x == self.array_V[i, j] else 0, (
                self.array_V[i - 1, j - 1] + self._match_score(self.origin_seq.seq1[i - 1],
                                                               self.origin_seq.seq2[j - 1]) if (i + j) > 1 else None,
                self.array_E[i, j], self.array_F[i, j])))
                if sum(pass_judgement) > 1:
                    if pass_judgement[0]:
                        # 新建引用，不会影响后面result_seq的使用
                        new_seq1 = self.origin_seq.seq1[i - 1] + result_seq.seq1
                        new_seq2 = self.origin_seq.seq2[j - 1] + result_seq.seq2
                        self.multi_backtracking(self.array_V, i - 1, j - 1, ResultSeq(new_seq1, new_seq2))
                    if pass_judgement[1]:
                        self.multi_backtracking(self.array_E, i, j, ResultSeq(result_seq.seq1, result_seq.seq2))
                    if pass_judgement[2]:
                        self.multi_backtracking(self.array_F, i, j, ResultSeq(result_seq.seq1, result_seq.seq2))
                    result_seq.del_ins()
                else:
                    if pass_judgement[0]:
                        result_seq.seq1 = self.origin_seq.seq1[i - 1] + result_seq.seq1
                        result_seq.seq2 = self.origin_seq.seq2[j - 1] + result_seq.seq2
                        self.multi_backtracking(self.array_V, i - 1, j - 1, result_seq)
                    elif pass_judgement[1]:
                        self.multi_backtracking(self.array_E, i, j, result_seq)
                    else:
                        self.multi_backtracking(self.array_F, i, j, result_seq)
            elif j > 0 and array is self.array_E:
                logger_1.debug("POSITION: E[{0},{1}]".format(i, j))
                result_seq.seq1 = "-" + result_seq.seq1
                result_seq.seq2 = self.origin_seq.seq2[j - 1] + result_seq.seq2
                pass_judgement = list(map(lambda x: x == self.array_E[i, j], (
                    self.array_E[i, j - 1] - self.slope,
                    self.array_V[i, j - 1] + self.param.gap_init_score - self.slope)))
                if all(pass_judgement):
                    if pass_judgement[0]:
                        self.multi_backtracking(self.array_E, i, j - 1, ResultSeq(result_seq.seq1, result_seq.seq2))
                    if pass_judgement[1]:
                        self.multi_backtracking(self.array_V, i, j - 1, ResultSeq(result_seq.seq1, result_seq.seq2))
                    result_seq.del_ins()
                else:
                    if pass_judgement[0]:
                        self.multi_backtracking(self.array_E, i, j - 1, result_seq)
                    else:
                        self.multi_backtracking(self.array_V, i, j - 1, result_seq)
            elif i > 0:
                logger_1.debug("POSITION: F[{0},{1}]".format(i, j))
                result_seq.seq1 = self.origin_seq.seq1[i - 1] + result_seq.seq1
                result_seq.seq2 = "-" + result_seq.seq2
                pass_judgement = list(map(lambda x: x == self.array_F[i, j], (
                    self.array_F[i - 1, j] - self.slope,
                    self.array_V[i - 1, j] + self.param.gap_init_score - self.slope)))
                if all(pass_judgement):
                    if pass_judgement[0]:
                        self.multi_backtracking(self.array_F, i - 1, j, ResultSeq(result_seq.seq1, result_seq.seq2))
                    if pass_judgement[1]:
                        self.multi_backtracking(self.array_V, i - 1, j, ResultSeq(result_seq.seq1, result_seq.seq2))
                    result_seq.del_ins()
                else:
                    if pass_judgement[0]:
                        self.multi_backtracking(self.array_F, i - 1, j, result_seq)
                    else:
                        self.multi_backtracking(self.array_V, i - 1, j, result_seq)


if __name__ == '__main__':
    if len(sys.argv) > 3:
        task1 = GlobalAlign(sys.argv[1], sys.argv[2], sys.argv[3], 10 if len(sys.argv) > 4 else float(sys.argv[4]))
        task1.run()
    elif len(sys.argv) == 1:
        test = GlobalAlign("data/parameter2.txt", "data/input2.fa", "data/output.txt", slope=2, multi=1)
        test.run()
    else:
        print("Usage: python3 global_align.py parameter.txt input.fa output.txt slope[Default:10] multi[Default:0]")
        raise ParameterError("The number of parameters")
