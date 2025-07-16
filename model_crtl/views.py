from django.http import JsonResponse
from django.shortcuts import render
from core import llm_parameters_management as llm_par_mang
# Create your views here.


def index_view(request):
    return render(request, 'model_crtl/model_control_index.html')


def query_view(request):
    return render(request, 'model_crtl/model_control_bll.html')


def query_main(request):
    if request.method == "GET":
        re_data = [i.model for i in llm_par_mang.llm_li]
        if int(request.GET.get("file_mode")) == 1:
            re_d = {'filesArr': re_data[:5], 'choose': llm_par_mang.llm_choose.model}
            return JsonResponse(re_d)
        elif int(request.GET.get("file_mode")) == 2:
            try:
                file_page = int(request.GET.get("file_page"))
                re_d = {'code':1, 'filesArr': re_data[(file_page - 1) * 5:file_page * 5], 'choose': llm_par_mang.llm_choose.model}
                print(re_data[(file_page-1)*5])
            except IndexError:
                re_d = {'code': 0}
            return JsonResponse(re_d)
        return JsonResponse({'code': 0})

def query_switch(request):
    if request.method == "GET":
        select_llm = request.GET.get("switchAi")
        for item in llm_par_mang.llm_li:
            if select_llm == item.model:
                item.switch()
                break
        re_d = {'code': 1, 'text': llm_par_mang.llm_choose.model}
        return JsonResponse(re_d)
    return JsonResponse({'code': 0})