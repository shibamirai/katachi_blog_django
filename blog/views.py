from django.views import generic
from .models import Post


class PostListView(generic.ListView):
    template_name = 'blog/posts/index.html'
    paginate_by = 10

    def get_queryset(self):
        self.queryset = Post.objects.select_related('category').order_by('-posted_at')
        return super().get_queryset()


class PostDetailView(generic.DetailView):
    template_name = 'blog/posts/detail.html'
    queryset = Post.objects.select_related('category').select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(category_id=self.object.category_id).order_by('-posted_at')[:5]
        return context
