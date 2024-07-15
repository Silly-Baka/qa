from py2neo import Graph
from function.answer import question_classifier
from function.answer import generate_sqls
from function.answer.utils import *


class answerearcher:
    def __init__(self):
        self.g = Graph(neo4j_address, auth = (neo4j_username, neo4j_password))   # 修改对应的neo4j用户名和密码

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
                    final_answer.append(answerTemplates[i].format(answers[0]['payer.name'], answers[0]['category.name']))
                    # TODO 这里写推荐的逻辑，如常买类别为零食、餐饮等，就推荐饭卡信用卡并介绍相关的信息
                    #      最好是在图里新增这样的数据， 零食节点 ——> [:适合推荐的业务] ——> 信用卡节点

                    # 从neo4j中找出该商品类型适合推荐的产品
                    categoryName = answers[0]['category.name']
                    recommend_service = []
                    sql = f"MATCH (t:`商品类别`)-[r:`推荐业务`]->(c:`信用卡`) WHERE t.name = '{categoryName}' RETURN c"
                    result = self.g.run(sql)
                    # TODO 待改造为通用逻辑
                    for record in result:
                        card = result['c']
                        final_answer.append(
                            f"该用户适合推荐信用卡:{card['name']}")
                        final_answer.append(f"该卡详细信息为:{card['description']}")

        return final_answer

    def main(self,sqls):
        reault= self.search_in_database(sqls)
        print('result:', reault)
        answer = self.answer_template(reault)
        return answer



if __name__ == "__main__":
    question='郑辛茹购买最多的商品类别是什么？'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    ans=searcher.main(b)
    print('ans:',ans)