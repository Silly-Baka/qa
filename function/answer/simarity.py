"""
余弦距离
曼哈顿距离
欧式距离
"""
import pandas as pd
import scipy.spatial.distance as dist
from bert_serving.client import BertClient
import re
import distance
import jieba
# import fool
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer
class similarity:
    # 编辑距离
    def edit_distance(self,s1, s2):
        return distance.levenshtein(s1, s2)

    # TF-IDF
    def tfidf_similarity(self,s1, s2):
        def add_space(s):
            w = jieba.cut(s)
            a = ' '.join(w)
            return a
        # 将字中间加入空格
        s1, s2 = add_space(s1), add_space(s2)

        # 转化为TF矩阵
        cv = TfidfVectorizer(tokenizer=lambda s: s.split())
        corpus = [s1, s2]
        vectors = cv.fit_transform(corpus).toarray()
        values= np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))
        return values

    # jescar距离
    def jaccard_similarity(self,s1, s2):
        def add_space(s):
            return ' '.join(list(s))

        # 将字中间加入空格
        s1, s2 = add_space(s1), add_space(s2)
        # 转化为TF矩阵
        cv = CountVectorizer(tokenizer=lambda s: s.split())
        corpus = [s1, s2]
        vectors = cv.fit_transform(corpus).toarray()
        # 求交集
        numerator = np.sum(np.min(vectors, axis=0))
        # 求并集
        denominator = np.sum(np.max(vectors, axis=0))
        # 计算杰卡德系数
        values =1.0 * numerator / denominator
        return values

    def cosine (self,v1,v2):
        value = dist.cosine(v1, v2)
        return value

    # 计算欧式距离
    def euclidean(self,v1,v2):

        value = dist.euclidean(v1, v1)
        return value

    # 计算曼哈顿距离
    def Manhattan(self,v1,v2):
        value = dist.minkowski(v1,v2, p=1)
        return value

    def bertvetor(self,s1,s2):
        bc = BertClient()
        text1 = re.sub('[  ，【】！!。：:～、;@#%*()？_‘’“”''***]', '', s1)
        text2 = re.sub('[  ，【】！!。：:～、;@#%*()？_‘’“”''***]', '', s2)
        a = bc.encode([text1, text2])  # 768
        return a








