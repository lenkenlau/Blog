# comments/forms.py

from django import forms
from .models import Comment

""" 用户评论表单类 """
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # 表明这个表单对应的数据库模型是 Comment 类
        fields = ['name', 'email', 'url', 'text']  # 指定表单需要显示的字段；