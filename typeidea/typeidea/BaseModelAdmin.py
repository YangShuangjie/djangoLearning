from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    '''
    def get_queryset:用来过滤queryset仅可见作者本人的数据
    def save_model:用来限定文章的创建者只能是作者本人
    '''
    # exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseModelAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseModelAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
