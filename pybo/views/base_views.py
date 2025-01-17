from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question, Answer,Comment
from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count


# Create your views here.
def index(request):
    '''
    Pybo 목록 출력 
    '''
    
    #입력인자
    page = request.GET.get('page', '1')  #페이지
    kw = request.GET.get('kw','')        #검색어
    so = request.GET.get('so', 'recent') #정렬기준
    
    #정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')
    
    #조회
    #question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
        
    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    
    context =  {'question_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)