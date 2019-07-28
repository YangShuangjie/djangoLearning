from rest_framework import serializers,pagination
from .models import Post,Category

'''
写法类似forms.ModelForm
'''

#　文章列表页接口
# class PostSerializer(serializers.ModelSerializer):
class PostSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField( # 外键需要它来配置
        read_only=True, #不可写
        slug_field='name' #需要展示的字段
    )
    tag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    # url = serializers.HyperlinkedIdentityField(view_name='api-post-detail')
    class Meta:
        model = Post
        fields = ['id','title','owner','category','tag','created_time']
        extra_kwargs = {
            'url':{'view_name':'api-post-detail'}
        }
# 文章详情页接口
class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ['id','title','owner','category','tag','desc','content_html','created_time']


# 分类接口
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','created_time']


class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self,obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        page = paginator.paginate_queryset(posts,self.context['request'])
        serializer = PostSerializer(page,many=True,context={'request':self.context['request']})
        return {
            'count':posts.count(),
            'results':serializer.data,
            'previous':paginator.get_previous_link(),
            'next':paginator.get_next_link(),
        }
    class Meta:
        model = Category
        fields = ('id','name','created_time','posts')