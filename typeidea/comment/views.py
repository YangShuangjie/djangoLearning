from django.shortcuts import redirect
from django.views.generic import TemplateView
from .forms import CommentForm

# Create your views here.
class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'
    def post(self,requset,*args,**kwargs):
        """
        接收数据、验证、并保存
        """
        comment_form = CommentForm(requset.POST)
        target = requset.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed=False
        context = {
            'succeed':succeed,
            'form':comment_form,
            'target':target,
        }
        return self.render_to_response(context)
