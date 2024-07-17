entity_path = 'C:\\Users\\86176\\Desktop\\公司课题暂用\\qa\\function\\answer\\entity.txt'
segment_word_path = 'C:\\Users\\86176\\Desktop\\公司课题暂用\\qa\\function\\answer\\segment_word.txt'

# questionTypes = ['name_UNhobby', 'name_UNhomemate', 'name_UNhometown', 'name_UNlive', 'live_UNperson']
# headTag = ['name', 'name', 'name', 'name', 'live']
# tailTag = ['hobby', 'homemate', 'hometown', 'live', 'person']
# answerTemplates = ['的爱好是：', '的室友是：', '的家乡是：', '住在：', '住的人数有：']

questionTypes = ['用户_most_type', '用户_商品类别_recommend', 'NONE_parent', '用户_parent', '亲属_recommend']
answerTemplates = ['{}购买最多的商品类别为{}']

# 疑问词，每个对象是一个问题的标签以及关键字列表
question_words = [
    {
        "label": "most_type",
        "keywords": ['最多', '商品类别', '商品类型']
    },
    {
        "label": "UNplace",
        "keywords": ['哪里']
    },
    {
        "label": "recommend",
        "keywords": ['适合', '推荐']
    },
    {
        "label": "parent",
        "keywords": ['疑似亲属', '亲属']
        # 有什么客户与疑似亲属有过相关的流水记录？
        # 1、xxx客户的疑似亲属相关信息？
        # 2、适合给这些客户推荐什么业务？
    },
]

# neo4j相关信息
neo4j_address = "http://localhost:7474/"
neo4j_username = "neo4j"
neo4j_password = "hjh123123"
questionType = ['payer_UNtype', 'payer_UNplace', 'payer_UNrecommend', 'payer_UNCommon']

headTag = ['payer', 'payer', 'payer']
tailTag = ['type', 'place', 'recommend']

answerTemple = ['的购买最多的商品类别是：', '最常使用的消费方式是：', '的家乡是：', '住在：', '住的人数有：']

# 上一个问题的实体列表，可作为下一个问题的参数
pre_entity_types = dict()