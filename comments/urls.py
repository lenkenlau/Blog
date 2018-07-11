# comments/urls.py

from django.conf.urls import url

from . import views

app_name = 'comments'  # 命名空间
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]