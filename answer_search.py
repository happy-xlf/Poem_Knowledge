#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-5

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            user="neo4j",
            password="fengge666")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers.append(ress)
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'author_poem':
            final_answer = ''
            for it in answers:
                desc = [i['n.name'] for i in it]
                desc.reverse()
                subject = it[0]['m.name']
                final_answer =final_answer+ '<br>{0}的诗词包括：{1}等等'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_friend':
            final_answer = ''
            for it in answers:
                desc = [i['n.name'] for i in it]
                desc.reverse()
                subject = it[0]['m.name']
                final_answer += '<br>{0}的好友包含：{1}等等'.format(subject, '；'.join(desc[:self.num_limit]))

        elif question_type == 'author_born':
            final_answer = ''
            for it in answers:
                desc = [i['m.bg_time'] for i in it]
                subject = it[0]['m.name']
                final_answer =final_answer+ '<br>{0}出生于：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_die':
            final_answer = ''
            for it in answers:
                desc = [i['m.ed_time'] for i in it]
                subject = it[0]['m.name']
                final_answer =final_answer+ '<br>{0}去世于：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_desty':
            final_answer = ''
            for it in answers:
                desc = [i['n.name'] for i in it]
                subject = it[0]['m.name']
                final_answer =final_answer+ '<br>{0}所属朝代为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_common_name':
            final_answer = ''
            for it in answers:
                desc = [i['n.name'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '<br>{0}的合称包含：{1}'.format(subject,
                                                                      '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_travel_where':
            final_answer = ''
            for it in answers:
                desc = [i['n.where_name'] for i in it if i['n.where_name']!=None ]
                subject = it[0]['m.name']
                final_answer = final_answer + '<br>{0}游历的地点包含：{1}等等'.format(subject,
                                                                      '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_zi':
            final_answer = ''
            for it in answers:
                desc = [i['m.zi'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '<br>{0}的字是：{1}'.format(subject,
                                                                      '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_hao':
            final_answer = ''
            for it in answers:
                desc = [i['m.hao'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '<br>{0}的号是：{1}'.format(subject,
                                                                    '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'author_poem_sum':
            final_answer = ''
            for it in answers:
                desc = [i['m.num'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '<br>{0}的诗词总数有：{1}个'.format(subject,str(desc[0]))

        elif question_type == 'author_desc':
            final_answer = ''
            for it in answers:
                desc = [i['m.produce'] for i in it]
                subject = it[0]['m.name']
                final_answer =final_answer+ '<br>{0}的简介：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'poem_desc':
            final_answer = '<br>'
            for it in answers:
                desc = [i['m.content'] for i in it]
                subject = it[0]['m.name']
                content=str(desc[0]).split('。')

                final_answer =final_answer + '{0}的内容是：<br>'.format(subject)
                for i in range(len(content)-1):
                    final_answer+=content[i]+"。<br>"

        elif question_type == 'poem_date':
            final_answer = '<br>'
            for it in answers:
                desc = [i['m.date'] for i in it]
                subject = it[0]['m.name']
                final_answer =final_answer + '{0}的创作时间是：{1}<br>'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'poem_back':
            final_answer = '<br>'
            for it in answers:
                desc = [i['m.background'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '{0}的相关背景是：{1}<br>'.format(subject,
                                                                       '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'poem_trans':
            final_answer = '<br>'
            for it in answers:
                desc = [i['m.trans_content'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '{0}的翻译是：{1}<br>'.format(subject,
                                                                       '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'poem_author':
            final_answer = '<br>'
            for it in answers:
                desc = [i['n.name'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '{0}的作者是：{1}<br>'.format(subject,
                                                                       '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'poem_desty':
            final_answer = '<br>'
            for it in answers:
                desc = [i['n.name'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '{0}的创作朝代是：{1}<br>'.format(subject,
                                                                       '；'.join(list(set(desc))[:self.num_limit]))
        elif question_type == 'poem_tag':
            final_answer = '<br>'
            print(answers)
            for it in answers:
                if it!=[]:
                    desc = [i['n.name'] for i in it]
                    subject = it[0]['m.name']
                    final_answer = final_answer + '{0}的类别是：{1}<br>'.format(subject,
                                                                           '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'poem_formal':
            final_answer = '<br>'
            for it in answers:
                desc = [i['n.name'] for i in it]
                subject = it[0]['m.name']
                final_answer = final_answer + '{0}的形式是：{1}<br>'.format(subject,
                                                                       '；'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'poem_cipaiming':
            final_answer = '<br>'
            if answers!=[[]]:
                for it in answers:
                    if it!=[]:
                        desc = [i['n.name'] for i in it]
                        subject = it[0]['m.name']
                        final_answer = final_answer + '{0}的词牌名是：{1}<br>'.format(subject,
                                                                               '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无词牌名'

        elif question_type == 'poem_qupaiming':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    if it!=[]:
                        desc = [i['n.name'] for i in it]
                        subject = it[0]['m.name']
                        final_answer = final_answer + '{0}的曲牌名是：{1}<br>'.format(subject,
                                                                              '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无曲牌名'
        elif question_type == 'tag_poem':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    subject = it[0]['m.name']
                    final_answer = final_answer + '{0}类别的诗包含：{1}等等<br>'.format(subject,
                                                                          '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该类别的诗'

        elif question_type == 'formal_poem':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    subject = it[0]['m.name']
                    final_answer = final_answer + '{0}形式的诗包含：{1}等等<br>'.format(subject,
                                                                          '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该形式的诗'

        elif question_type == 'cipaiming_poem':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    desc.reverse()
                    subject = it[0]['m.name']
                    final_answer = final_answer + '以{0}为词牌名的的诗包含：{1}等等<br>'.format(subject,
                                                                          '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该词牌名的诗'

        elif question_type == 'qupaiming_poem':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    desc.reverse()
                    subject = it[0]['m.name']
                    final_answer = final_answer + '以{0}为曲牌名的的诗包含：{1}等等<br>'.format(subject,
                                                                          '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该曲牌名的诗'

        elif question_type == 'desty_poem':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    desc.reverse()
                    subject = it[0]['m.name']
                    final_answer = final_answer + '{0}的诗包含：{1}等等<br>'.format(subject,
                                                                          '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该朝代的诗'

        elif question_type == 'desty_author':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    desc.reverse()
                    subject = it[0]['m.name']
                    final_answer = final_answer + '{0}的诗人包含：{1}等等<br>'.format(subject,
                                                                            '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该朝代的诗人'

        elif question_type == 'common_name_author':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    desc.reverse()
                    subject = it[0]['m.name']
                    final_answer = final_answer + '{0}包含的诗人：{1}等等<br>'.format(subject,
                                                                            '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该合称的诗人'

        elif question_type == 'word_poem':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['n.name'] for i in it]
                    desc.reverse()
                    subject = it[0]['m.name']
                    final_answer = final_answer + '以{0}为飞花令包含的诗：{1}等等<br>'.format(subject,
                                                                            '；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='暂无该飞花令的诗'

        elif question_type == 'cipai_desc':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['m.name'] for i in it]
                    desc.reverse()
                    final_answer = final_answer + '词牌名包含：{0}等等<br>'.format('；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='没有词牌名'

        elif question_type == 'qupai_desc':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['m.name'] for i in it]
                    desc.reverse()
                    final_answer = final_answer + '曲牌名包含：{0}等等<br>'.format('；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='没有曲牌名'

        elif question_type == 'formal_desc':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['m.name'] for i in it]
                    desc.reverse()
                    final_answer = final_answer + '诗词形式包含：{0}等等<br>'.format('；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='没有诗词形式'

        elif question_type == 'tag_desc':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['m.name'] for i in it]
                    desc.reverse()
                    final_answer = final_answer + '诗词类别包含：{0}等等<br>'.format('；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='没有诗词类别'

        elif question_type == 'desty_desc':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['m.name'] for i in it if i['m.name'] not in ['无','未知','元']]
                    desc.reverse()
                    final_answer = final_answer + '朝代包含：{0}等等<br>'.format('；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='没有朝代'

        elif question_type == 'common_name_desc':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['m.name'] for i in it if i['m.name'] not in ['无','未知','元']]
                    desc.reverse()
                    final_answer = final_answer + '诗人合称包含：{0}等等<br>'.format('；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='没有诗人合称'

        elif question_type == 'word_desc':
            final_answer = '<br>'
            if answers != [[]]:
                for it in answers:
                    desc = [i['m.name'] for i in it if i['m.name'] not in ['无','未知','元']]
                    desc.reverse()
                    final_answer = final_answer + '飞花令包含：{0}等等<br>'.format('；'.join(list(set(desc))[:self.num_limit]))
            else:
                final_answer='没有飞花令'

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()