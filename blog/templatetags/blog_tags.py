from ..models import Post, Category
from django import template

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    # 获取数据库中前 num 篇文章. 默认 num 为5.
    return Post.objects.all()[:num]
    # return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    # 实现按月归档
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag
def get_categories():
    return Category.objects.all()