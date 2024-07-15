from function.answer import FindEntity
from function.answer import FindRelation


def classify(question):
    relationfinder=FindRelation.findrelation_base_keywords()
    entityfinder = FindEntity.FindEntity_base_similarity()
    relation_types = relationfinder.main(question)  # str
    # relation_type会得到一个列表，列表中存储了无重复的问题类型字符串
    # relation_type例如['UNhobby']
    relation_type = relationfinder.main(question)  # str
    # print('relation_type:', relation_type)

    # 查询相关的实体标签，作为参数构造sql，将被构造为问题标签
    entity_types = entityfinder.main(question)

    # print('entity_type:', entity_type)

    if not entity_types:
        return {}
    # 问题类型列表

    # 收集问句当中所涉及到的实体类型
    question_types = []

    # 参数列表_问题标签 --> 组合成问题类型，可用于索引到实际的处理逻辑
    for relation_type in relation_types:
        str = ''
        for type in entity_types.values():
            str += type+'_'
        str += relation_type
        question_types.append(str)
    # for i in relation_type:
    #     for type in entity_type.values():
    #         # question_types是一个列表，每个元素是"实体类型_问题类型"这样的全排列组合
    #         # question_types例如['name_UNhobby']
    #         question_types.append(type+'_'+i)
    data = {}
    data['args'] = entity_types
    data['question_types'] = question_types
    # data是一个字典，args这个key里面存放entity_type这个实体为key，类型为值的字典
    # question_types这个key里面存放question_types这个"实体类型_问题类型"这样的全排列组合的列表
    return data #{'args': {'珠海科德电子有限公司': ['comapny']}, 'question_types': ['comapny_belong_concept']}


if __name__ == "__main__":
    question = '黄嘉桓购买最多的商品类别是什么？'
    print(classify(question))