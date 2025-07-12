from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, 'simulation/simulation_index.html')


def query_view(request):
    return render(request, 'simulation/simulation_control_bll.html')
