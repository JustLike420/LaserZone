from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('benefits', benefits, name='benefits'),
    path('news', News.as_view(), name='news'),
    # path('benefits/', register, name='benefits'),
    # path('news/', user_login, name='login'),
]