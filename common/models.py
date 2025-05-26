from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
class UploadedFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    assigned_name = 
models.CharField(max_length=255, blank=false)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    