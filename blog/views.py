# blog/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category
import markdown
from comments.forms import CommentForm

# Create your views here.
def index(request):
    # post_list = Post.objects.all().order_by('-created_time')
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})

""" 博客全文、评论 """
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    # 获取这篇 post 下的全部评论据
    comment_list = post.comment_set.all()

    # 将 文章、表单、以及文章下的评论列表
    # 作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)
    # return render(request, 'blog/detail.html', context={'post': post})

""" 归档 """
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
                                    # ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

""" 分类 """
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    # post_list = Post.objects.filter(category=cate).order_by('-created_time')
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})

