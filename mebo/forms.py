from django import forms
from mebo.models import Memo, InMemo
#form: page 요청 시 전달되는 parameter를 쉽게 관리하기 위한 class
#필수 파라미터 존재 확인, 형식 확인/검증, html 자동생성, 데이터 저장 by 연결된 model
class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['subject','content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class InMemoForm(forms.ModelForm):
    class Meta:
        model = InMemo
        fields = ['content']
        labels = {
            'content':'작은Memo',
        }
