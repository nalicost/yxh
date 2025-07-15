from django.shortcuts import render

from django.http import JsonResponse

# Create your views here.


def index_view(request):
    return render(request, 'param_crtl/param_control_index.html')


def query_view(request):
    return render(request, 'param_crtl/param_control_bll.html')


def query_main_back_info(request):
    if request.method == "GET":
        if int(request.GET.get("file_mode")) == 1:
            re_d = {'filesArr': re_data['/']['filesArr'][:5]}
            return JsonResponse(re_d)
        elif int(request.GET.get("file_mode")) == 2:
            forward_path = request.GET.get("file_name")
            if forward_path + '/' in re_data:
                re_d = {'code': 1, 'filesArr': re_data[forward_path + '/']['filesArr'][:5], 'newLayer': forward_path + '/'}
                return JsonResponse(re_d)
            else:
                re_d = {'code': 2, 'fileCon': file_content[forward_path], 'newLayer': forward_path}
                return JsonResponse(re_d)
        elif int(request.GET.get("file_mode")) == 3:
            pre_path = '/' if len(request.GET.get("path_cur").rsplit('/', 2)) < 2 else request.GET.get("path_cur").rsplit('/', 1)[0] + '/' \
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
    '/': {"filesArr": ["hhhh","sssss","dddddd", "hhhh","sssss","dddddd", 'niaho', 'woshi', 'shei']},
    '/hhhh/': {'filesArr': ['niaho', 'woshi', 'shei', 'niaho', 'woshi', 'shei', 'niaho', 'woshi', 'shei', 'niaho', 'woshi', 'shei']},
    '/hhhh/shei/': {'filesArr': ['niaho', 'woshi']},
}
file_content = {
    '/sssss': '这是一段内容',
    '/dddddd': '这是好几段内容',
    '/hhhh/niaho': '这是几段内容',
    '/hhhh/woshi': '这是一部分内容',
    '/hhhh/shei/niaho': '我看起来像内容',
    '/hhhh/shei/woshi': '这是所有内容',
}


def query_delete_back_info(request):
    if request.method == "GET":
        num = int(request.GET.get("file_page")) * 5
        del_path = request.GET.get("file_name").rsplit('/', 1)[0] + '/' if request.GET.get("file_name").rsplit('/', 1)[0] else '/'
        del_file = request.GET.get("file_name").rsplit("/", 1)[1]
        re_data[del_path]['filesArr'].remove(del_file)
        if del_path + del_file in file_content:
            del file_content[del_path + del_file]
        elif del_path + del_file + '/' in re_data:
            del re_data[del_path + del_file + '/']
        re_d = {"code": 1, "filesArr": re_data[del_path]["filesArr"][:num]}
        return JsonResponse(re_d)
    else:
        re_d = {"code": 0}
        return JsonResponse(re_d)

def upload_view(request):
    if request.method == "POST":
        if int(request.GET.get("add_mode")) == 1:
            dir_name = request.POST.get("dir_name")
            file_content_path = request.GET.get("file_path")
            re_d = {"code": 1}
            return JsonResponse(re_d)
        elif int(request.GET.get("add_mode")) == 2:
            file_content_upload = request.FILES.get('fileObj')
            file_content_path = request.GET.get("file_path")
            re_d = {"code": 2}
            return JsonResponse(re_d)
        elif int(request.GET.get("add_mode")) == 3:
            file_only_content_upload = request.FILES.get('fileObj')
            file_content_path = request.GET.get("file_path")
            re_d = {"code": 1}
            return JsonResponse(re_d)
        return JsonResponse({"code": 0})

