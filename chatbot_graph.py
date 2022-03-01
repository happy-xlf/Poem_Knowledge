#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        print('分类器构建完毕')
        self.parser = QuestionPaser()
        print('sql语句构建完毕')
        self.searcher = AnswerSearcher()
        print('回答构建完毕')

    def chat_main(self, sent):
        answer = '您好，我是小诗智能助手，希望可以帮到您。如果没答上来，可联系我的老大：徐利峰先生。祝您学习诗词愉快！'
        res_classify = self.classifier.classify(sent)
        print(res_classify)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return ''.join(final_answers)

# if __name__ == '__main__':
#     handler = ChatBotGraph()
#     while 1:
#         question = input('用户:')
#         answer = handler.chat_main(question)
#         print('小诗:', answer)

