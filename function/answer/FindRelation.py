

class findrelation_base_keywords:
    """
    基于规则的关键字匹配
    """
    def __init__(self):
        # 问句疑问词
        self.manager=['经理', '是谁', '基金经理']
        self.index=['哪个指数', '所属指数', '指数是哪个']
        self.scale=['资产规模', '资产', '规模']
        self.fund=['基金有哪些', '管理的基金', '哪些基金']
        self.company=['什么公司','哪些公司','公司有哪些','哪个公司','什么企业','哪些企业','企业有哪些','哪个企业', '基金公司', '公司是什么']
        self.manager_qwds = ['高管', '经理']
        self.scale_qwds = ['资产规模', '资产']
        self.index_qwds = ['所属指数', '指数是什么']
        self.performance_qwds = ['好不好', '好吗', '牛逼', '牛', '厉害', '蓝筹', '牛股', '怎样', '如何', '好么', '牛不', '屌', '评价', '评估', '表现']
        self.wd_dict = dict()

        for wd in self.manager:self.wd_dict[wd]='UNmanager'
        for wd in self.index:self.wd_dict[wd]='UNindex'
        for wd in self.scale:self.wd_dict[wd]='UNscale'
        for wd in self.fund:self.wd_dict[wd]='UNfund'
        for wd in self.company:self.wd_dict[wd]='UNcompany'
        for wd in self.manager_qwds: self.wd_dict[wd] = 'UNmanager'
        for wd in self.performance_qwds: self.wd_dict[wd] = 'UNperformance'
        for wd in self.scale_qwds:self.wd_dict[wd] = 'UNscale'
        for wd in self.index_qwds:self.wd_dict[wd] = 'UNindex'

    def main(self,sentence):
        relationtype=set()
        for wd in self.wd_dict.keys():
            if wd in sentence:
                relationtype.add(self.wd_dict[wd])
        return list(relationtype)

if __name__ == "__main__":
    finder = findrelation_base_keywords()
    question = '华安上证180ETF所属基金公司是哪个'
    r = finder.main(question)
    print(r)