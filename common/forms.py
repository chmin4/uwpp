from django import forms
from .models import UploadedFile

class UploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['assigned_name', 'file']
        label = {
            'assigned_name':"파일 이름"
        }