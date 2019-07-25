from django.shortcuts import render
from django.http import HttpResponse

from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.

'''
function view
'''
# def post_list(request,category_id=None,tag_id=None):
#     tag = None
#     category = None
#     if tag_id:
#         post_list,tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list,category = Post.get_by_category(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category':category, #具体的分类值 get_navs()返回的值中categories是类别对象
#         'tag':tag,
#         'post_list':post_list,
#         'sidebars':SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#
#     return render(request,'blog/list.html',context=context)
#
#
# def post_detail(request,post_id):
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#
#     return render(request,'blog/detail.html',context=context)

'''
class-based view
'''

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Post, Tag, Category
from config.models import SideBar


class IndexView(ListView):
    '''
    首页视图
    '''
    # model = Post
    queryset = Post.latest_posts()
    paginate_by = 3
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class SearchView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(
            {'keyword': self.request.GET.get('keyword', '')}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class CategoryView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context.update(
            {'category': category}
        )
        return context

    def get_queryset(self):
        '''
        重写queryset:根据分类过滤
        '''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(id=category_id)


class TagView(IndexView):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, id=tag_id)
        context.update(
            {'tag': tag}
        )
        return context

    def get_queryset(self):
        '''
        重写queryset:根据标签过滤
        '''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(id=tag_id)


class CommonView:
    '''
    通用视图：导航、侧边栏
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'sidebars': SideBar.get_all()
            }
        )
        context.update(
            Category.get_navs()  # return dict
        )

        return context


class PostDetailView(CommonView, DetailView):
    '''
    文章详情页
    '''
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
