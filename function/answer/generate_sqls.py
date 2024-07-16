from function.answer import utils
from function.answer.utils import questionTypes


def generate_sql(data):
    # args用于获取实体信息，args例如{'张三': 'name'}

    sqls = []

    if data == {}:
        sqls.append({'question_type': 'payer_UNCommon', 'sql': '1'})

        return sqls

    args = data['args']
    print(11111111111111111111111111111, args)

    # questions为所有"实体类型_问题类型"这样全排列的一个个
    # questions例如name_UNhobby
    for quetions in data['question_types']:
        # for j in range(len(questionType)):
        #     if quetions == questionType[j]:
        #         # 该sql仅支持 a -> 关系 -> c 这样的数据模式
        #         sql = [
        #             f"MATCH(m:{headTag[j]})-[r:{headTag[j]}_{tailTag[j]}]->(n:{tailTag[j]}) where m.name='{i}' return n.name, m.name"
        #             for i in args.keys()]

        print(22222222222222222222222222222222, quetions)
        # questionType是列表，包含了事先准备的所有准备好的"实体类型_问题类型"的组合
        for j in range(len(questionTypes)):
            # 如果questions例如name_UNhobby等于questionType中的某个元素，即questionType中的某个元素此时为nameUNhobby
            if quetions == questionTypes[j]:
                print(quetions, questionTypes[j])
                # 使用一种特殊的规则方法生成非经典的sql语句
                # headTag宽泛表示实体类型
                # tailTag宽泛表示问题类型

                # TODO: 待完善代码逻辑、匹配逻辑（关键字、问题类型等）
                if quetions == '付款方_most_type':
                    name = ''
                    for key in args.keys():
                        if args[key] == '付款方':
                            name = key
                    sql = [
                        f"MATCH (payer:付款方 {{name: '{name}'}})-[:付款]->(transaction:流水)-[:属性]->(category:商品类别)\
                        RETURN payer.name, category.name, COUNT(transaction) AS TransactionsCount\
                        ORDER BY TransactionsCount DESC\
                        LIMIT 1"
                    ]
                if quetions == '付款方_recommend':
                    categoryName = ''
                    for key in args.keys():
                        if args[key] == '商品类别':
                            categoryName = key
                    sql = [
                        f"MATCH (t:`商品类别`)-[r:`推荐业务`]->(c:`信用卡`) WHERE t.name = '{categoryName}' RETURN c"
                    ]

                if(quetions == 'payer_UNtype'):
                    sql = [
                        f"MATCH (payer:付款方)-[:付款]->(tran:流水)-[:属性_商品类别]->(type:商品类别) where payer.name='{i}' "
                        f"WITH payer, type, COUNT(tran) AS 消费次数 RETURN payer.name AS 付款人姓名, type.name AS 商品类别 ORDER BY 消费次数 DESC LIMIT 1" for i in args.keys()]
                    print(3333333333333333333333333333333333333333333, sql)
                if (quetions == 'payer_UNplace'):
                    sql = [
                        f"MATCH (payer:付款方)-[:付款]->(tran:流水)-[:属性_交易地点]->(place:交易地点) where payer.name='{i}' "
                        f"WITH payer, place, COUNT(tran) AS 消费次数 RETURN payer.name AS 付款人姓名, place.name AS 商品类别 ORDER BY 消费次数 DESC LIMIT 1"
                        for i in args.keys()]
                    print(3333333333333333333333333333333333333333333, sql)
                if (quetions == 'payer_UNrecommend'):
                    sql = [
                        f"MATCH (payer:付款方)-[:付款]->(tran:流水)-[:属性_商品类别]->(type:商品类别) where payer.name='{i}' "
                        f"WITH payer, type, COUNT(tran) AS 消费次数 RETURN payer.name AS 付款人姓名, type.name AS 商品类别 ORDER BY 消费次数 DESC LIMIT 1"
                        for i in args.keys()]
                    print(3333333333333333333333333333333333333333333, sql)
                if sql:
                    # 如果sql不为空，则在sqls中添加一个字典
                    # 字典的格式如下
                    # {'question_type': 'name_UNhobby', 'sql': ["MATCH(m:name)-[r:name_hobby]->(n:hobby) where m.name='张三' return n.name, m.name"]}s
                    sqls.append({'question_type': quetions, 'sql': sql})
        print(sqls)
    return sqls
