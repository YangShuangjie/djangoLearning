from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.BaseModelAdmin import BaseModelAdmin

import xadmin
from xadmin.layout import Row,Fieldset,Container



# Register your models here.
"""
------------------------------------------------------------------
    admin 原生模型关联
------------------------------------------------------------------
class PostInline(admin.TabularInline):  # admin.StackedInline
    model = Post  # 关联哪个模型
    fields = ('title', 'desc')
    extra = 1
"""
"""
------------------------------------------------------------------
xadmin 模型关联
------------------------------------------------------------------
"""
class PostInline:
    model = Post
    form_layout = (
        Container(Row('title','desc'))
    ) #变动部分
    extra = 1

'''
#　等同于admin.site.register(Category, CategoryAdmin)
#  custom_site.register(Category,CategoryAdmin)
@admin.register(Category,site=custom_site)
'''
@xadmin.sites.register(Category)
class CategoryAdmin(BaseModelAdmin):
    list_display = (
        'owner', 'name', 'status',
        'is_nav', 'created_time', 'post_count'
    )
    fields = ('owner', 'name', 'status', 'is_nav')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    inlines = [PostInline]


# @admin.register(Tag,site=custom_site)
@xadmin.sites.register(Tag)
class TagAdmin(BaseModelAdmin):
    list_display = ('owner', 'name', 'status', 'created_time')
    fields = ('owner', 'name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)

"""
 ------------------------------------------------------------------
    django 原生后台日志配置[xadmin 自带更能较好的log功能]
 ------------------------------------------------------------------
@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'object_repr',
        'object_id',
        'user',
        'action_flag',
        'change_message'
    )
"""


"""
-------------------------------------------------------------------
 django 原生自定义筛选器
-------------------------------------------------------------------
class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义Category过滤器'''
    title = 'Category'
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset
"""


"""
-------------------------------------------------------------------
xadmin 自定义筛选器
-------------------------------------------------------------------
"""
from xadmin.filters import  manager
from xadmin.filters import RelatedFieldListFilter


class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category' #定义过滤字段

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id','name') # lookup_choices默认情况下查询所有数据

manager.register(CategoryOwnerFilter, take_priority=True) #过滤器在管理器中注册并设置优先权

# @admin.register(Post, site=custom_site)
@xadmin.sites.register(Post)
class PostAdmin(BaseModelAdmin):
    form = PostAdminForm
    # exclude = ('owner',) #限定不展示的字段
    list_display = (
        'owner',
        'title', 'category', 'status',
        'created_time', 'operator')  # 展示字段
    list_display_links = []  # 字段链接
    list_filter = ['category']  # 页面过滤字段[xadmin 同此]
    # list_filter = [CategoryOwnerFilter] #admin自定义filter
    # list_per_page = 1
    search_fields = ['title', 'category__name']  # 搜索字段

    actions_on_top = True  # 置顶
    actions_on_bottom = True  # 置底
    # save_on_top = True #　保存、编辑等选项是否在顶部展示

    filter_horizontal = ('tag',) #水平向选择
    # filter_vertical =('tag',)　#　垂直向选择

    """
    ------------------------------------------------------------------
        django 原生admin的fields设置
    ------------------------------------------------------------------
    # fields = (
    #     'owner', 'title',  # 每个字段独自成行，(field1,field2)并排一行
    #     'category',
    #     'desc', 'status',
    #     'content', 'tag'
    # )  # 创建编辑页字段
    fieldsets = (
        ('基础配置', {
            'description': "填写作者、分类、标题",
            'fields': ('owner',
                       'category',
                       'title',
                       'status'),
        }),
        ('内容', {
            'fields': ('desc', 'content'),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',)
        })
    )
    """

    '''
    ------------------------------------------------------------------
    xadmin fields　设置
    ------------------------------------------------------------------
    '''
    form_layout = (
        Fieldset('基础信息',
                 'owner',
                 Row('title','category'),
                 'status',
                 'tag'),
        Fieldset(
            '内容信息',
            'desc',
            'content',
            'use_md',
            'content_md',
            'content_ck'
        )
    )

    """
    ------------------------------------------------------------------
    xadmin 不支持自定义site,因此custom_site不能用了
    ------------------------------------------------------------------
    """
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('cus_admin:blog_post_change', args=(obj.id,)) #原生admin自定义site
            # reverse('xadmin:blog_post_change', args=(obj.id,)) #xadmin
            self.model_admin_url('change',obj.id) #admin提供的方法
        )

    operator.short_description = '操作'

    """
    ------------------------------------------------------------------
        下面代码限定了文章post的创建者只能是系统登录者[抽象到了BaseModelAdmin]
    ------------------------------------------------------------------
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
    """


    """
    ------------------------------------------------------------------
    静态资源配置：自定义后端post管理的css和js
    ------------------------------------------------------------------
    class Media:
        css = {
            'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",)
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)
    """

    """
    ------------------------------------------------------------------
    xadmin 静态资源配置
    ------------------------------------------------------------------
    @property
    def media(self):
        media = super().media
        media.add_js(["https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js"])
        media.add_css({
            'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",)
        })
        return media
    """

