from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, 're_crtl/re_control_index.html')


def query_view(request):
    return render(request, 're_crtl/re_control_bll.html')


re_data = {
    '/': {"filesArr": ["aaaa","bbbb","cccc", "aaaa","bbbb","cccc"]},
    '/bbbb/': {'filesArr': ['niaafdho', 'wosafdi', 'niaafdho', 'wosafdi', "aaaa", "cccc", "cccc", "cccc", "aaaa", 'safd']},
    '/bbbb/safd/': {'filesArr': ['naaho', 'woffhi']},
}
file_content = {
    '/aaaa': {
        'content':'这是一段内容',
        'tag': ['a']
    },
    '/cccc': {
        'content':'这是一段内容',
        'tag': ['a', 'e']
    },
    '/bbbb/niaafdho': {
        'content':'这是一段内容',
        'tag': ['a', 'c']
    },
    '/bbbb/wosafdi': {
        'content':'这是一段内容',
        'tag': ['b']
    },
    '/bbbb/safd/naaho': {
        'content':'这是一段内容',
        'tag': ['c']
    },
    '/bbbb/safd/woffhi': {
        'content':'这是一段内容',
        'tag': ['a', 'b', 'c']
    }
}



def query_main(request):
    if request.method == "GET":
        if int(request.GET.get('file_mode')) == 1:
            re_d = {'filesArr': re_data['/']["filesArr"][:5]}
            return JsonResponse(re_d)
        elif int(request.GET.get('file_mode')) == 2:
            forward_path = request.GET.get("file_name")
            if forward_path + '/' in re_data:
                re_d = {'code': 1, 'filesArr': re_data[forward_path + '/']['filesArr'][:5],
                        'newLayer': forward_path + '/'}
                return JsonResponse(re_d)
            else:
                re_d = {'code': 2, 'fileCon': file_content[forward_path]['content'],
                        'newLayer': forward_path, 'fileTags': file_content[forward_path]['tag']}
                return JsonResponse(re_d)
        elif int(request.GET.get('file_mode')) == 3:
            pre_path = '/' if len(request.GET.get("path_cur").rsplit('/', 2)) < 2 else \
            request.GET.get("path_cur").rsplit('/', 1)[0] + '/' \
                if request.GET.get("path_cur")[-1] != '/' else request.GET.get("path_cur").rsplit('/', 2)[0] + '/'
            re_d = {'pathInfo': pre_path, 'filesArr': re_data[pre_path]['filesArr'][:5]}
            return JsonResponse(re_d)
        elif int(request.GET.get('file_mode')) == 4:
            num_start= (int(request.GET.get("file_page")) - 1) * 5
            num_end = int(request.GET.get("file_page")) * 5
            file_path = request.GET.get("file_path")
            try:
                print(re_data[file_path]['filesArr'][num_start])
                re_d = {'code': 1, 'filesArr': re_data[file_path]['filesArr'][num_start:num_end]}
            except IndexError:
                re_d = {'code': 0}
            return JsonResponse(re_d)


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
            tag_name = request.POST.get("dir_name")
            file_content_path = request.GET.get("file_path")
            re_d = {"code": 1}
            return JsonResponse(re_d)
        elif int(request.GET.get("add_mode")) == 2:
            file_name = request.POST.get('file_name')
            tag_sel = request.POST.get("tag_sel")
            file_content_path = request.GET.get("file_path")
            re_d = {"code": 2}
            return JsonResponse(re_d)
        return JsonResponse({"code": 0})
