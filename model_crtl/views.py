from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, 'model_crtl/model_control_index.html')


def query_view(request):
    return render(request, 'model_crtl/model_control_bll.html')


re_data = {'filesArr': ['chatgpt', 'chatgpt2', 'chatgpt3', 'chatgpt4', 'chatgpt5',
            'chatgpt6'],'choose':'chatgpt4'
           }
def query_main(request):
    if request.method == "GET":
        if int(request.GET.get("file_mode")) == 1:
            re_d = {'filesArr': re_data['filesArr'][:5], 'choose':re_data['choose']}
            return JsonResponse(re_d)
        elif int(request.GET.get("file_mode")) == 2:
            try:
                file_page = int(request.GET.get("file_page"))
                re_d = {'code':1, 'filesArr': re_data['filesArr'][(file_page - 1) * 5:file_page * 5], 'choose': re_data['choose']}
                print(re_data['filesArr'][(file_page-1)*5])
            except IndexError:
                re_d = {'code': 0}
            return JsonResponse(re_d)
        return JsonResponse({'code': 0})

def query_switch(request):
    if request.method == "GET":
        re_data['choose'] = request.GET.get("switchAi")
        re_d = {'code': 1, 'text': re_data['choose']}
        return JsonResponse(re_d)
    return JsonResponse({'code': 0})