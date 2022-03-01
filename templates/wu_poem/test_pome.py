import torch
import torch.nn as nn
import numpy as np
from gensim.models.word2vec import Word2Vec
import pickle
from torch.utils.data import Dataset,DataLoader
import os


def train_vec(split_file='templates/wu_poem/split.txt',org_file='templates/wu_poem/wu_jueju.txt'):
    #word2vec模型
    vec_params_file="vec_params.pkl"
    #读取切分的文件
    split_all_data=open(split_file,"r",encoding="utf-8").read().split("\n")
    #读取原始文件
    org_data=open(org_file,"r",encoding="utf-8").read().split("\n")
    #存在模型文件就去加载，返回数据即可
    if os.path.exists(vec_params_file):
        return org_data,pickle.load(open(vec_params_file,"rb"))
    #词向量大小：vector_size，构造word2vec模型，字维度107，只要出现一次就统计该字，workers=6同时工作
    embedding_num=128
    model=Word2Vec(split_all_data,vector_size=embedding_num,min_count=1,workers=6)
    #保存模型
    pickle.dump((model.syn1neg,model.wv.key_to_index,model.wv.index_to_key),open(vec_params_file,"wb"))
    return org_data,(model.syn1neg,model.wv.key_to_index,model.wv.index_to_key)
#给出开头一个字，自动生成诗
def generate_poetry_auto(res,model,word_2_index,index_2_word,w1):

    result=res
    #随机产生第一个字的下标
    # word_index=np.random.randint(0,word_size,1)[0]
    # result += index_2_word[word_index]
    word_index=word_2_index[res]
    #叠词优化
    pre_index=word_index
    hidden_num = 128
    h_0 = torch.tensor(np.zeros((2, 1, hidden_num), np.float32))
    c_0 = torch.tensor(np.zeros((2, 1, hidden_num), np.float32))

    #开头词不重复
    num_mark=[5,11,17]
    ans_index=[]
    ans_index.append(word_index)
    for i in range(23):
        word_embedding=torch.tensor(w1[word_index].reshape(1,1,-1))
        pre,(h_0,c_0)=model(word_embedding,h_0,c_0)
        word_index=int(torch.argmax(pre))
        #叠词优化
        while(pre_index==word_index):
            word_embedding = torch.tensor(w1[pre_index].reshape(1, 1, -1))
            pre, (h_0, c_0) = model(word_embedding, h_0, c_0)
            word_index = int(torch.argmax(pre))
        #保证开头词不重复
        if i in num_mark:
            while word_index in ans_index:
                word_embedding = torch.tensor(w1[pre_index].reshape(1, 1, -1))
                pre, (h_0, c_0) = model(word_embedding, h_0, c_0)
                word_index = int(torch.argmax(pre))
            ans_index.append(word_index)
        result+=index_2_word[word_index]
        pre_index=word_index
    print(result)
    return result

#藏头诗
def cang(res,model,word_2_index,index_2_word,w1):
    result=''
    hidden_num = 128
    punctuation_list = ["，", "。", "，", "。"]
    for i in range(len(res)):
        result+=res[i]
        word_index = word_2_index[res[i]]
        #叠词优化
        pre_index=word_index
        h_0 = torch.tensor(np.zeros((2, 1, hidden_num), np.float32))
        c_0 = torch.tensor(np.zeros((2, 1, hidden_num), np.float32))
        for j in range(4):
            word_embedding = torch.tensor(w1[word_index].reshape(1, 1, -1))
            pre, (h_0, c_0) = model(word_embedding, h_0, c_0)
            word_index = int(torch.argmax(pre))
            #叠词优化
            while(pre_index==word_index):
                word_embedding = torch.tensor(w1[pre_index].reshape(1, 1, -1))
                pre, (h_0, c_0) = model(word_embedding, h_0, c_0)
                word_index = int(torch.argmax(pre))
            result += index_2_word[word_index]
            pre_index=word_index
        result+=punctuation_list[i]
    print(result)
    return result