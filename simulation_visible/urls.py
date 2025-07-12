from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index_view),
    path('query/', views.query_view),
]