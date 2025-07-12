from django.shortcuts import render

from django.http import JsonResponse

# Create your views here.


def index_view(request):
    return render(request, 'param_crtl/param_control_index.html')


def query_view(request):
    return render(request, 'param_crtl/param_control_bll.html')

re_data = {"filesArr": ["hhhh","sssss","dddddd"]}
def query_main_back_info(request):
    if request.method == "GET":
        if int(request.GET.get("file_all")) == 1:
            return JsonResponse(re_data)
        else:
            del_file=request.GET.get("file_name").split("/")[1]
            re_data["filesArr"].remove(del_file)
            re_d={"code":1,"filesArr":re_data["filesArr"]}
            return JsonResponse(re_d)
