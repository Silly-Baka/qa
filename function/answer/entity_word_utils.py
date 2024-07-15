
'''实体关键词处理用工具类'''
import json

from py2neo import Graph

from function.answer.utils import entity_path
from utils import *


class EntityWordUtils:
    def __init__(self):
        self.graph = Graph(neo4j_address, auth = (neo4j_username, neo4j_password))
        self.json_dict = dict()
        self.get_all_labels_names()

    '''获取neo4j中所有的标签'''
    def labels(self):
        result = self.graph.run("CALL db.labels()")
        labels = [record["label"] for record in result]
        return labels

    '''获取neo4j中所有标签为label的节点名字，并写成json格式'''
    def names(self, label):
        sql = f"match (p: {label}) return p.name"
        result = self.graph.run(sql)
        names = [record["p.name"] for record in result]
        for name in names:
            self.json_dict[name] = label

    '''获取neo4j中所有的标签并写入文件entity.txt中'''
    def get_all_labels_names(self):
        labels = self.labels()
        for label in labels:
            self.names(label)
        json_str = json.dumps(self.json_dict, ensure_ascii=False)
        print(json_str)

        # 写入文件中
        with open(entity_path, 'w', encoding='utf-8') as f:
            f.write(json_str)

if __name__ == '__main__':
    EntityWordUtils()