from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, 'model_crtl/model_control_index.html')


def query_view(request):
    return render(request, 'model_crtl/model_control_bll.html')
