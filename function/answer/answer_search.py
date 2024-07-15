from py2neo import Graph
from function.answer import question_classifier
from function.answer import generate_sqls
from function.answer.utils import questionTypes, answerTemplates

from .utils import *

class answerearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474/", auth = ("neo4j", "hjh123123"))   # 修改对应的neo4j用户名和密码

        # self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_in_database(self,sqls):
        num_limit = 20
        result = {}
        # 从sqls中拿出一条条例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]的元素
        for sql_ in sqls:
            print(44444444444444444444444444444444, sqls)
            # question_type例如name_UNhobby
            question_type = sql_['question_type']
            # queries例如["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]
            queries = sql_['sql']
            if(queries == '1'):
                result = {'question_type': 'payer_UNCommon', 'answer': '1'}
                return result
            answer= []
            # query是一条字符串，query例如"MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"
            for query in queries:
                ress = self.g.run(query).data()
                answer+= ress

        # # answer例如[{'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}]
        # result['question_type'] = question_type
        # result['answer'] = answer
        # result例如{'question_type': 'name_UNhobby', 'answer': [{'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}]}
        # print(666666666666666666666666666666666, result)
        return result

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_template(self, result):
        # question_type例如name_UNhobby
        question_type = result['question_type']
        final_answer = []
        if not result['answer']:
            return '哎呀抱歉了，暂时没有答案，红棉助手会尽快优化~'
        else:
            # answers例如[{'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}]
            answers = result['answer']
            print(777777777777777777777777, answers)
            if(answers == '1'):
                final_answer = "你好，我是红棉助手，有什么可以帮您~"
                return final_answer

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
        # 遍历预先定义好的questionType中每个元素
        for i in range(len(questionType)):
            # 如果该问题的"实体类型_问题类型"包含在预先定义好的questionType这个例表中
            if question_type==questionType[i]:
                item1_set=set()
                item2=''
                # 遍历answers中的每个元素
                for answer in answers:
                    print(888888888888888888888888888888888, answer)
                    # item1_set用于存放例如篮球这样的答案
                    item1_set.add(answer['商品类别'])
                    # item2用于存放原有的实体
                    item2 = answer['付款人姓名']
                # 将item_set中的每个元素转换为字符串，并使用逗号连接起来形成新的字符串
                item1 = ','.join(item1_set)
                print(999999999999999999999999999999, item1)
                print("item166666666666666666666666666", item1)
                # 前面的i可以定位是第几类问题，然后该类问题的回答模板也对应第i + 1个answerTemple中的元素
                template = f'{item2}{answerTemple[i]}{item1}。'
                final_answer = template
                if(i == 2):
                    template = f'没问题，{item2}购买最多的商品类别是{item1}，推荐广州银行饭卡白金信用卡，其详细介绍如下面网址：https://ccmp.creditcard.gzcb.com.cn。'
                    final_answer = template
        # final_answer就是最后会显示出来的回答
        return final_answer

    def main(self,sqls):
        # sqls例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
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
    # b例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
    # b就为非经典的sql语句
    ans=searcher.main(b)
    print('ans:',ans)