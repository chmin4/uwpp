import markdown2
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def mark(value):
    return mark_safe(markdown2.markdown(value, extras=[
        "fenced-code-blocks", 
        "tables",           
        "break-on-newline",  
        "strike",        
        "task_list",         
        "cuddled-lists",   
        "footnotes",         
        "header-ids",        
    ]))
