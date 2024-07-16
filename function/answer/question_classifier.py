from function.answer import FindEntity
from function.answer import FindRelation
from function.answer import utils


def classify(question):
    relationfinder=FindRelation.findrelation_base_keywords()
    entityfinder = FindEntity.FindEntity_base_similarity()
    relation_types = relationfinder.main(question)  # str
    # relation_type会得到一个列表，列表中存储了无重复的问题类型字符串
    # relation_type例如['UNhobby']
    # relation_type = relationfinder.main(question)  # str
    # print('relation_type:', relation_type)

    # 查询相关的实体标签，作为参数构造sql，将被构造为问题标签
    entity_types = entityfinder.main(question)

    # print('entity_type:', entity_type)

    if not entity_types and not utils.pre_entity_types:
        return {}

    # 问题类型列表
    question_types = set()

    # 参数列表_问题标签 --> 组合成问题类型，可用于索引到实际的处理逻辑

    # DONE 对上一次的关键词进行全排列再与问题标签组合
    values = list(utils.pre_entity_types.values())
    for relationType in relation_types:
        generate_combinations('', values, relationType, question_types)

    # 这一次的问题关键词与问题标签组合
    # TODO 需检查是否需要全排列，是否有可能乱序输入
    for relationType in relation_types:
        str = ''
        for type in entity_types.values():
            str += type+'_'
        str += relationType
        question_types.add(str)
    # for i in relation_type:
    #     for type in entity_type.values():
    #         # question_types是一个列表，每个元素是"实体类型_问题类型"这样的全排列组合
    #         # question_types例如['name_UNhobby']
    #         question_types.append(type+'_'+i)

    # 记录为上一次问题关键词
    args = {**utils.pre_entity_types, **entity_types}

    utils.pre_entity_types = entity_types

    question_types = list(question_types)

    data = {'args': args, 'question_types': question_types}

    # data是一个字典，args这个key里面存放entity_type这个实体为key，类型为值的字典l
    # question_types这个key里面存放question_types这个"实体类型_问题类型"这样的全排列组合的列表
    return data #{'args': {'珠海科德电子有限公司': ['comapny']}, 'question_types': ['comapny_belong_concept']}

# 根据上一个问题的实体列表，递归生成所有问题组合
def generate_combinations(current, remaining, relation_type, question_types):
    if not remaining:
        # 如果没有剩余元素，添加到结果集中
        question_types.add(current + relation_type)
        return
    for i in range(len(remaining)):
        next_remaining = remaining[:i] + remaining[i + 1:]
        generate_combinations(current, next_remaining, relation_type, question_types)
        generate_combinations(current + remaining[i] + '_', next_remaining, relation_type, question_types)

if __name__ == "__main__":
    question = '郑辛茹购买最多的商品类别是什么？'
    print(classify(question))
