from django.views import generic
from .models import Post


class PostListView(generic.ListView):
    template_name = 'blog/posts/index.html'
    paginate_by = 10

    def get_queryset(self):
        self.queryset = Post.objects.select_related('category').order_by('-posted_at')
        return super().get_queryset()
