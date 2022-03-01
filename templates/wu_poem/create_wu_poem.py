import torch
import torch.nn as nn
import numpy as np
from gensim.models.word2vec import Word2Vec
import pickle
from torch.utils.data import Dataset,DataLoader
import os

def split_poetry(file='wu_jueju.txt'):
    all_data=open(file,"r",encoding="utf-8").read()
    all_data_split=" ".join(all_data)
    with open("split.txt","w",encoding='utf-8') as f:
        f.write(all_data_split)

def train_vec(split_file='split.txt',org_file='wu_jueju.txt'):
    #word2vec模型
    vec_params_file="vec_params.pkl"
    #判断切分文件是否存在，不存在进行切分
    if os.path.exists(split_file)==False:
        split_poetry()
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

class MyDataset(Dataset):
    #数据打包
    #加载所有数据
    #存储和初始化变量
    def __init__(self,all_data,w1,word_2_index):
        self.w1=w1
        self.word_2_index=word_2_index
        self.all_data=all_data


    #获取一条数据，并做处理
    def __getitem__(self, index):
        a_poetry_words = self.all_data[index]
        a_poetry_index = [self.word_2_index[word] for word in a_poetry_words]

        xs_index = a_poetry_index[:-1]
        ys_index = a_poetry_index[1:]

        #取出31个字，每个字对应107维度向量，【31,107】
        xs_embedding=self.w1[xs_index]

        return xs_embedding,np.array(ys_index).astype(np.int64)

    #获取数据总长度
    def __len__(self):
        return len(self.all_data)

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

def generate_poetry_auto():

    result=''
    #随机产生第一个字的下标
    word_index=np.random.randint(0,word_size,1)[0]
    result += index_2_word[word_index]
    h_0 = torch.tensor(np.zeros((2, 1, hidden_num), np.float32))
    c_0 = torch.tensor(np.zeros((2, 1, hidden_num), np.float32))

    for i in range(23):
        word_embedding=torch.tensor(w1[word_index].reshape(1,1,-1))
        pre,(h_0,c_0)=model(word_embedding,h_0,c_0)
        word_index=int(torch.argmax(pre))
        result+=index_2_word[word_index]
    print(result)


if __name__ == '__main__':

    device="cuda" if torch.cuda.is_available() else "cpu"
    print(device)

    #源数据小了，batch不能太大
    batch_size=128
    all_data,(w1,word_2_index,index_2_word)=train_vec()
    dataset=MyDataset(all_data,w1,word_2_index)
    dataloader=DataLoader(dataset,batch_size=batch_size,shuffle=True)

    epoch=1000
    word_size , embedding_num=w1.shape
    lr=0.003
    hidden_num=128
    model_result_file='model_lstm.pkl'
#测试代码
    # if os.path.exists(model_result_file):
    #     model=pickle.load(open(model_result_file, "rb"))
    # generate_poetry_auto()
#训练代码
    model=Mymodel(embedding_num,hidden_num,word_size)
    #放入gpu训练
    model.to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=lr)

    for e in range(epoch):
        #按照指定的batch_size获取诗词条数【32,31,107】
        #ys_index:torch.Size([32,31])
        for batch_index,(xs_embedding,ys_index) in enumerate(dataloader):
            xs_embedding=xs_embedding.to(device)
            ys_index=ys_index.to(device)


            pre,_=model.forward(xs_embedding)
            loss=model.cross_entropy(pre,ys_index.reshape(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch_index%100==0:
                print(f"loss:{loss:.3f}")
                generate_poetry_auto()



    pickle.dump(model, open(model_result_file, "wb"))