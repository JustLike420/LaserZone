from django.shortcuts import render
from .models import Post

# Create your views here.
from django.views.generic import ListView


def index(request):
    return render(request, 'index.html')


def benefits(request):
    return render(request, 'benefits.html')


# def news(request):
#     return render(request, 'news.html')


class News(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 6
   # def get_context_data(self, object_list=None, **kwargs):
   #     context = super().get_context_data(**kwargs)
   #     context[]