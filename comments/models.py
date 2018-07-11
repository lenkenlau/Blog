# comments/models.py

from django.db import models
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()  # 用户发表的评论；
    created_time = models.DateTimeField(auto_now_add=True)  # 保存到数据库到时候自动添加时间；

    post = models.ForeignKey('blog.Post')  # 关联到某一篇文章；

    def __str__(self):
        return self.text[:20]

# Create your models here.
