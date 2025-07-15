from django.shortcuts import render
from django.http import JsonResponse
from time import sleep
# Create your views here.


def index_view(request):
    return render(request, 'simulation/simulation_index.html')


def query_view(request):
    return render(request, 'simulation/simulation_control_bll.html')


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
    '/': {"filesArr": ["hhhh", "sssss", "dddddd", "hhhh", "sssss", "dddddd", 'niaho', 'woshi', 'shei']},
    '/hhhh/': {
        'filesArr': ['niaho', 'woshi', 'shei', 'niaho', 'woshi', 'shei', 'niaho', 'woshi', 'shei', 'niaho', 'woshi',
                     'shei']},
    '/hhhh/shei/': {'filesArr': ['niaho', 'woshi']},
}


def gen_statu_view(request):
    if request.method == "GET":
        if int(request.GET.get("statu_code")) == 1:
            file_path = request.GET.get("file_path")
            file_name = request.GET.get("file_name")
            if file_path + file_name + '/' in re_data:
                return JsonResponse({'code': 0})
            else:
                re_d = {'code': 1,
                        'height': -40,
                        'fileName': file_name,
                        'filePath': file_path,
                        'con': '正在输入参数中<span class="point"></span><span class="point"></span><span class="point"></span>'}
                return JsonResponse(re_d)
        elif int(request.GET.get("statu_code")) == 2:
            sleep(10)
            re_d = {'code': 2,
                    'height': -100,
                    'con': '正在生成交通状态图中<span class="point"></span><span class="point"></span><span class="point"></span>'}
            return JsonResponse(re_d)
        elif int(request.GET.get("statu_code")) == 3:
            sleep(20)
            re_d = {'code': 2,
                    'height': -130,
                    'con': '正在生成决策分析中<span class="point"></span><span class="point"></span><span class="point"></span>'}
            return JsonResponse(re_d)
        return JsonResponse({'code': 0})

def gen_view(request):
    if request.method == "GET":
        file_path = request.GET.get("file_path")
        file_name = request.GET.get("file_name")
        print(file_path, file_name)
        re_d = {'code': 3,
                'height': -260,
                'con': '生成完成'}
        sleep(30)
        return JsonResponse(re_d)