"""
1,相似度计算，停用词过滤，词标准化，,

"""
import jieba
# import fool
import pickle
import json
import difflib
#import ahocorasick
from function.answer import simarity
from function.answer.utils import *
import copy
class FindEntity_base_similarity:
    """s
    基于相似度
    """
    def __init__(self):
        with open(entity_path, 'r', encoding='utf-8') as f:
            self.entity_type=json.load(f)

    def stop (self,sentence):          # 去掉停止词
        jieba.load_userdict(segment_word_path)   # 加载个人分词词典
        wordlist = list(jieba.cut(sentence))
        #wordlist = fool.cut(sentence)[0]            # 分词
        stopwords=['有', '属于','哪里','哪些', '和','在','的']   # 停止词列表
        a=copy.deepcopy(wordlist)
        for item in a:
            if item in stopwords:
                wordlist.remove(item)
        return wordlist

    def entity_candidate(self,question):
        similarity=simarity.similarity()
        wordlist=self.stop(question)           # 分词，去掉停止词
        # print('worl',wordlist)
        target=[]
        for item in wordlist:
            temp=[]
            for entity in self.entity_type.keys():
                # print(entity)
                if item in entity:
                    idfsim = similarity.tfidf_similarity(question, entity)
                    # print(item, entity, idfsim)
                    if idfsim>0.2:
                        temp.append((item, entity,idfsim))
            if temp:
                target.append(temp)
        # print('target',target)
        return target

    def best_entity(self,candidate):
        final=[]
        for item in candidate:
            best=max(item,key=lambda x:x[2])
            final.append(best)
        # print('final',final)
        return final

    def main(self,question):
        target=self.entity_candidate(question)    # 分词，输出词与实体库中的词的相似度
        entitys=self.best_entity(target)          # 找出相似度最大的target
        final_dict = {}
        for entity in entitys:
            final_dict[entity[1]]=self.entity_type[entity[1]]         # 返回实体对应的标签
        return final_dict



if __name__=='__main__':
        finder=FindEntity_base_similarity()
        question = '黄嘉桓购买最多的商品类别是什么？'
        # question = '新开普是什么行业'
        # f2=FindEntity_base_AC()
        # e2=f2.main(question)
        # print(e2,'ac')
        entity = finder.main(question)
        print(entity, 'xiangsidu1')
