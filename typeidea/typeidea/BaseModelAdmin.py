from django.contrib import admin


# class BaseModelAdmin(admin.ModelAdmin):
class BaseModelAdmin(object): # xadmin继承对象为object或无继承
    '''
    def get_queryset:用来过滤queryset仅可见作者本人的数据
    def save_model:用来限定文章的创建者只能是作者本人
    '''
    # exclude = ('owner',)
    """
    ---------------------------------------------------
                        admin
    ---------------------------------------------------    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseModelAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseModelAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
    """
    """
    ---------------------------------------------------
                        xadmin
    ---------------------------------------------------
    """
    def save_models(self):
        self.new_obj.owner = self.request.user
        return super().save_models()
    def get_list_queryset(self):
        request = self.request
        qs = super().get_list_queryset()
        return qs.filter(owner=request.user)