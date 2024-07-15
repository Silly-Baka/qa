

class findrelation_base_keywords:
    """
    基于规则的关键字匹配
    """
    def __init__(self):
        # 问句疑问词
        self.type=['类别']
        self.place=['哪里']
        self.recommend=['推荐']
        self.wd_dict = dict()

        for wd in self.type:self.wd_dict[wd]='UNtype'
        for wd in self.place:self.wd_dict[wd]='UNplace'
        for wd in self.recommend:self.wd_dict[wd]='UNrecommend'

        print(self.wd_dict)

    def main(self,sentence):
        relationtype=set()
        # 遍历关键字规则库中的每个key
        for wd in self.wd_dict.keys():
            # 如果关键字规则库中的key包含在句子中
            if wd in sentence:
                # 则将该key所对应的问题的类型加入进relationtype这个set中
                # set可以去除重复，所以relationtype中不会有重复元素
                relationtype.add(self.wd_dict[wd])
        return list(relationtype)

if __name__ == "__main__":
    finder = findrelation_base_keywords()
    question = '张三的爱好是什么？'
    r = finder.main(question)
    print(r)