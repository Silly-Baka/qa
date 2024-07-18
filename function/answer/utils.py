entity_path = 'C:\\Users\\Supre_yuan\\Desktop\\qa\\function\\answer\\entity.txt'
segment_word_path = 'C:\\Users\\Supre_yuan\\Desktop\\qa\\function\\answer\\segment_word.txt'

# questionTypes = ['name_UNhobby', 'name_UNhomemate', 'name_UNhometown', 'name_UNlive', 'live_UNperson']
# headTag = ['name', 'name', 'name', 'name', 'live']
# tailTag = ['hobby', 'homemate', 'hometown', 'live', 'person']
# answerTemplates = ['的爱好是：', '的室友是：', '的家乡是：', '住在：', '住的人数有：']

questionTypes = ['付款方_most_type', '付款方_recommend', '交易金额_analysis', "金额区间_potential"]
answerTemplates = ['{}购买最多的商品类别为{}']

# 疑问词，每个对象是一个问题的标签以及关键字列表
question_words = [
    {
        "label": "most_type",
        "keywords": ['最多', '购买', '商品类别']
    },
    # {
    #     "label": "UNtype",
    #     "keywords": ['类别']
    # },
    {
        "label": "UNplace",
        "keywords": ['哪里']
    },
    # {
    #     "label": "UNrecommend",
    #     "keywords": ['推荐']
    # },
    {
        "label": "recommend",
        "keywords": ['适合', '推荐']
    },
    {
        "label": "analysis",
        "keywords": ["理财交易金额"]
    },
    {
        "label": "potential",
        "keywords": ["潜力"]
    }
]

# neo4j相关信息
neo4j_address = "http://localhost:7474/"
neo4j_username = "neo4j"
neo4j_password = "Zty686240722"
questionType = ['payer_UNtype', 'payer_UNplace', 'payer_UNrecommend', 'payer_UNCommon']

headTag = ['payer', 'payer', 'payer']
tailTag = ['type', 'place', 'recommend']

answerTemple = ['的购买最多的商品类别是：', '最常使用的消费方式是：', '的家乡是：', '住在：', '住的人数有：']

# 上一个问题的实体列表，可作为下一个问题的参数
pre_entity_types = dict()