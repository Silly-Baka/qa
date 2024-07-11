from .utils import *


def generate_sql(data):
    args = data['args']
    sqls = []
    for quetions in data['question_types']:
        # for j in range(len(questionType)):
        #     if quetions == questionType[j]:
        #         # 该sql仅支持 a -> 关系 -> c 这样的数据模式
        #         sql = [
        #             f"MATCH(m:{headTag[j]})-[r:{headTag[j]}_{tailTag[j]}]->(n:{tailTag[j]}) where m.name='{i}' return n.name, m.name"
        #             for i in args.keys()]

        # TODO: 待完善代码逻辑、匹配逻辑（关键字、问题类型等）
        if quetions == '付款方_商品类别_most_type':
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
            if sql:
                sqls.append({'question_type': quetions, 'sql': sql})
    return sqls
