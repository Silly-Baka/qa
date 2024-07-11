from py2neo import Graph
from function.answer import question_classifier
from function.answer import generate_sqls
from utils import *

class answerearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474/", auth = ("neo4j", "hjh123123"))   # 修改对应的neo4j用户名和密码

        # self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_in_database(self,sqls):
        num_limit = 20
        result = {}
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answer= []
            for query in queries:
                ress = self.g.run(query).data()
                answer+= ress
            result['question_type'] = question_type
            result['answer'] = answer
        return result

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_template(self, result):
        question_type = result['question_type']
        final_answer = []
        if not result['answer']:
            return '数据缺失'
        else:
            answers = result['answer']

        for i in range(len(questionTypes)):
            if question_type==questionTypes[i]:
                # item1_set=set()
                # item2=''
                # for answer in answers:
                #     item1_set.add(answer['n.name'])
                #     item2 = answer['m.name']
                # item1 = ','.join(item1_set)
                # template = f'{item2}{answerTemplates[i]}{item1}'
                # final_answer = template
                if question_type == '付款方_商品类别_most_type':
                    final_answer = answerTemplates[i].format(answers[0]['payer.name'], answers[0]['category.name'])
        return final_answer

    def main(self,sqls):
        reault= self.search_in_database(sqls)
        print('result:', reault)
        answer = self.answer_template(reault)
        return answer



if __name__ == "__main__":
    question='黄嘉桓购买最多的商品类别是什么？'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    ans=searcher.main(b)
    print('ans:',ans)