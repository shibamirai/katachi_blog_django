from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from .forms import PostCreateForm
from .models import Post, Category


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

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(
                category_id=category_id
            )

        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(
                author_id=author_id 
            )

        return queryset.select_related('category').order_by('-posted_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = Category.objects.filter(id=self.request.GET.get('category')).first()
        return context


class MyPostListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = 'blog/posts/mylist.html'
    paginate_by = 10

    def test_func(self):
        """管理者しかアクセスできないようにする"""
        return self.request.user.is_admin

    def get_queryset(self):
        """ログインユーザが投稿したものだけ表示"""
        queryset = Post.objects.filter(
            author_id=self.request.user.id 
        )
        return queryset.select_related('category').order_by('-posted_at')


class PostDetailView(generic.DetailView):
    template_name = 'blog/posts/detail.html'
    queryset = Post.objects.select_related('category').select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(category_id=self.object.category_id).order_by('-posted_at')[:5]
        return context


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.CreateView):
    form_class = PostCreateForm
    template_name = 'blog/posts/create.html'
    success_url = reverse_lazy('home')
    success_message = '「%(title)s」を投稿しました'

    def test_func(self):
        """
        管理者しかアクセスできないようにする
        """
        return self.request.user.is_admin
    
    def form_valid(self, form):
        """
        モデルの保存前に、ログインユーザを投稿者としスラッグには投稿日時分を'202510271318'形式の文字列にしてセットする
        """
        form.instance.author = self.request.user
        form.instance.slug = datetime.now().strftime('%Y%m%d%H%M')
        return super().form_valid(form)
