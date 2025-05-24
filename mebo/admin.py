from django.contrib import admin
from .models import Memo

class MemoAdmin(admin.ModelAdmin):
    search_fields = ['subject']

admin.site.register(Memo, MemoAdmin)

# Register your models here.
