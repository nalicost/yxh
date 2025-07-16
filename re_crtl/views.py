import os.path
import shutil
from pathlib import Path
from django.http import JsonResponse
from django.shortcuts import render
from core.ReDocManager import ReDocManager

# Create your views here.
re_doc_manager = ReDocManager('./files/re_files/')

def index_view(request):
    return render(request, 're_crtl/re_control_index.html')


def query_view(request):
    return render(request, 're_crtl/re_control_bll.html')


def query_main(request):
    if request.method == "GET":
        if int(request.GET.get('file_mode')) == 1:
            return origin_info()
        elif int(request.GET.get('file_mode')) == 2:
            return forward(request)
        elif int(request.GET.get('file_mode')) == 3:
            return previous(request)
        elif int(request.GET.get('file_mode')) == 4:
            return turn_page(request)


def turn_page(request):
    num_start = (int(request.GET.get("file_page")) - 1) * 5
    num_end = int(request.GET.get("file_page")) * 5
    file_path = request.GET.get("file_path")
    final_path = re_doc_manager.main_folder + file_path[1:]
    re_data = os.listdir(final_path)
    try:
        print(re_data[num_start])
        re_d = {'code': 1, 'filesArr': re_data[num_start:num_end]}
    except IndexError:
        re_d = {'code': 0}
    return JsonResponse(re_d)


def previous(request):
    pre_path = '/' if len(request.GET.get("path_cur").rsplit('/', 2)) < 2 else \
        request.GET.get("path_cur").rsplit('/', 1)[0] + '/' \
            if request.GET.get("path_cur")[-1] != '/' else request.GET.get("path_cur").rsplit('/', 2)[0] + '/'
    final_path = re_doc_manager.main_folder + pre_path[1:]
    re_data = os.listdir(final_path)
    re_d = {'pathInfo': pre_path, 'filesArr': re_data[:5]}
    return JsonResponse(re_d)


def forward(request):
    forward_path = request.GET.get("file_name")
    try:
        with open(re_doc_manager.main_folder + forward_path[1:], 'r', encoding='utf-8') as f:
            file_content = f.read()
        file_tags = ''
        return if_file_with_tag_index(file_content, file_tags, forward_path)
    except Exception as e:
        print(e)
        return dir_forward(forward_path)


def dir_forward(forward_path):
    final_path = re_doc_manager.main_folder + forward_path[1:]
    re_data = os.listdir(final_path)
    re_d = {'code': 1, 'filesArr': re_data[:5],
            'newLayer': forward_path + '/'}
    return JsonResponse(re_d)


def if_file_with_tag_index(file_content, file_tags, forward_path):
    if forward_path.rsplit('/', 1)[-1] in ['aft_decision.json', 'pre_decision.json', 'suggestion.json']:
        file_name = '/'.join(forward_path.rsplit('/', 2)[-2:])
        file_tags = re_doc_manager.index_tag(file_name=file_name,
                                             path='/'.join([forward_path.rsplit('/', 2)[0], '/re_title.json']))
        file_tags = [i.split('_')[1] for i in file_tags]
    re_d = {'code': 2, 'fileCon': file_content,
            'newLayer': forward_path, 'fileTags': file_tags}
    return JsonResponse(re_d)


def origin_info():
    re_data = os.listdir(re_doc_manager.main_folder)
    re_d = {'filesArr': re_data[:5]}
    return JsonResponse(re_d)


def query_delete_back_info(request):
    if request.method == "GET":
        num_start = (int(request.GET.get("file_page")) - 1) * 5
        num_end = int(request.GET.get("file_page")) * 5
        del_path = request.GET.get("file_name").rsplit('/', 1)[0] + '/' if request.GET.get("file_name").rsplit('/', 1)[0] else '/'
        del_file = request.GET.get("file_name").rsplit("/", 1)[1]
        final_path = re_doc_manager.main_folder + del_path[1:]
        try:
            shutil.rmtree(final_path + del_file)
        except Exception as e:
            print(e)
            return JsonResponse({'code': 0})
        re_data = os.listdir(final_path)
        re_d = {"code": 1, "filesArr": re_data[num_start:num_end]}
        return JsonResponse(re_d)
    else:
        re_d = {"code": 0}
        return JsonResponse(re_d)


def upload_view(request):
    if request.method == "POST":
        if int(request.GET.get("add_mode")) == 1:
            tag_name = request.POST.get("dir_name")
            file_content_path = request.GET.get("file_path")
            not_add = int(request.POST.get("not_add"))
            if not not_add:
                return tag_add(file_content_path, tag_name)
            else:
                return tag_del(file_content_path, tag_name)
        elif int(request.GET.get("add_mode")) == 2:
            file_name = request.POST.get('file_name')
            tag_sel = request.POST.get("tag_sel")
            file_content_path = request.GET.get("file_path")
            not_add = int(request.POST.get("not_add"))
            if not not_add:
                return file_add_tag(file_content_path, file_name, tag_sel)
            else:
                return fill_rm_tag(file_content_path, file_name, tag_sel)
        return JsonResponse({"code": 0})


def tag_del(file_content_path, tag_name):
    if not file_content_path.endswith('_doc/'):
        return JsonResponse({'code': 5})
    re_status = re_doc_manager.del_tag(tag_name, file_content_path[1:] + 're_title.json')
    if not re_status:
        return JsonResponse({'code': 7})
    re_d = {'code': 4}
    return JsonResponse(re_d)


def tag_add(file_content_path, tag_name):
    if not file_content_path.endswith('_doc/'):
        return JsonResponse({'code': 3})
    re_status = re_doc_manager.add_tag(tag_name, file_content_path[1:] + 're_title.json')
    if not re_status:
        return JsonResponse({'code': 6})
    else:
        re_d = {'code': 1}
        return JsonResponse(re_d)


def fill_rm_tag(file_content_path, file_name, tag_sel):
    if not file_content_path.endswith('_doc/'):
        return JsonResponse({'code': 5})
    elif not os.path.exists(re_doc_manager.main_folder + file_content_path[1:] + file_name):
        return JsonResponse({'code': 11})
    re_status = re_doc_manager.rm_file(file_content_path[1:] + 're_title.json', tag_sel, file_name)
    if not re_status:
        return JsonResponse({'code': 7})
    elif re_status == 2:
        return JsonResponse({'code': 8})
    else:
        re_d = {"code": 10}
        return JsonResponse(re_d)


def file_add_tag(file_content_path, file_name, tag_sel):
    if not file_content_path.endswith('_doc/'):
        return JsonResponse({'code': 3})
    elif not os.path.exists(re_doc_manager.main_folder + file_content_path[1:] + file_name):
        return JsonResponse({'code': 11})
    re_status = re_doc_manager.add_file(file_content_path[1:] + 're_title.json', tag_sel, file_name)
    if not re_status:
        return JsonResponse({'code': 7})
    elif re_status == 2:
        return JsonResponse({'code': 9})
    else:
        re_d = {"code": 2}
        return JsonResponse(re_d)
