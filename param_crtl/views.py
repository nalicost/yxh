import shutil
from time import sleep
from django.shortcuts import render
from core.ParamDocManager import ParamDocManager
from django.http import JsonResponse
from GeneratorArtificialIntelligenceSimulationTraffic.settings import BASE_DIR
import os
# Create your views here.


# 实例化初始参数管理类
param_doc_manager = ParamDocManager(os.path.join(BASE_DIR, 'files/param_files'))

def index_view(request):
    return render(request, 'param_crtl/param_control_index.html')


def query_view(request):
    return render(request, 'param_crtl/param_control_bll.html')


def query_main_back_info(request):
    if request.method == "GET":
        if int(request.GET.get("file_mode")) == 1:
            return origin_info()
        elif int(request.GET.get("file_mode")) == 2:
            return next_layer(request)
        elif int(request.GET.get("file_mode")) == 3:
            return last_layer(request)
        elif int(request.GET.get("file_mode")) == 4:
            return turn_page(request)
        else:
            return 0
    else:
        return 0


def turn_page(request, path=''):
    num_start = (int(request.GET.get("file_page")) - 1) * 5
    num_end = int(request.GET.get("file_page")) * 5
    file_path: str = request.GET.get("file_path") if not path else path
    final_path = os.path.join(param_doc_manager.base_path, file_path[1:])
    re_data = os.listdir(final_path)
    try:
        print(re_data[num_start])
        re_d = {'code': 1, 'filesArr': re_data[num_start:num_end]}
    except IndexError:
        re_d = {'code': 0}
    return JsonResponse(re_d)


def last_layer(request):
    pre_path = '/' if len(request.GET.get("path_cur").rsplit('/', 2)) < 2 else \
    request.GET.get("path_cur").rsplit('/', 1)[0] + '/' \
        if request.GET.get("path_cur")[-1] != '/' else request.GET.get("path_cur").rsplit('/', 2)[0] + '/'
    final_path = os.path.join(param_doc_manager.base_path, pre_path[1:])
    re_data = os.listdir(final_path)
    re_d = {'pathInfo': pre_path, 'filesArr': re_data[:5]}
    return JsonResponse(re_d)


def next_layer(request):
    forward_path: str = request.GET.get("file_name")
    final_path = os.path.join(param_doc_manager.base_path, forward_path[1:])
    try:
        with open(final_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        re_d = {'code': 2, 'fileCon': file_content, 'newLayer': forward_path}
        return JsonResponse(re_d)
    except Exception as e:
        print(e)
        re_data = os.listdir(final_path)
        re_d = {'code': 1, 'filesArr': re_data[:5], 'newLayer': forward_path + '/'}
        return JsonResponse(re_d)


def origin_info():
    re_data = os.listdir(param_doc_manager.base_path)
    re_d = {'filesArr': re_data[:5]}
    return JsonResponse(re_d)


def query_delete_back_info(request):
    if request.method == "GET":
        del_path = request.GET.get("file_name").rsplit('/', 1)[0] + '/' if request.GET.get("file_name").rsplit('/', 1)[0] else '/'
        del_file = request.GET.get("file_name").rsplit("/", 1)[1]
        final_path = os.path.join(param_doc_manager.base_path, del_path[1:], del_file)
        if del_file.endswith('_title.json'):
            return JsonResponse({'code': 0})
        try:
            os.remove(final_path)
        except Exception as e:
            print(e)
            shutil.rmtree(final_path)
        return turn_page(request, del_path)
    else:
        re_d = {"code": 0}
        return JsonResponse(re_d)

def upload_view(request):
    if request.method == "POST":
        if int(request.GET.get("add_mode")) == 1:
            return doc_add(request)
        elif int(request.GET.get("add_mode")) == 2:
            sleep(1)
            return title_file_add(request)
        elif int(request.GET.get("add_mode")) == 3:
            return param_file_add(request)
        return JsonResponse({"code": 0})


def doc_add(request):
    dir_name = request.POST.get("dir_name")
    re_status = param_doc_manager.doc_name_generator(dir_name)
    if re_status == 0:
        return JsonResponse({'code': 0})
    re_d = {"code": 1}
    return JsonResponse(re_d)


def title_file_add(request):
    file_content_upload = request.FILES.get('fileObj')
    dir_name = request.GET.get("dir_name")
    header_list = file_deal_title(file_content_upload.readlines())
    if not header_list:
        shutil.rmtree(os.path.join(param_doc_manager.base_path, f'{dir_name}_param_doc'))
        return JsonResponse({'code': 5})
    re_status = param_doc_manager.load_title_structure_doc(header_list, dir_name)
    return return_generator_status(re_status)


def return_generator_status(re_status):
    if re_status == 0:
        return JsonResponse({'code': 3})
    elif re_status == 2:
        return JsonResponse({'code': 4})
    else:
        re_d = {"code": 2}
        return JsonResponse(re_d)


def param_file_add(request):
    file_only_content_upload = request.FILES.get('fileObj')
    file_content_path = request.GET.get("file_path")
    final_path = os.path.join(param_doc_manager.base_path, file_content_path[1:])
    if not final_path.endswith('_param_doc/'):
        return JsonResponse({'code': 3})
    param_list = file_deal_content(file_only_content_upload.read())
    if param_list == 0:
        return JsonResponse({'code': 5})
    elif param_list == 1:
        return JsonResponse({'code': 4})
    param = param_doc_manager.load_json_doc(param_list)
    param_doc_manager.doc_json_generator(param, file_content_path.split('/')[-2].split('_')[0])
    re_d = {"code": 1}
    return JsonResponse(re_d)


def file_deal_title(file_con):
    re_list = ['road_info']
    for item in file_con:
        try:
            re_list.append(item.strip().decode('utf-8'))
        except Exception as e:
            print(e)
            return 0
    return re_list


def file_deal_content(file_con):
    re_list = []
    try:
        file_con = file_con.decode('utf-8')
    except Exception as e:
        print(e)
        return 0
    try:
        main_list = file_con.split('#')
        main_list = [i.strip() for i in main_list]
        if len(main_list) != 3:
            return 1
        for item in range(3):
            if item == 0:
                re_list.append(main_list[item].strip())
            else:
                re_sub_list = []
                sub_list = main_list[item].split('$')
                sub_list = [i.strip() for i in sub_list]
                for sub in sub_list:
                    sub_item_list = sub.split('\n')
                    if item == 1 and len(sub_item_list) != 4:
                        return 1
                    elif item == 2 and len(sub_item_list) != 3:
                        return 1
                    sub_item_list = [i.strip() for i in sub_item_list]
                    re_sub_list.append(sub_item_list)
                re_list.append(re_sub_list)
    except Exception as e:
        print(e)
        return 1
    return re_list

