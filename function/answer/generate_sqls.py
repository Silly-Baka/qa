from .utils import *


def generate_sql(data):
    # args用于获取实体信息，args例如{'张三': 'name'}

    sqls = []

    if(data == {}):
        sqls.append({'question_type': 'payer_UNCommon', 'sql': '1'})
        return sqls

    args = data['args']
    print(11111111111111111111111111111, args)



    # questions为所有"实体类型_问题类型"这样全排列的一个个
    # questions例如name_UNhobby
    for quetions in data['question_types']:
        print(22222222222222222222222222222222, quetions)
        # questionType是列表，包含了事先准备的所有准备好的"实体类型_问题类型"的组合
        for j in range(len(questionType)):
            # 如果questions例如name_UNhobby等于questionType中的某个元素，即questionType中的某个元素此时为nameUNhobby
            if quetions == questionType[j]:
                print(quetions, questionType[j])
                # 使用一种特殊的规则方法生成非经典的sql语句
                # headTag宽泛表示实体类型
                # tailTag宽泛表示问题类型
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
    return sqls