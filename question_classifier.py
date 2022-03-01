#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.author_path = os.path.join(cur_dir, 'dict/author.txt')
        self.cipai_name_path = os.path.join(cur_dir, 'dict/cipai_name.txt')
        self.common_name_path = os.path.join(cur_dir, 'dict/common_name.txt')
        self.desty_path = os.path.join(cur_dir, 'dict/desty.txt')
        self.formal_path = os.path.join(cur_dir, 'dict/formal.txt')
        self.poem_path = os.path.join(cur_dir, 'dict/tang_poem.txt')
        self.qupai_name_path = os.path.join(cur_dir, 'dict/qupai_name.txt')
        self.tag_path = os.path.join(cur_dir, 'dict/tag.txt')
        self.word_path = os.path.join(cur_dir, 'dict/word.txt')
        # 加载特征词
        self.author_wds= [i.strip() for i in open(self.author_path,encoding='utf-8') if i.strip()]
        self.cipai_name_wds= [i.strip() for i in open(self.cipai_name_path,encoding='utf-8') if i.strip()]
        self.common_name_wds= [i.strip() for i in open(self.common_name_path,encoding='utf-8') if i.strip()]
        self.desty_wds= [i.strip() for i in open(self.desty_path,encoding='utf-8') if i.strip()]
        self.formal_wds= [i.strip() for i in open(self.formal_path,encoding='utf-8') if i.strip()]
        self.poem_wds= [i.strip() for i in open(self.poem_path,encoding='utf-8') if i.strip()]
        self.qupai_name_wds= [i.strip() for i in open(self.qupai_name_path,encoding='utf-8') if i.strip()]
        self.tag_wds=[i.strip() for i in open(self.tag_path,encoding='utf-8') if i.strip()]
        self.word_wds = [i.strip() for i in open(self.word_path, encoding='utf-8') if i.strip()]
        print('开始合并词：')
        self.region_words = set(self.author_wds + self.cipai_name_wds + self.common_name_wds + self.desty_wds+ self.formal_wds
                                + self.poem_wds
                                +self.qupai_name_wds + self.tag_wds + self.word_wds)
        print('合并完成，一共'+str(len(self.region_words))+'个')
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        print('树，构建完成，开始构建词典')
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        print('词典构建完成')
        # 问句疑问词
#----------诗人相关问题-------------------------------------------------
        # 诗人的作品
        self.poem_name_qwds=['诗','作品','诗集','诗词']
        # 诗人的朋友
        self.poemer_friend_qwds=['好友','朋友','知己']
        # 诗人的出生年月
        self.poemer_born_qwds=['出生','生于']
        # 诗人的去世年月
        self.poemer_die_qwds = ['死', '去世']
        # 诗人的简介
        self.author_qwds=['简介','介绍']
        # 诗人所属朝代
        self.author_desty_qwds=['朝代','朝','年代','代']
        # 诗人的合称
        self.author_common_name_qwds=['合称','称号']
        # 诗人旅行地点
        self.author_travel_where_qwds=['旅行','游历','游玩','到','地点']
        # 诗人的字
        self.author_zi_qwds=['字']
        # 诗人的号
        self.author_hao_qwds=['号']
        # 诗人的诗集总数
        self.author_poem_sum_qwds=['总数','合计','总共','诗词总数']
# ----------诗词相关问题-------------------------------------------------
        # 诗词的内容
        self.poem_qwds=['内容']
        # 诗词作诗时间
        self.poem_date_qwds=['时间','作诗时间']
        # 诗词的创作背景
        self.poem_back_qwds=['创作背景','背景']
        # 诗词的翻译
        self.poem_trans_qwds=['翻译','译文']
        # 诗词的作者
        self.poem_author_qwds=['作者','诗人']
        # 诗词的朝代
        self.poem_desty_qwds=['朝代','朝','年代','代']
        # 诗词的类别
        self.poem_tag_qwds=['类','类别','类型','风格']
        # 诗词的形式
        self.poem_formal_qwds=['形式','题材']
        # 诗词的词牌名
        self.poem_cipaiming_qwds=['词牌名']
        # 诗词的曲牌名
        self.poem_qupaiming_qwds = ['曲牌名']
# ----------类别相关问题-------------------------------------------------
        # 所有诗词类别？
        self.tag_qwds = ['诗词类别']
        # 类别包含哪些诗？
        self.tag_poem_qwds=['诗','有']
# ----------形式相关问题-------------------------------------------------
        # 所有诗词形式？
        self.formal_qwds = ['诗词形式']
        # 形式包含哪些诗？
        self.formal_poem_qwds=['诗','有']
