from function.answer import FindEntity
from function.answer import FindRelation
from function.answer import utils


def classify(question):
    relationfinder=FindRelation.findrelation_base_keywords()
    entityfinder = FindEntity.FindEntity_base_similarity()
    # relation_types例如['recommend']
    relation_types = relationfinder.main(question)  # str
    # relation_type会得到一个列表，列表中存储了无重复的问题类型字符串
    # relation_type例如['UNhobby']

    # 查询相关的实体标签，作为参数构造sql，将被构造为问题标签
    # entity_types例如{'黄嘉桓': '付款方'}
    entity_types = entityfinder.main(question)

    if len(entity_types) == 0 and len(utils.pre_entity_types) == 0:
        entity_types['NONE'] = 'NONE'

    # 问题类型列表
    question_types = set()

    # 参数列表_问题标签 --> 组合成问题类型，可用于索引到实际的处理逻辑


    # 清除上一个问题中的NONE标签，避免bug
    utils.pre_entity_types.pop('NONE', None)

    # DONE 对上一次的关键词进行全排列再与问题标签组合
    values = list(utils.pre_entity_types.values())
    # pre_entity_types例如{'黄嘉桓': '付款方', '娱乐': '商品类别'}
    print(444444444444444444444444444, utils.pre_entity_types)
    # pre_entity_types.values()例如dict_values(['付款方', '商品类别'])
    print(555555555555555555555555555, utils.pre_entity_types.values())
    # values例如['付款方', '商品类别']
    print(666666666666666666666666666, values)
    for relationType in relation_types:
        generate_combinations('', values, relationType, question_types)

    print(333222111333222111111222333111222333, question_types)
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
    """
    :param current: ''
    :param remaining: [‘付款方’, '商品类别']
    :param relation_type: 'recommend'
    :param question_types: set()
    """
    if not remaining:
        # 如果没有剩余元素，添加到结果集中
        # 如果没有剩余元素，则将remaining的元素的全排列（全部和非全部）之后加上当前的问题类型
        # 例如{'商品类别_付款方_recommend', '商品类别_recommend', 'recommend', '付款方_recommend', '付款方_商品类别_recommend'}
        question_types.add(current + relation_type)
        return
    # 如果有上一个问题的实体和问题信息
    for i in range(len(remaining)):
        # 从remaining中去掉第`i`个元素
        next_remaining = remaining[:i] + remaining[i + 1:]
        # 第一种generate_combinations是去除第i种元素下的全排列（非全部）
        generate_combinations(current, next_remaining, relation_type, question_types)
        # 第二种generate_combinations是包含第i种元素下的全排列（全部）
        generate_combinations(current + remaining[i] + '_', next_remaining, relation_type, question_types)

# def generate_combination(current, remaining, relation_type, question_types):
#     # 判断特殊情况
#     if not remaining:
#         return []
#
#     # 定义结果集
#     result = set()
#
#     def permutation(selected, selectable):
#         # 如果没有剩余元素，则添加到结果集中
#         if not selectable:
#             result.add('_'.join(selected) + '_' + relation_type)
#             return
#
#         # 遍历每个阶段的可选解集合
#         for i in range(len(selectable)):
#             cur = selectable[i]
#
#             # 选择此阶段其中一个解，将其加入到已选解集合中
#             selected.append(cur)
#
#             # 选完之后再进入下一个阶段
#             next_selectable = selectable[:i] + selectable[i + 1:]
#             permutation(selected, next_selectable)
#
#             # [回溯]换个解再遍历
#             selected.pop()
#
#         # 处理不包含当前元素的组合
#         permutation(selected, selectable[1:])
#
#     # 初始化调用
#     permutation([], remaining)
#
#     # 包含仅有relation_type的组合
#     result.add(relation_type)
#
#     return result



if __name__ == "__main__":
    question = '郑辛茹购买最多的商品类别是什么？'
    print(classify(question))
