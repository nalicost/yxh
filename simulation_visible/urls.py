from django.urls import path, re_path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index_view),
    path('query/', views.query_view),
    re_path('query_main', views.query_main),
    re_path('gen', views.gen_view),
]