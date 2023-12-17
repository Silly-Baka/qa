from function.answer import FindEntity
from function.answer import FindRelation


def classify(question):
    relationfinder=FindRelation.findrelation_base_keywords()
    entityfinder = FindEntity.FindEntity_base_similarity()
    relation_type = relationfinder.main(question)  # str
    # print('relation_type:', relation_type)
    entity_type = entityfinder.main(question)
    # print('entity_type:', entity_type)

    if not entity_type:
        return {}
    # 收集问句当中所涉及到的实体类型
    question_types = []
    for i in relation_type:
        for type in entity_type.values():
            question_types.append(type+'_'+i)
    data = {}
    data['args'] = entity_type
    data['question_types'] = question_types
    return data #{'args': {'珠海科德电子有限公司': ['comapny']}, 'question_types': ['comapny_belong_concept']}


if __name__ == "__main__":
    question = '华安上证180ETF所属基金公司是哪个'
    print(classify(question))