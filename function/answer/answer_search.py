from py2neo import Graph
from function.answer import question_classifier
from function.answer import generate_sqls
from function.answer import utils

class answerearcher:
    def __init__(self):
        self.g = Graph(utils.neo4j_address, auth = (utils.neo4j_username, utils.neo4j_password))   # 修改对应的neo4j用户名和密码

        # self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''
    def search_in_database(self,sqls):
        num_limit = 20
        result = {}
        # 从sqls中拿出一条条例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]的元素
        for sql_ in sqls:
            # print(44444444444444444444444444444444, sqls)
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
            result['question_type'] = question_type
            result['answer'] = answer
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
            # print(777777777777777777777777, answers)
            if(answers == '1'):
                final_answer = "你好，我是红棉助手，有什么可以帮您~"
                return final_answer

            for i in range(len(utils.questionTypes)):
                if question_type== utils.questionTypes[i]:
                    if question_type == '用户_most_type':
                        payerName = answers[0]['payer.name']
                        categoryName = answers[0]['category.name']
                        final_answer.append(utils.answerTemplates[i].format(payerName, categoryName))
                        # 将商品类别信息保存
                        utils.pre_entity_types[categoryName] = '商品类别'

                    if question_type == '用户_商品类别_recommend':
                        # DONE 这里写推荐的逻辑，如常买类别为零食、餐饮等，就推荐饭卡信用卡并介绍相关的信息
                        #      最好是在图里新增这样的数据， 零食节点 ——> [:适合推荐的业务] ——> 信用卡节点
                        for record in answers:
                            card = record['c']
                            final_answer.append(
                                f"该用户适合推荐信用卡:{card['name']}")
                            final_answer.append(f"{card['description']}")
                    if question_type == '亲属_recommend':
                        services = []
                        for record in answers:
                            service = record['p']
                            services.append(service['name'])
                        final_answer.append(
                            f"适合给这些用户推荐以下业务：{'，'.join(set(services))}"
                        )

                    if question_type == 'NONE_parent':
                        payers = []
                        for record in answers:
                            payer = record['payer']
                            payers.append(payer['name'])
                        print(payers)
                        final_answer.append(
                            f"以下用户与疑似亲属有过相关流水记录: {'，'.join(payers)}"
                        )
                        utils.pre_entity_types['亲属'] = '亲属'   # 作为亲属相关问题的标志位
                    if question_type == '用户_parent':
                        receivers = []
                        for record in answers:
                            receiver = record['receiver']
                            receivers.append({
                                "用户名": receiver['name'],
                                "用户电话": '1xxxxxxx',
                                "其余信息": '暂无信息来源'
                            })
                        print(receiver)
                        final_answer.append(
                            f"该用户的疑似亲属如下: {receivers}"
                        )
                        utils.pre_entity_types['亲属'] = '亲属'  # 作为亲属相关问题的标志位

                # 遍历预先定义好的questionType中每个元素
                # for i in range(len(questionType)):
                #     # 如果该问题的"实体类型_问题类型"包含在预先定义好的questionType这个例表中
                #     if question_type==questionType[i]:
                #         item1_set=set()
                #         item2=''
                #         # 遍历answers中的每个元素
                #         for answer in answers:
                #             print(888888888888888888888888888888888, answer)
                #             # item1_set用于存放例如篮球这样的答案
                #             item1_set.add(answer['商品类别'])
                #             # item2用于存放原有的实体
                #             item2 = answer['付款人姓名']
                #         # 将item_set中的每个元素转换为字符串，并使用逗号连接起来形成新的字符串
                #         item1 = ','.join(item1_set)
                #         print(999999999999999999999999999999, item1)
                #         print("item166666666666666666666666666", item1)
                #         # 前面的i可以定位是第几类问题，然后该类问题的回答模板也对应第i + 1个answerTemple中的元素
                #         template = f'{item2}{answerTemple[i]}{item1}。'
                #         final_answer = template
                #         if(i == 2):
                #             template = f'没问题，{item2}购买最多的商品类别是{item1}，推荐广州银行饭卡白金信用卡，其详细介绍如下面网址：https://ccmp.creditcard.gzcb.com.cn。'
                #             final_answer = template
        # final_answer就是最后会显示出来的回答
        return final_answer

    def main(self,sqls):
        # sqls例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
        reault= self.search_in_database(sqls)
        print('result:', reault)
        answer = self.answer_template(reault)
        return answer



if __name__ == "__main__":
    question='黄嘉桓最常购买的商品类别？'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    # b例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
    # b就为非经典的sql语句
    ans=searcher.main(b)
    print('ans:',ans)

    question = '汤继锐疑似亲属的相关信息'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    # b例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
    # b就为非经典的sql语句
    ans=searcher.main(b)
    print('ans:',ans)

    question = '这些用户适合推荐什么业务'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    # b例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
    # b就为非经典的sql语句
    ans=searcher.main(b)
    print('ans:',ans)
