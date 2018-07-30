from django.conf.urls import url
from . import views

app_name = 'blog'

"""
    # 函数视图的URL配置
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<year>[0-9]+)/$', views.category, name='category'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
"""

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),  # as_view() 方法可以将类视图转化成函数视图
    url(r'^category/(?P<year>[0-9]+)/$', views.CategoryView.as_view, name='category'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view, name='archives'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
]