# ----------词牌名问题-----------------------------------------------
        # 所有的词牌名？
        self.cipaiming_qwds = ['词牌名']
        # 词牌名包含哪些诗？
        self.cipaiming_poem_qwds=['诗','有']
# ----------曲牌名问题-----------------------------------------------
        # 类所有曲牌名？
        self.qupaiming_qwds = ['曲牌名']
        # 曲牌名包含哪些诗？
        self.qupaiming_poem_qwds = ['诗', '有']
# ----------朝代问题-----------------------------------------------
        # 所有的朝代？
        self.desty_qwds = ['朝代']
        # 朝代包含哪些诗？
        self.desty_poem_qwds = ['诗', '有']
        # 朝代包含的诗人？
        self.desty_author_qwds=['诗人','人']
# ----------诗人合称问题-----------------------------------------------
        # 所有合称
        self.common_name_qwds = ['诗人合称']
        # 诗人合称包含哪些人？
        self.common_name_author_qwds=['人','诗人']
# ----------飞花令问题--------------------------------------------------
        # 飞花令的诗句
        self.word_qwds = ['飞花令']
        # 飞花令的诗句
        self.word_poem_qwds=['飞花令']


        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        medical_dict = self.check_medical(question)
        # 实体改进：缺失实体填充
        if not medical_dict:
            if 'diseases_dict' in globals():  # 判断是否是首次提问，若首次提问，则diseases_dict无值
                medical_dict = diseases_dict
            else:
                return {}
        data['args'] = medical_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # 诗人的诗集有哪些
        if self.check_words(self.poem_name_qwds, question) and ('author' in types):
            question_type = 'author_poem'
            question_types.append(question_type)

        # 诗人的好友有哪些
        if self.check_words(self.poemer_friend_qwds, question) and ('author' in types):
            question_type = 'author_friend'
            question_types.append(question_type)

        # 诗人的出生年月
        if self.check_words(self.poemer_born_qwds, question) and ('author' in types):
            question_type = 'author_born'
            question_types.append(question_type)

        # 诗人的死亡年月
        if self.check_words(self.poemer_die_qwds, question) and ('author' in types):
            question_type = 'author_die'
            question_types.append(question_type)

        # 诗人的朝代
        if self.check_words(self.author_desty_qwds, question) and ('author' in types):
            question_type = 'author_desty'
            question_types.append(question_type)

        # 诗人的合称
        if self.check_words(self.author_common_name_qwds, question) and ('author' in types):
            question_type = 'author_common_name'
            question_types.append(question_type)

        # 诗人的游历地点
        if self.check_words(self.author_travel_where_qwds, question) and ('author' in types):
            question_type = 'author_travel_where'
            question_types.append(question_type)

        # 诗人的字
        if self.check_words(self.author_zi_qwds, question) and ('author' in types):
            question_type = 'author_zi'
            question_types.append(question_type)

        # 诗人的号
        if self.check_words(self.author_hao_qwds, question) and ('author' in types):
            question_type = 'author_hao'
            question_types.append(question_type)

        # 诗人的诗集总数
        if self.check_words(self.author_poem_sum_qwds, question) and ('author' in types):
            question_type = 'author_poem_sum'
            question_types.append(question_type)

        # 诗人的个人介绍
        if self.check_words(self.author_qwds ,question) and ('author' in types):
            question_type = 'author_desc'
            question_types.append(question_type)

        # 诗词的文章内容
        if self.check_words(self.poem_qwds, question) and ('poem' in types):
            question_type = 'poem_desc'
            question_types.append(question_type)

        # 诗词的作诗时间
        if self.check_words(self.poem_date_qwds, question) and ('poem' in types):
            question_type = 'poem_date'
            question_types.append(question_type)

        # 诗词的创作背景
        if self.check_words(self.poem_back_qwds, question) and ('poem' in types):
            question_type = 'poem_back'
            question_types.append(question_type)

        # 诗词的翻译
        if self.check_words(self.poem_trans_qwds, question) and ('poem' in types):
            question_type = 'poem_trans'
            question_types.append(question_type)

        # 诗词的作者
        if self.check_words(self.poem_author_qwds, question) and ('poem' in types):
            question_type = 'poem_author'
            question_types.append(question_type)

        # 诗词的朝代
        if self.check_words(self.poem_desty_qwds, question) and ('poem' in types):
            question_type = 'poem_desty'
            question_types.append(question_type)

        # 诗词的类别
        if self.check_words(self.poem_tag_qwds, question) and ('poem' in types):
            question_type = 'poem_tag'
            question_types.append(question_type)

        # 诗词的形式
        if self.check_words(self.poem_formal_qwds, question) and ('poem' in types):
            question_type = 'poem_formal'
            question_types.append(question_type)

        # 诗词的词牌名
        if self.check_words(self.poem_cipaiming_qwds, question) and ('poem' in types):
            question_type = 'poem_cipaiming'
            question_types.append(question_type)

        # 诗词的曲牌名
        if self.check_words(self.poem_qupaiming_qwds, question) and ('poem' in types):
            question_type = 'poem_qupaiming'
            question_types.append(question_type)

        # 类别包含的诗
        if self.check_words(self.tag_poem_qwds, question) and ('tag' in types):
            question_type = 'tag_poem'
            question_types.append(question_type)

        #形式包含的诗
        if self.check_words(self.formal_poem_qwds, question) and ('formal' in types):
            question_type='formal_poem'
            question_types.append(question_type)

        # 词牌名包含的诗
        if self.check_words(self.cipaiming_poem_qwds, question) and ('cipai_name' in types):
            question_type = 'cipaiming_poem'
            question_types.append(question_type)

        # 曲牌名包含的诗
        if self.check_words(self.qupaiming_poem_qwds, question) and ('qupai_name' in types):
            question_type = 'qupaiming_poem'
            question_types.append(question_type)

        # 朝代包含的诗
        if self.check_words(self.desty_poem_qwds, question) and ('desty' in types):
            question_type = 'desty_poem'
            question_types.append(question_type)

        # 朝代包含的诗人
        if self.check_words(self.desty_author_qwds, question) and ('desty' in types):
            question_type = 'desty_author'
            question_types.append(question_type)

        # 合称包含的诗人
        if self.check_words(self.common_name_author_qwds, question) and ('common_name' in types):
            question_type = 'common_name_author'
            question_types.append(question_type)

        # 飞花令包含的诗句
        if self.check_words(self.word_poem_qwds, question) and ('word' in types):
            question_type = 'word_poem'
            question_types.append(question_type)

        # 所有的词牌名
        if self.check_words(self.cipaiming_qwds, question) and ('ci_pai' not in types):
            question_type = 'cipai_desc'
            question_types.append(question_type)

        # 所有的曲牌名
        if self.check_words(self.qupaiming_qwds, question) and ('qu_pai' not in types):
            question_type = 'qupai_desc'
            question_types.append(question_type)

        # 所有的诗词形式
        if self.check_words(self.formal_qwds, question) and ('formal' not in types):
            question_type = 'formal_desc'
            question_types.append(question_type)

        # 所有的诗词类别
        if self.check_words(self.tag_qwds, question) and ('tag' not in types):
            question_type = 'tag_desc'
            question_types.append(question_type)

        # 所有的朝代
        if self.check_words(self.desty_qwds, question) and ('desty' not in types):
            question_type = 'desty_desc'
            question_types.append(question_type)

        # 所有的合称
        if self.check_words(self.common_name_qwds, question) and ('common_name' not in types):
            question_type = 'common_name_desc'
            question_types.append(question_type)

        # 所有的飞花令
        if self.check_words(self.word_qwds, question):
            question_type = 'word_desc'
            question_types.append(question_type)


        # 若没有查到相关的外部查询信息，那么则将该主节点的描述信息返回
        if question_types == [] and 'author' in types:
            question_types = ['author_desc']

        # 若没有查到相关的外部查询信息，那么则将该主节点的描述信息返回
        if question_types == [] and 'poem' in types:
            question_types = ['poem_desc']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

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


    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        i=0
        for wd in self.region_words:
            print('这是第'+str(i)+'个')
            wd_dict[wd] = []
            if wd in self.author_wds:
                wd_dict[wd].append('author')
            if wd in self.cipai_name_wds:
                wd_dict[wd].append('cipai_name')
            if wd in self.common_name_wds:
                wd_dict[wd].append('common_name')
            if wd in self.desty_wds:
                wd_dict[wd].append('desty')
            if wd in self.formal_wds:
                wd_dict[wd].append('formal')
            if wd in self.poem_wds:
                wd_dict[wd].append('poem')
            if wd in self.qupai_name_wds:
                wd_dict[wd].append('qupai_name')
            if wd in self.tag_wds:
                wd_dict[wd].append('tag')
            if wd in self.word_wds:
                wd_dict[wd].append('word')
            i+=1
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}
        global diseases_dict
        if final_dict:
            diseases_dict = final_dict

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)