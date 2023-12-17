from django.shortcuts import render
from function.answer import question_classifier,generate_sqls,answer_search
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def answer(request):    #问答系统
    context = {}
    return render(request,'answer.html',context)

def find_answer(request):   #使用知识图谱实现问答
    # question = '大成基金管理有限公司的基金有哪些'
    question = request.GET.get('question','').strip()
    searcher = answer_search.answerearcher()
    # try:
    ans = searcher.main(generate_sqls.generate_sql(question_classifier.classify(question)))
        # print(ans)
    # except:
    #     ans = '输入问题有误'
    data = {}
    data['question'] = question
    data['answer'] = ans
    return JsonResponse(data)