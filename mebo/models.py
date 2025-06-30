from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Field는 속성을 의미
class Memo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)  #글자 수 제한을 위한 형식지정 char
    content = models.TextField()    #글자 수 제한이 없는 TextField
    create_date = models.DateTimeField()    #date & time을 저장하는 속성
    modify_date = models.DateTimeField(null=True, blank=True)


class InMemo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = models.ForeignKey(Memo, on_delete=models.CASCADE)    #Inmemo는 Memo에 종속적(cascade) --> ForeignKey를 통한 Memo(Master)를 속성으로 포함; 모델 간 관계 정의
                                                                #CASCADE: 종속을 뜻함, on_delete을 통해 Memo 삭제에 따른 Inmemo의 순장을 설정
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

#   def __str__(self):
#       return self.content
