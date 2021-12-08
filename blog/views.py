from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
import operator
from django.urls import reverse_lazy

from django.db.models import Q
from django.conf import settings
PAGINATE_COSTANT = settings.PAGINATE_COSTANT

def home(request):
    post = Post.objects.all()

    context = {
        'posts': post,
    }

    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter((Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query)) & Q(is_visible=True))
    paginate_by=PAGINATE_COSTANT
    context={ 'posts':result }
    return render(request,template,context)
   


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = PAGINATE_COSTANT


    def get_queryset(self):
        object_list = self.model.objects.filter(is_visible=True)
        return object_list


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = PAGINATE_COSTANT

    def get_queryset(self):
        logged_in_user = self.request.user
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user == logged_in_user:
            return Post.objects.filter(author=user).order_by('-date_posted')
        
        return Post.objects.filter(Q(author=user) & Q(is_visible=True)).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self):
        logged_in_user = self.request.user
        object = self.model.objects.get(pk=self.kwargs['pk'])

        if logged_in_user == object.author:
            return object
        if object.is_visible == False:
            raise Http404("Not Available")
        return object


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
