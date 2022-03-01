#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'author_poem':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_friend':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_born':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_die':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_desty':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_common_name':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_travel_where':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_zi':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_hao':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_poem_sum':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_travel':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'author_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('author'))

            elif question_type == 'poem_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_date':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_back':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_trans':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_author':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_desty':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_tag':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_formal':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_cipaiming':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'poem_qupaiming':
                sql = self.sql_transfer(question_type, entity_dict.get('poem'))

            elif question_type == 'tag_poem':
                sql = self.sql_transfer(question_type, entity_dict.get('tag'))

            elif question_type == 'formal_poem':
                sql = self.sql_transfer(question_type, entity_dict.get('formal'))

            elif question_type == 'cipaiming_poem':
                sql = self.sql_transfer(question_type, entity_dict.get('cipai_name'))

            elif question_type == 'qupaiming_poem':
                sql = self.sql_transfer(question_type, entity_dict.get('qupai_name'))

            elif question_type == 'desty_poem':
                sql = self.sql_transfer(question_type, entity_dict.get('desty'))

            elif question_type == 'desty_author':
                sql = self.sql_transfer(question_type, entity_dict.get('desty'))

            elif question_type == 'common_name_author':
                sql = self.sql_transfer(question_type, entity_dict.get('common_name'))

            elif question_type == 'word_poem':
                sql = self.sql_transfer(question_type, entity_dict.get('word'))

            elif question_type == 'cipai_desc':
                sql = self.sql_transfer(question_type, ['词牌名'])

            elif question_type == 'qupai_desc':
                sql = self.sql_transfer(question_type, ['曲牌名'])

            elif question_type == 'formal_desc':
                sql =self.sql_transfer(question_type,['形式'])

            elif question_type == 'tag_desc':
                sql =self.sql_transfer(question_type,['类别'])

            elif question_type == 'desty_desc':
                sql =self.sql_transfer(question_type,['朝代'])

            elif question_type == 'common_name_desc':
                sql =self.sql_transfer(question_type,['合称'])

            elif question_type == 'word_desc':
                sql =self.sql_transfer(question_type,['飞花令'])

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls




    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 查询诗人的诗集
        if question_type == 'author_poem':
            sql = ["MATCH (m:author)-[r:`写作`]->(n:poem) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询诗人的好友
        elif question_type == 'author_friend':
            sql = ["MATCH (m:author)-[r:`好友`]->(n:author) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询诗人的出生年月
        elif question_type == 'author_born':
            sql = ["MATCH (m:author) where m.name = '{0}' return m.name, m.bg_time".format(i) for i in entities]

        # 查询诗人的死亡年月
        elif question_type == 'author_die':
            sql = ["MATCH (m:author) where m.name = '{0}' return m.name, m.ed_time".format(i) for i in entities]

        # 查询诗人的年代
        elif question_type == 'author_desty':
            sql= ["MATCH (m:author)-[r:`朝代`]->(n:desty) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询诗人的合称
        elif question_type == 'author_common_name':
            sql = ["MATCH (m:author)-[r:`合称`]->(n:common_name) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询诗人的游历地点
        elif question_type == 'author_travel_where':
            sql = ["MATCH (m:author)-[r:`事迹`]->(n:things) where m.name = '{0}' return m.name, n.where_name".format(i) for i in entities]

        # 查询诗人的字
        elif question_type == 'author_zi':
            sql = ["MATCH (m:author) where m.name = '{0}' return m.name, m.zi".format(i) for i in entities]

        # 查询诗人的号
        elif question_type == 'author_hao':
            sql = ["MATCH (m:author) where m.name = '{0}' return m.name, m.hao".format(i) for i in entities]

        # 查询诗人的诗词总数
        elif question_type == 'author_poem_sum':
            sql = ["MATCH (m:author) where m.name = '{0}' return m.name, m.num".format(i) for i in entities]

        # 查询诗人的基本信息
        elif question_type == 'author_desc':
            sql = ["MATCH (m:author) where m.name = '{0}' return m.name, m.produce".format(i) for i in entities]

        # 查询诗词的基本信息
        elif question_type == 'poem_desc':
            sql = ["MATCH (m:poem) where m.name = '{0}' return m.name, m.content".format(i) for i in entities]

        # 查询诗词的创作时间
        elif question_type == 'poem_date':
            sql = ["MATCH (m:poem) where m.name = '{0}' return m.name, m.date".format(i) for i in entities]

        # 查询诗词的相关背景
        elif question_type == 'poem_back':
            sql = ["MATCH (m:poem) where m.name = '{0}' return m.name, m.background".format(i) for i in entities]

        # 查询诗词的翻译
        elif question_type == 'poem_trans':
            sql = ["MATCH (m:poem) where m.name = '{0}' return m.name, m.trans_content".format(i) for i in entities]

        # 查询诗词的作者
        elif question_type == 'poem_author':
            sql = ["MATCH (m:poem)-[r:`作者`]->(n:author) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询诗词的朝代
        elif question_type == 'poem_desty':
            sql = ["MATCH (m:poem)-[r:`朝代`]->(n:desty) where m.name = '{0}' return m.name, n.name".format(i) for i in entities]

        # 查询诗词的类别
        elif question_type == 'poem_tag':
            sql = ["MATCH (m:poem)-[r:`分类`]->(n:tag) where m.name = '{0}' return m.name, n.name".format(i) for i in
                   entities]

        # 查询诗词的形式
        elif question_type == 'poem_formal':
            sql = ["MATCH (m:poem)-[r:`形式`]->(n:formal) where m.name = '{0}' return m.name, n.name".format(i) for i in
                   entities]

        # 查询诗词的词牌名
        elif question_type == 'poem_cipaiming':
            sql = ["MATCH (m:poem)-[r:`词牌名`]->(n:ci_pai) where m.name = '{0}' return m.name, n.name".format(i) for i in
                   entities]

        # 查询诗词的曲牌名
        elif question_type == 'poem_qupaiming':
            sql = ["MATCH (m:poem)-[r:`曲牌名`]->(n:qu_pai) where m.name = '{0}' return m.name, n.name".format(i) for i in
                   entities]

        # 查询类别包含的诗
        elif question_type == 'tag_poem':
            sql = ["MATCH (m:tag)-[r:`包含`]->(n:poem) where m.name = '{0}' return m.name, n.name".format(i) for i in
                   entities]

        # 查询形式包含的诗
        elif question_type == 'formal_poem':
            sql = ["MATCH (m:formal)-[r:`包含`]->(n:poem) where m.name = '{0}' return m.name, n.name".format(i) for i in
                   entities]

        # 查询词牌名包含的诗
        elif question_type == 'cipaiming_poem':
            sql = ["MATCH (m:ci_pai)-[r:`包含`]->(n:poem) where m.name = '{0}' return m.name, n.name".format(i) for i in
                   entities]

        # 查询曲牌名包含的诗
        elif question_type == 'qupaiming_poem':
            sql = ["MATCH (m:qu_pai)-[r:`包含`]->(n:poem) where m.name = '{0}' return m.name, n.name".format(i) for i
                   in entities]

        # 查询朝代包含的诗
        elif question_type == 'desty_poem':
            sql = ["MATCH (m:desty)-[r:`包含诗词`]->(n:poem) where m.name = '{0}' return m.name, n.name".format(i) for i
                   in entities]

        # 查询朝代包含的诗人
        elif question_type == 'desty_author':
            sql = ["MATCH (m:desty)-[r:`包含`]->(n:author) where m.name = '{0}' return m.name, n.name".format(i) for i
                   in entities]

        # 查询朝代包含的诗人
        elif question_type == 'common_name_author':
            sql = ["MATCH (m:common_name)-[r:`包含`]->(n:author) where m.name = '{0}' return m.name, n.name".format(i) for i
                   in entities]

        # 查询飞花令包含的诗
        elif question_type == 'word_poem':
            sql = ["MATCH (m:word)-[r:`诗句`]->(n:sentence) where m.name = '{0}' return m.name, n.name LIMIT 25".format(i) for
                   i in entities]

        # 查询所有的词牌名
        elif question_type == 'cipai_desc':
            sql = ["MATCH (m:ci_pai)  return m.name"]

        # 查询所有的词牌名
        elif question_type == 'qupai_desc':
            sql = ["MATCH (m:qu_pai)  return m.name"]

        # 查询所有的类别
        elif question_type == 'formal_desc':
            sql = ["MATCH (m:formal) return m.name"]

        # 查询所有的类别
        elif question_type == 'tag_desc':
            sql = ["MATCH (m:tag)  return m.name"]

        # 查询所有的朝代
        elif question_type == 'desty_desc':
            sql = ["MATCH (m:desty)  return m.name"]

        # 查询所有的合称
        elif question_type == 'common_name_desc':
            sql = ["MATCH (m:common_name)  return m.name"]

        # 查询所有的飞花令
        elif question_type == 'word_desc':
            sql = ["MATCH (m:word)  return m.name"]

        return sql


 # # 诗词作诗时间
    # self.poem_date_qwds = ['时间', '作诗时间']
    # # 诗词的创作背景
    # self.poem_back_qwds = ['创作背景', '背景']
    # # 诗词的翻译
    # self.poem_trans_qwds = ['翻译']
    # # 诗词的作者
    # self.poem_author_qwds = ['作者', '写', '作', '创作']
    # # 诗词的朝代
    # self.poem_desty_qwds = ['朝代', '朝', '年代', '代']
    # # 诗词的类别
    # self.poem_tag_qwds = ['类', '类别', '类型', '风格']
    # # 诗词的形式
    # self.poem_formal_qwds = ['形式', '题材']
    # # 诗词的牌名
    # self.poem_paiming_qwds = ['牌名']


if __name__ == '__main__':
    handler = QuestionPaser()
