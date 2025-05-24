from django.shortcuts import redirect
from django.contrib import messages

def my_lockout_handler(request, credentials):
    messages.error(request,"5회 로그인 오류. 일정 시간 동안 로그인이 차단됩니다.")
    return redirect('common:login')