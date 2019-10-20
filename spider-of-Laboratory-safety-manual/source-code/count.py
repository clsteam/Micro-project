#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 15:26
# @Author  : Yao
import os
download_doc = 'F:/practice/'
os.chdir(download_doc)

def generate_question_database(paper_file = None):
    QN = 0
    with open(paper_file, "r", encoding='utf-8') as doc:
        for line in doc:
            if line.startswith(">"):
                QN += 1
    return QN

for page, txt in enumerate(os.listdir(download_doc)):
    # txt = txt.encode("utf-8")
    qn = generate_question_database(txt)
    # txt = txt.encode('utf-8')
    # |page:1|华中农业大学实验室技术安全管理体制与运行机制|60|√|
    print("|page:{0}|{1}|{2}|?|".format(page,txt.split(".")[0][1:], qn))