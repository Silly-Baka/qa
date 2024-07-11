from function.answer.utils import question_words


class findrelation_base_keywords:
    """
    基于规则的关键字匹配
    """
    def __init__(self):
        # 问句疑问词
        self.wd_dict = dict()

        '''引入关键字'''
        for qw in question_words:
            for keyword in qw["keywords"]:
                self.wd_dict[keyword] = qw["label"]

    def main(self,sentence):
        relationtype=set()
        for wd in self.wd_dict.keys():
            if wd in sentence:
                relationtype.add(self.wd_dict[wd])
        return list(relationtype)

if __name__ == "__main__":
    finder = findrelation_base_keywords()
    question = '张三的爱好是什么？'
    r = finder.main(question)
    print(r)