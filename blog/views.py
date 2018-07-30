# blog/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category
import markdown
from comments.forms import CommentForm
# 引入 ListView 视图
from django.views.generic import ListView, DetailView

# 在类视图方法下，基于列表视图(ListView)的有： index, archives, category.

# 1): 改视图函数 index 为类视图函数 IndexView
# 首先要继承Django中的一个类，因为 IndexView 需要获得列表数据，所以继承 ListView
class IndexView(ListView):
    #  以下属性用来指定视图函数要做事情：
    model = Post  # 将 model 指定为 Post（即要获取的模型是 Post）
    template_name = 'blog/index.html'  # 指定渲染的模板
    context_object_name = 'post_list'  # 传递给模板的变量名

# 以下是 index 函数视图：
# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html', context={'post_list': post_list})

""" 归档 """
# 2): 改函数视图 archives 为类视图函数
class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )

# 以下是 archives 的函数视图
# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month
#                                     )
#                                     # ).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

""" 分类 """
# 3): 改函数视图 category 为类视图函数
class CategoryView(IndexView):
    """
    属性设置与 IndexView 是一样的，所以可以直接继承 IndexView，从而省略下面三行：
    model = Post  # 获取 Post 模型
    template_name = 'blog/index.html'  # 渲染的模板
    context_object_name = 'post_list'  # 变量名
    """
    # 先获取分类的ID值(cate)，然后用父类的 get_queryset 获得全部文章列表然后 filter 筛选：
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

# 以下是 category 的函数视图
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# 类视图方法从数据库获得一条记录数据：用 DetailView 类视图

""" 博客全文、评论 """
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        #
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        #
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list':comment_list
        })
        return context


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 阅读量 +1 (执行一次就加一次)
#     post.increase_views()
#
#     post.body = markdown.markdown(post.body,
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                       'markdown.extensions.toc',
#                                   ])
#     form = CommentForm()
#     # 获取这篇 post 下的全部评论据
#     comment_list = post.comment_set.all()
#
#     # 将 文章、表单、以及文章下的评论列表
#     # 作为模板变量传给 detail.html 模板，以便渲染相应数据。
#     context = {'post': post,
#                'form': form,
#                'comment_list': comment_list
#                }
#     return render(request, 'blog/detail.html', context=context)