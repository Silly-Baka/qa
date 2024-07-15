entity_path = 'C:\\Users\\86176\\Desktop\\公司课题暂用\\qa\\function\\answer\\entity.txt'
segment_word_path = 'C:\\Users\\86176\\Desktop\\公司课题暂用\\qa\\function\\answer\\segment_word.txt'

# questionTypes = ['name_UNhobby', 'name_UNhomemate', 'name_UNhometown', 'name_UNlive', 'live_UNperson']
# headTag = ['name', 'name', 'name', 'name', 'live']
# tailTag = ['hobby', 'homemate', 'hometown', 'live', 'person']
# answerTemplates = ['的爱好是：', '的室友是：', '的家乡是：', '住在：', '住的人数有：']


questionTypes = ['付款方_商品类别_most_type']
answerTemplates = ['{}购买最多的商品类型为{}']

# 疑问词，每个对象是一个问题的标签以及关键字列表
question_words = [
    {
        "label": "most_type",
        "keywords": ['最多', '购买', '商品类型']
    },
]

# neo4j相关信息
neo4j_address = "http://localhost:7474/"
neo4j_username = "neo4j"
neo4j_password = "hjh123123"