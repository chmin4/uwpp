from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    assigned_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.assigned_name:
            raise ValueError("이름을 지정해주세요")
        super().save(*args, **kwargs)


