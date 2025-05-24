from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Memo, InMemo
from .forms import MemoForm, InMemoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import markdown

#CRUD_start
#READ
@login_required(login_url='common:login')
def index(request):
   page = request.GET.get('page','1')
   kw = request.GET.get('kw','')
   broad_list = Memo.objects.filter(author__is_superuser=True).order_by('-create_date')
   if request.user.is_superuser:
      memo_list = Memo.objects.exclude(author__is_superuser=True).order_by('-create_date')
      if kw:
         broad_list = None #공지는 검색 결과에서 빠짐
         memo_list=memo_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(inmemo__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(inmemo__author__username__icontains=kw)  
         ).distinct()
   else:
      memo_list = Memo.objects.filter(author=request.user).order_by('-create_date')
      if kw:
         broad_list = None #공지는 검색 결과에서 빠짐
         memo_list=memo_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(inmemo__content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(inmemo__author__username__icontains=kw)  
         ).distinct()

   paginator = Paginator(memo_list,15)
   page_obj = paginator.get_page(page)
   context = {'broad_list':broad_list, 'memo_list': page_obj, 'page':page, 'kw':kw}
   return render(request, 'mebo/memo_list.html',context)

def detail(request, memo_id):
   memo = get_object_or_404(Memo, pk=memo_id)
   if request.user != memo.author and not request.user.is_superuser:
      if memo.author.is_superuser:
         memo = Memo.objects.get(id=memo_id)
         html_content = markdown.markdown(memo.content)
         context = {'memo':memo, 'html_content':html_content }
         return render(request, 'mebo/memo_detail.html',context)
      else:
#        messages.error(request, "접근 권한 없음")
         return redirect('mebo:index')
   else:
      memo = Memo.objects.get(id=memo_id)
      context = {'memo':memo}
      return render(request, 'mebo/memo_detail.html',context)

#CREATE
def inmemo_create(request, memo_id):
   memo = get_object_or_404(Memo, pk=memo_id)
   if request.method == "POST":
      form = InMemoForm(request.POST)
      if form.is_valid():
         inmemo = form.save(commit=False)
         inmemo.author = request.user
         inmemo.create_date = timezone.now()
         inmemo.memo = memo
         inmemo.save()
         return redirect('{}#inmemo_{}'.format(resolve_url('mebo:detail',memo_id=memo.id), inmemo.id))   #inmemo 생성 후 redirect 페이지 이동 함수로 기존 페이지 다시 띄움
   else:
      return HttpResponseNotAllowed('문제가 발생했습니다')
   context = {'memo':memo, 'form':form}
   return render(request, 'mebo/memo_detail.html', context)

#board형 기능에서 가장 중요한 view 함수
@login_required(login_url='common:login')
def memo_create(request):#1.list에서 작성 버튼을 누르면 GET으로 request됨
   if request.method=='POST':#3.Memo작성 버튼을 누르면 template이 POST로 request됨에 따라 하단의 if block 실행(저장)
      form = MemoForm(request.POST)#4.인수 request.POST의 subject와 content값이 MemoForm의 subject와 content 속성에 매핑됨(객체 생성)
      #if form.is_valid():
      if form.is_valid():#5.form 유효성 검사; subject와 content 값의 유효성에 따라 memo의 생성 여부 결정
         memo = form.save(commit=False)#6.form의 임시저장(commit=False); MemoForm에 create_date가 정의되어있지 않아 이 지점에서 DB로 저장을 하지 않는다
         memo.create_date = timezone.now()#7.생성 시점에서의 create_date를 timezone.now()함수로 지정해줌
         memo.author = request.user
         memo.save()#8.최종적으로 저장
         return redirect('mebo:index')
   else:#2.작성 화면 렌더링
      form = MemoForm()
   context = {'form':form}
   return render(request, 'mebo/memo_form.html',context)#2의 영역(실질적으로 작성 화면을 띄우는 지점)

#DELETE
@login_required(login_url='common:login')
def memo_delete(request, memo_id):
   memo = get_object_or_404(Memo,pk=memo_id)
   if request.user != memo.author and not request.user.is_superuser:
      messages.error(request, "삭제 권한 없음")
      return redirect('mebo:detail',memo_id=memo.id)
   memo.delete()
   return redirect('mebo:index')

@login_required(login_url='common:login')
def inmemo_delete(request, inmemo_id):
   inmemo = get_object_or_404(InMemo,pk=inmemo_id)
   if request.user != inmemo.author and not request.user.is_superuser:
      messages.error(request, "삭제 권한 없음")
      return redirect('mebo:detail',memo_id=inmemo.memo.id)
   else:
      inmemo.delete()
   return redirect('mebo:detail',memo_id = inmemo.memo.id)

#MODIFY

def memo_modify(request,memo_id):
   memo = get_object_or_404(Memo,pk=memo_id)
   if request.user != memo.author and not request.user.is_superuser:
      messages.error(request, '수정 권한 없음')
      return redirect('mebo:detail',memo_id=memo.id)
   if request.method == "POST":
      form = MemoForm(request.POST, instance=memo)
      if form.is_valid():
         memo = form.save(commit=False)
         memo.author = request.user
         memo.modify_date = timezone.now()
         memo.save()
         return redirect('mebo:detail', memo_id=memo.id)
   else: 
      form = MemoForm(instance=memo)
   context = {'form':form}
   return render(request, 'mebo/memo_form.html', context)

@login_required(login_url='common:login')
def inmemo_modify(request,inmemo_id):
   inmemo = get_object_or_404(InMemo,pk=inmemo_id)
   if request.user != inmemo.author and not request.user.is_superuser:
      messages.error(request, '수정 권한 없음')
      return redirect('mebo:detail',memo_id=inmemo.memo.id)
   if request.method == "POST":
      form = InMemoForm(request.POST, instance=inmemo)
      if form.is_valid():
         inmemo = form.save(commit=False)
         inmemo.modify_date = timezone.now()
         inmemo.save()
         return redirect('{}#inmemo_{}'.format(resolve_url('mebo:detail',memo_id=inmemo.memo.id), inmemo.id))
   else: 
      form = InMemoForm(instance=inmemo)
   context = {'inmemo':inmemo, 'form':form}
   return render(request, 'mebo/inmemo_form.html', context)
#CRUD_end

#File_Uploadings


