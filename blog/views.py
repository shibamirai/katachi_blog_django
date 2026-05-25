from django.db.models import Q
from django.views import generic
from .models import Post


class PostListView(generic.ListView):
    template_name = 'blog/posts/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__contains=search) | Q(body__contains=search)
            )
        return queryset.select_related('category').order_by('-posted_at')


class PostDetailView(generic.DetailView):
    template_name = 'blog/posts/detail.html'
    queryset = Post.objects.select_related('category').select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(category_id=self.object.category_id).order_by('-posted_at')[:5]
        return context
