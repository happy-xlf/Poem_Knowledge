from templates.wu_poem.test_pome import generate_poetry_auto,train_vec,cang
from templates.qi_poem.test_pome import generate_poetry_auto as qi_generate_poetry_auto,train_vec as qi_train_vec,cang as qi_cang
import torch
import torch.nn as nn
import numpy as np
from gensim.models.word2vec import Word2Vec
import pickle
import os

class Mymodel(nn.Module):

    def __init__(self,embedding_num,hidden_num,word_size):
        super(Mymodel, self).__init__()

        self.embedding_num=embedding_num
        self.hidden_num = hidden_num
        self.word_size = word_size
        #num_layer:两层，代表层数,出来后的维度[5,31,64],设置hidden_num=64
        self.lstm=nn.LSTM(input_size=embedding_num,hidden_size=hidden_num,batch_first=True,num_layers=2,bidirectional=False)
        #做一个随机失活，防止过拟合，同时可以保持生成的古诗不唯一
        self.dropout=nn.Dropout(0.3)
        #做一个flatten,将维度合并【5*31,64】
        self.flatten=nn.Flatten(0,1)
        #加一个线性层：[64,词库大小]
        self.linear=nn.Linear(hidden_num,word_size)
        #交叉熵
        self.cross_entropy=nn.CrossEntropyLoss()

    def forward(self,xs_embedding,h_0=None,c_0=None):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        xs_embedding=xs_embedding.to(device)
        if h_0==None or c_0==None:
            #num_layers,batch_size,hidden_size
            h_0=torch.tensor(np.zeros((2,xs_embedding.shape[0],self.hidden_num),np.float32))
            c_0 = torch.tensor(np.zeros((2, xs_embedding.shape[0], self.hidden_num),np.float32))
        h_0=h_0.to(device)
        c_0=c_0.to(device)
        hidden,(h_0,c_0)=self.lstm(xs_embedding,(h_0,c_0))
        hidden_drop=self.dropout(hidden)
        flatten_hidden=self.flatten(hidden_drop)
        pre=self.linear(flatten_hidden)
        return pre,(h_0,c_0)

def qi_cang_poem(res):
    all_data, (w1, word_2_index, index_2_word) = qi_train_vec()
    model_result_file = 'templates/qi_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    return qi_cang(res, model, word_2_index, index_2_word, w1)

def qi_gen_poem(res):
    all_data, (w1, word_2_index, index_2_word) = qi_train_vec()
    model_result_file = 'templates/qi_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    # qi_cang("风花雪月", model, word_2_index, index_2_word, w1)
    return qi_generate_poetry_auto(res, model, word_2_index, index_2_word, w1)


def wu_cang_poem(res):
    all_data, (w1, word_2_index, index_2_word) = train_vec()
    model_result_file = 'templates/wu_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    return cang(res, model, word_2_index, index_2_word, w1)


def wu_gen_poem(res):
    all_data, (w1, word_2_index, index_2_word) = train_vec()
    model_result_file = 'templates/wu_poem/model_lstm.pkl'
    model = pickle.load(open(model_result_file, "rb"))
    # qi_cang("风花雪月", model, word_2_index, index_2_word, w1)
    return generate_poetry_auto(res, model, word_2_index, index_2_word, w1)

if __name__ == '__main__':
    wu_gen_poem("草")