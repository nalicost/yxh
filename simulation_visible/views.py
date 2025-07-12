from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, 'simulation_visible/simulation_visible_index.html')


def query_view(request):
    return render(request, 'simulation_visible/simulation_visible_control_bll.html')
