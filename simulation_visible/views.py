from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.


def index_view(request):
    return render(request, 'simulation_visible/simulation_visible_index.html')


def query_view(request):
    return render(request, 'simulation_visible/simulation_visible_control_bll.html')


def query_main(request):
    if request.method == "GET":
        if int(request.GET.get("file_mode")) == 1:
            re_d = {'filesArr': re_data['/']['filesArr'][:5]}
            return JsonResponse(re_d)
        elif int(request.GET.get("file_mode")) == 2:
            forward_path = request.GET.get("file_name")
            if forward_path + '/' in re_data:
                re_d = {'code': 1, 'filesArr': re_data[forward_path + '/']['filesArr'][:5],
                        'newLayer': forward_path + '/'}
                return JsonResponse(re_d)
            else:
                re_d = {'code': 2}
                return JsonResponse(re_d)
        elif int(request.GET.get("file_mode")) == 3:
            pre_path = '/' if len(request.GET.get("path_cur").rsplit('/', 2)) < 2 else \
            request.GET.get("path_cur").rsplit('/', 1)[0] + '/' \
                if request.GET.get("path_cur")[-1] != '/' else request.GET.get("path_cur").rsplit('/', 2)[0] + '/'
            re_d = {'pathInfo': pre_path, 'filesArr': re_data[pre_path]['filesArr'][:5]}
            return JsonResponse(re_d)
        elif int(request.GET.get("file_mode")) == 4:
            num_start = (int(request.GET.get("file_page")) - 1) * 5
            num_end = int(request.GET.get("file_page")) * 5
            file_path = request.GET.get("file_path")
            try:
                print(re_data[file_path]['filesArr'][num_start])
                re_d = {'code': 1, 'filesArr': re_data[file_path]['filesArr'][num_start:num_end]}
            except IndexError:
                re_d = {'code': 0}
            return JsonResponse(re_d)
        else:
            return 0
    else:
        return 0


re_data = {
    '/': {"filesArr": ["aaaa","bbbb","cccc", "aaaa","bbbb","cccc"]},
    '/bbbb/': {'filesArr': ['niaafdho', 'wosafdi', 'niaafdho', 'wosafdi', "aaaa", "cccc", "cccc", "cccc", "aaaa", 'safd']},
    '/bbbb/safd/': {'filesArr': ['naaho', 'woffhi']},
}


def gen_view(request):
    if request.method == "GET":
        if int(request.GET.get("file_mode")) == 1:
            re_d = {'code': 1, 'dataJson': {}}
        elif int(request.GET.get("file_mode")) == 2:
            pass
        elif int(request.GET.get("file_mode")) == 3:
            pass
        elif int(request.GET.get("file_mode")) == 4:
            pass
        elif int(request.GET.get("file_mode")) == 5:
            pass
        return JsonResponse(re_d)