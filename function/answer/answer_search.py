from py2neo import Graph
from function.answer import question_classifier
from function.answer import generate_sqls

class answerearcher:
    def __init__(self):
        self.g = Graph(
            host="localhost",
            http_port=7687,
            user="neo4j",
            password="neo4jneo4j")
        # self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_in_database(self,sqls):
        g = Graph(
            host="localhost",
            http_port=7687,
            user="neo4j",
            password="neo4jneo4j")
        num_limit = 20
        result = {}
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answer= []
            for query in queries:
                ress = g.run(query).data()
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

        if question_type=='fund_UNcompany':
            item1_set=set()
            item2=''
            for answer in answers:
                item1_set.add(answer['n.name'])      # 公司名
                item2 = answer['m.name']             # 基金名
            item1 = ','.join(item1_set)
            template = '{0}的所属基金公司为：{1}'.format(item2, item1)
            final_answer = template
        elif question_type=='company_UNfund':
            item1_set = set()
            item2 = ''
            for answer in answers:
                item1_set.add(answer['m.name'])      # 基金名
                item2 = answer['n.name']             # 公司名
            item1 = ','.join(item1_set)
            template = '{0}管理的基金有：{1}'.format(item2, item1)
            final_answer = template
        elif question_type=='fund_UNscale':
            item1_set = set()
            item2 = ''
            for answer in answers:
                item1_set.add(answer['n.name'])      # 资产规模
                item2 = answer['m.name']             # 基金名
                item1 = ','.join(item1_set)
                template = '{0}的资产规模有：{1}元'.format(item2, item1)
                final_answer = template
        elif question_type=='fund_UNindex':
            item1_set = set()
            item2 = ''
            for answer in answers:
                item1_set.add(answer['n.name'])     # 指数名
                item2 = answer['m.name']            # 基金名
                item1 = ','.join(item1_set)
                template = '{0}的所属指数为：{1}'.format(item2, item1)
                final_answer = template
        elif question_type=='index_UNfund':
            item1_set = set()
            item2 = ''
            for answer in answers:
                item1_set.add(answer['m.name'])     # 基金名
                item2 = answer['n.name']            # 指数名
                item1 = ','.join(item1_set)
                template = '{0}的所有基金有：{1}'.format(item2, item1)
                final_answer = template
        elif question_type=='fund_UNmanager':
            item1_set = set()
            item2 = ''
            for answer in answers:
                item1_set.add(answer['n.name'])  # 经理名
                item2 = answer['m.name']        # 基金名
                item1 = ','.join(item1_set)
                template = '{0}的基金经理是：{1}'.format(item2, item1)
                final_answer = template
        elif question_type=='manage_UNfund':
            item1_set = set()
            item2 = ''
            for answer in answers:
                item1_set.add(answer['m.name'])     # 基金名
                item2 = answer['n.name']            # 经理名
                item1 = ','.join(item1_set)
                template = '{0}管理的基金有：{1}'.format(item2, item1)
                final_answer = template
        return final_answer

    def main(self,sqls):
        reault= self.search_in_database(sqls)
        # print('result:', reault)
        answer = self.answer_template(reault)
        return answer



if __name__ == "__main__":
    question='华安上证180ETF所属基金公司是哪个'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    ans=searcher.main(b)
    print('ans',ans)