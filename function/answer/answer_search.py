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
            # 假如输入例如"你好"这样的查不出关键字的情况，就将问题类型置为'payer_UNCommon'
            # 这种情况下，在后面的代码中会直接回复"你好，我是红棉助手，有什么可以帮您~"
            if(queries == '1'):
                result = {'question_type': 'payer_UNCommon', 'answer': '1'}
                return result
            answer= []
            # query是一条字符串，query例如"MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"
            for query in queries:
                ress = self.g.run(query).data()
                print(123123123123123123123123123123123, ress)
                answer+= ress
                print(111222333111222333111222333111222, answer)

            # # answer例如[{'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}]
            result['question_type'] = question_type
            result['answer'] = answer
        return result

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_template(self, result):
        # question_type例如name_UNhobby
        question_type = result['question_type']
        final_answer = []

        # 如果能搜到关键字，即data并不是空，但是用关键字搜数据库没有答案，则回复"哎呀抱歉了，暂时没有答案，红棉助手会尽快优化~"
        if not result['answer']:
            return '哎呀抱歉了，暂时没有答案，红棉助手会尽快优化~'
        else:
            # answers例如[{'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}, {'n.name': '篮球', 'm.name': '张三'}]
            answers = result['answer']
            # print(777777777777777777777777, answers)
            # 假如输入例如"你好"这样的查不出关键字的情况，就将问题类型置为'payer_UNCommon'
            # 这种情况下，在后面的代码中会直接回复"你好，我是红棉助手，有什么可以帮您~"
            if(answers == '1'):
                final_answer = "你好，我是红棉助手，有什么可以帮您~"
                return final_answer

            for i in range(len(utils.questionTypes)):
                if question_type== utils.questionTypes[i]:
                    # 根据question_type进行if判断
                    if question_type == '付款方_most_type':
                        # answer的格式例如[{'payer.name': '黄嘉桓', 'category.name': '娱乐', 'TransactionsCount': 616}]
                        payerName = answers[0]['payer.name']
                        categoryName = answers[0]['category.name']
                        final_answer.append(utils.answerTemplates[i].format(payerName, categoryName))
                        # 将商品类别信息保存
                        # 这里是关键之一，在回答问题后，将当前信息存储进pre_entity_types以回答下一轮问题
                        utils.pre_entity_types[categoryName] = '商品类别'

                    if question_type == '付款方_recommend':
                        # TODO: 这里写推荐的逻辑，如常买类别为零食、餐饮等，就推荐饭卡信用卡并介绍相关的信息
                        #  最好是在图里新增这样的数据， 零食节点 ——> [:适合推荐的业务] ——> 信用卡节点
                        # 这个是一开始手动添加的
                        for record in answers:
                            # record例如{'c': Node('信用卡', description='权益有效期内，使用广州银行X系列（玩儿卡卡版）进行移动
                            # 支付消费或分期，满足达标条件，可获得以下权益三选一：\r\n【消费达标·白银好礼】：每个自然月累计达成6笔移动支付消费（每天仅计1笔
                            # 且每笔金额达66元，即可获白银权益专区兑换资格，可任选一款奖励兑换，奖品价值最高30元；\r\n【分期达标·铂金好礼】：每个自然月分分
                            # 金额累计达1000元或以上且分期期数达12期或以上，即可获铂金权益专区兑换资格，可任选一款奖励兑换，奖品价值最高50元；\r\n【分期
                            # 达标·黑金好礼】：每个自然月分期金额累计达2000元或以上且分期期数达12期或以上，即可获黑金权益专区兑换资格，可任选一款奖励兑换，
                            # 品价值最高100元；\r\n注：分期仅包括消费分期及账单分期，不含现金分期。\r\n客户可在每档权益专区自由选择视频影音、餐饮外卖代金金、出行打车券及返现券等奖品进行兑换哦，超过30款权益奖品等你来拿！\r\n积分政策', name='广州银行玩儿卡')}
                            print(789789789789789789789789789789789789, record)
                            # answer例如[{'c': Node('信用卡', description='权益有效期内，使用广州银行X系列（玩儿卡卡版）进行移动
                            # 付消费或分期，满足达标条件，可获得以下权益三选一：\r\n【消费达标·白银好礼】：每个自然月累计达成6笔移动支付消费（每天仅计1笔笔
                            # 且每笔金额达66元，即可获白银权益专区兑换资格，可任选一款奖励兑换，奖品价值最高30元；\r\n【分期达标·铂金好礼】：每个自然月分分
                            # 金额累计达1000元或以上且分期期数达12期或以上，即可获铂金权益专区兑换资格，可任选一款奖励兑换，奖品价值最高50元；\r\n【分期
                            # 达标·黑金好礼】：每个自然月分期金额累计达2000元或以上且分期期数达12期或以上，即可获黑金权益专区兑换资格，可任选一款奖励兑换，
                            # 品价值最高100元；\r\n注：分期仅包括消费分期及账单分期，不含现金分期。\r\n客户可在每档权益专区自由选择视频影音、餐饮外卖代金金、出行打车券及返现券等奖品进行兑换哦，超过30款权益奖品等你来拿！\r\n积分政策', name='广州银行玩儿卡')}]
                            print(567567567567567567567576567567567567, answers)
                            card = record['c']
                            print(123456789123456789123456789, card)
                            # card是Node('信用卡', description='权益有效期内...')
                            # card例如(_25403:信用卡 {description: '\u6743\u76ca\u6709\u6548\u671f\u5185\uff0c\u4f7f\u7528\u5e7f\u5dde\
                            # u94f6\u884cX\u7cfb\u5217\uff08\u73a9\u513f\u5361\u5361\u7248\uff09\u8fdb\u884c\u79fb\u52a8\u652f\u4ed8\u6d88\u8d39\u6216\u520
                            # 6\u671f\uff0c\u6ee1\u8db3\u8fbe\u6807\u6761\u4ef6\uff0c\u53ef\u83b7\u5f97\u4ee5\u4e0b\u6743\u76ca\u4e09\u9009\u4e00\uff1a\r\n
                            # \u3010\u6d88\u8d39\u8fbe\u6807\u00b7\u767d\u94f6\u597d\u793c\u3011\uff1a\u6bcf\u4e2a\u81ea\u7136\u6708\u7d2f\u8ba1\u8fbe\u621
                            # 06\u7b14\u79fb\u52a8\u652f\u4ed8\u6d88\u8d39\uff08\u6bcf\u5929\u4ec5\u8ba11\u7b14\uff09\u4e14\u6bcf\u7b14\u91d1\u989d\u8fbe66
                            # \u5143\uff0c\u5373\u53ef\u83b7\u767d\u94f6\u6743\u76ca\u4e13\u533a\u5151\u6362\u8d44\u683c\uff0c\u53ef\u4efb\u9009\u4e00\u6b3
                            # e\u5956\u52b1\u5151\u6362\uff0c\u5956\u54c1\u4ef7\u503c\u6700\u9ad830\u5143\uff1b\r\n\u3010\u5206\u671f\u8fbe\u6807\u00b7\u94
                            # c2\u91d1\u597d\u793c\u3011\uff1a\u6bcf\u4e2a\u81ea\u7136\u6708\u5206\u671f\u91d1\u989d\u7d2f\u8ba1\u8fbe1000\u5143\u6216\u4ee
                            # 5\u4e0a\u4e14\u5206\u671f\u671f\u6570\u8fbe12\u671f\u6216\u4ee5\u4e0a\uff0c\u5373\u53ef\u83b7\u94c2\u91d1\u6743\u76ca\u4e13\u
                            # 533a\u5151\u6362\u8d44\u683c\uff0c\u53ef\u4efb\u9009\u4e00\u6b3e\u5956\u52b1\u5151\u6362\uff0c\u5956\u54c1\u4ef7\u503c\u6700\
                            # u9ad850\u5143\uff1b\r\n\u3010\u5206\u671f\u8fbe\u6807\u00b7\u9ed1\u91d1\u597d\u793c\u3011\uff1a\u6bcf\u4e2a\u81ea\u7136\u6708
                            # \u5206\u671f\u91d1\u989d\u7d2f\u8ba1\u8fbe2000\u5143\u6216\u4ee5\u4e0a\u4e14\u5206\u671f\u671f\u6570\u8fbe12\u671f\u6216\u4ee
                            # 5\u4e0a\uff0c\u5373\u53ef\u83b7\u9ed1\u91d1\u6743\u76ca\u4e13\u533a\u5151\u6362\u8d44\u683c\uff0c\u53ef\u4efb\u9009\u4e00\u6b
                            # 3e\u5956\u52b1\u5151\u6362\uff0c\u5956\u54c1\u4ef7\u503c\u6700\u9ad8100\u5143\uff1b\r\n\u6ce8\uff1a\u5206\u671f\u4ec5\u5305\u
                            # 62ec\u6d88\u8d39\u5206\u671f\u53ca\u8d26\u5355\u5206\u671f\uff0c\u4e0d\u542b\u73b0\u91d1\u5206\u671f\u3002\r\n\u5ba2\u6237\u5
                            # 3ef\u5728\u6bcf\u6863\u6743\u76ca\u4e13\u533a\u81ea\u7531\u9009\u62e9\u89c6\u9891\u5f71\u97f3\u3001\u9910\u996e\u5916\u5356\u
                            # 4ee3\u91d1\u5238\u3001\u51fa\u884c\u6253\u8f66\u5238\u53ca\u8fd4\u73b0\u5238\u7b49\u5956\u54c1\u8fdb\u884c\u5151\u6362\u54e6\
                            # uff0c\u8d85\u8fc730\u6b3e\u6743\u76ca\u5956\u54c1\u7b49\u4f60\u6765\u62ff\uff01\r\n\u79ef\u5206\u653f\u7b56', name: '\u5e7f\u5dde\u94f6\u884c\u73a9\u513f\u5361'})

                            # card是一个neo4j的节点信息，包括description和name属性
                            # name属性可通过card['name']拿到
                            final_answer.append(
                                f"该用户适合推荐信用卡:{card['name']}")
                            final_answer.append(f"该卡详细信息为:{card['description']}")

                    if(question_type == '交易金额_analysis'):
                        # final_answer.append(
                        #     f"第一个参数是{answers[0]['n.first_quarter']}, 第二个参数是{answers[0]['n.second_quarter']}"
                        # )
                        final_answer.append(
                            f"""第一季度（1月至3月）理财交易金额总计: {answers[0]['n.first_quarter']}元。第二季度（4月至6月）理财交易金额总计: {answers[0]['n.second_quarter']}元。
                            理财交易金额在第二季度明显减少，可能受到市场利率变化或者季节性因素的影响。为了优化理财产品的推广策略，银行可以考虑：
                            \n加强针对第二季度客户的市场调研，了解其投资偏好和需求变化。
                            \n推出更具吸引力的理财产品和服务，以增加客户的投资参与度。
                            \n提供个性化的理财建议，帮助客户做出更理性的投资决策，从而提升交易活跃度和客户满意度。"""
                        )

                    if(question_type == "金额区间_potential"):
                        proportion = (answers[0]['node.two'] + answers[0]['node.three'] + answers[0]['node.four'] + answers[0]['node.five']) / (answers[0]['node.one'] + answers[0]['node.two'] + answers[0]['node.three'] + answers[0]['node.four'] + answers[0]['node.five'] + answers[0]['node.six'] + answers[0]['node.seven']) * 100
                        proportion_2 = "{:.2f}".format(proportion)
                        final_answer.append(
                            f"根据分析，消费金额在5000-30000元区间的客户群体占总人数的{proportion_2}%。这个区间的客户群体具有较大的增长潜力，可以定期分析他们的消费行为并提供相应的增值服务。"
                        )

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
    question='郑辛茹购买最多的商品类别是什么？'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    # b例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
    # b就为非经典的sql语句
    ans=searcher.main(b)
    print('ans:',ans)

    question = '她适合推荐一些什么业务?'
    a=question_classifier.classify(question)
    print('a:',a)
    b=generate_sqls.generate_sql(a)
    print('sqls:', b)
    searcher = answerearcher()
    # b例如[{'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}]
    # b就为非经典的sql语句
    ans=searcher.main(b)
    print('ans:',ans)
