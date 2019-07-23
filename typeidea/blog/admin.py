from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Category, Tag, Post
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site


# Register your models here.
class PostInline(admin.TabularInline):  # admin.StackedInline
    model = Post  # 关联哪个模型
    fields = ('title', 'desc')
    extra = 1

#　等同于admin.site.register(Category, CategoryAdmin)
#  custom_site.register(Category,CategoryAdmin)
@admin.register(Category,site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'owner', 'name', 'status',
        'is_nav', 'created_time', 'post_count'
    )
    fields = ('owner', 'name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    inlines = [PostInline]


@admin.register(Tag,site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'status', 'created_time')
    fields = ('owner', 'name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


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


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    # exclude = ('owner',) #限定不展示的字段
    list_display = (
        'owner',
        'title', 'category', 'status',
        'created_time', 'operator')  # 展示字段
    list_display_links = []  # 字段链接
    list_filter = ['category']  # 页面过滤字段
    # list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']  # 搜索字段

    actions_on_top = True  # 置顶
    actions_on_bottom = True  # 置底
    # save_on_top = True #　保存、编辑等选项是否在顶部展示

    filter_horizontal = ('tag',)
    # filter_vertical =('tag',)

    # fields = (
    #     'owner', 'title',  # 每个字段独自成行，(field1,field2)并排一行
    #     'category',
    #     'desc', 'status',
    #     'content', 'tag'
    # )  # 创建字段
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

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    # 下面代码限定了文章post的创建者只能是系统登录者
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    # # 自定义后端post管理的css和js
    # class Media:
    #     css = {
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",)
    #     }
    #     js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js",)

@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        'object_repr',
        'object_id',
        'user',
        'action_flag',
        'change_message'
    )
