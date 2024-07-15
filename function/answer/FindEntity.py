"""
1,相似度计算，停用词过滤，词标准化，,

"""
import jieba
# import fool
import pickle
import json
import difflib
# import ahocorasick
from function.answer import simarity
from function.answer.utils import *
import copy


class FindEntity_base_similarity:
    """
    基于相似度
    """

    def __init__(self):
        with open(entity_path, 'r', encoding='utf-8') as f:
            self.entity_type = json.load(f)

    def stop(self, sentence):  # 去掉停止词
        jieba.load_userdict(one_path)
        # 这里wordlist已经分词了
        wordlist = list(jieba.cut(sentence))
        # wordlist = fool.cut(sentence)[0]            # 分词
        stopwords = ['购买', '最多', '的', '是', '什么', '最常', '进行', '消费', '可以', '为', '做', '一些', '嘛']
        a = copy.deepcopy(wordlist)
        for item in a:
            if item in stopwords:
                wordlist.remove(item)
        return wordlist

    def entity_candidate(self, question):
        # similarity是simarity.py文件中similarity类型的实体对象
        similarity = simarity.similarity()
        # 分词，去掉停止词
        wordlist = self.stop(question)
        print('worl', wordlist)
        target = []
        # 遍历wordlist中每一个元素
        for item in wordlist:
            temp = []
            # 遍历entity.txt中的每一个关键字
            for entity in self.entity_type.keys():
                # 如果wordlist中的一个元素item在entity中
                if item == entity:
                    idfsim = similarity.tfidf_similarity(question, entity)
                    if idfsim > 0.2:
                        temp.append((item, entity, idfsim))
            if temp:
                target.append(temp)
        print('target',target)
        return target

    def best_entity(self, candidate):
        final = []
        for item in candidate:
            # 找出所有item中具有最大第三个元素的item
            best = max(item, key=lambda x: x[2])
            final.append(best)
        print('final', final)
        return final

    def main(self, question):
        target = self.entity_candidate(question)  # 分词，输出词与实体库中的词的相似度
        entitys = self.best_entity(target)  # 找出相似度最大的target
        final_dict = {}
        # 遍历每一个三元组
        for entity in entitys:
            # self.entity_type是一个字典，内容如下：{'张三': 'name', '李四': 'name', '篮球': 'hobby', '音乐': 'hobby', '四川': 'hometown', '甘肃': 'hometown', '东7601': 'live', '2': 'person'}
            # 返回实体对应的标签
            final_dict[entity[1]] = self.entity_type[entity[1]]
        return final_dict


if __name__ == '__main__':
    finder = FindEntity_base_similarity()
    question = '张三的爱好是什么？'
    # question = '新开普是什么行业'
    # f2=FindEntity_base_AC()
    # e2=f2.main(question)
    # print(e2,'ac')
    entity = finder.main(question)
    print(entity, 'xiangsidu1')
