#import FileManager
import os
import json
import re
from typing import Union, Dict, List
from pathlib import Path

class ReDocManager:
    
    def __init__(self):
        main_folder = "C:\\ReDocManager"
        title_structure_doc = ""

    def doc_name_generator(self,base_name):
        """
        生成父结果文件夹，并进行命名，文件夹命名规范：{参数集文件夹中用户给出的名字}_re_doc
        生成子结果文件夹，并进行命名，文件夹命名规范：re_doc{doc_re_num}  
        文件夹命名要求：都为英文小写字母，不得重复
        判断{参数集文件夹中用户给出的名字}是否存在，如果不存在，则创建该文件夹
        创建成功，则从文件夹中文件名称中判断已有的{doc_re_num}最大的是哪个，并加一

        :param base_name: 参数集文件夹中用户给出的名字
        """
         
        '''规范化为小写字母并移除非法字符'''
        base_name = re.sub(r'[^a-z0-9]', '', base_name.lower())
        if not base_name:
            return False, "无效的文件夹名称", None, None
        
        parent_folder = f"{base_name}_re_doc"
        try:
            '''创建父文件夹（如果不存在）'''
            os.makedirs(parent_folder, exist_ok=True)
            
            '''2. 查找父文件夹中已有的子文件夹编号'''
            existing_nums = []
            pattern = re.compile(r'^re_doc(\d+)$')
            
            for item in os.listdir(parent_folder):
                item_path = os.path.join(parent_folder, item)
                if os.path.isdir(item_path):
                    match = pattern.match(item)
                    if match:
                        existing_nums.append(int(match.group(1)))
            
            '''确定新编号（最大编号+1，如果没有则为1）'''
            new_num = max(existing_nums) + 1 if existing_nums else 1
            
            '''3. 创建子文件夹 re_doc{new_num}'''
            child_folder = f"re_doc{new_num}"
            child_path = os.path.join(parent_folder, child_folder)
            os.makedirs(child_path, exist_ok=False)  # 确保不会覆盖已有文件夹
            
            return True, "文件夹创建成功", os.path.abspath(parent_folder), os.path.abspath(child_path)
        
        except FileExistsError:
            return False, f"子文件夹 {child_folder} 已存在", None, None
        except Exception as e:
            return False, f"创建文件夹时出错: {str(e)}", None, None
               

    def load_title_structure_doc(self,file_path: Union[str, Path]) -> Union[Dict, List]:
        """
        加载结果数据头文件模板
        在文件夹中找re_title文件->JSON并加载返回
        返回“JSON已调用”
        """
        """
        从 JSON 文件加载数据
        
        :param file_path: JSON 文件路径
        :return: 解析后的 Python 对象
        :raises: ValueError 如果文件不存在或 JSON 格式无效
        """
        path = Path(file_path)
        if not path.exists():
            raise ValueError(f"文件不存在: {file_path}")
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.title_structure_doc = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"无效的 JSON 格式: {e}")

    def load_json_doc(self):
        """
        读取结果数据头文件的结果文件数量，并加载结果文件模板 -> json
        
        """
        re_num = title_structure_doc["re_num"]
        param_set = title_structure_doc["param_set"]

        pre_file_name = string.format("re_sub_title/{param_set}_re_doc/re_doc{re_num}/re_decision_pre")
        aft_file_name = string.format("re_sub_title/{param_set}_re_doc/re_doc{re_num}/re_dicision_aft")
        suggest_file_name= string.format("re_sub_title/{param_set}_re_doc/re_doc{re_num}/re_analyse")
        
        with open("pre_file_name", 'r', encoding='utf-8') as re_decision_pre:
            re_decision_pre = json.load(pre_file)
            
        with open("aft_file_name", 'r', encoding='utf-8') as re_dicision_aft:
            re_dicision_aft = json.load(aft_file)
            
        with open("suggest_file_name", 'r', encoding='utf-8') as re_analyse:
            re_analyse = json.load(suggest_file)

        return re_decision_pre,re_dicision_aft,re_analyse

    def doc_json_generator(self):
        """
        存储传输过来的三个JSON文件 按要求的命名格式       
        """
        file = open("file_name", 'r', encoding='utf-8')
        data = json.load(file)

        road_data = data['道路数据']

        traffic_data = {
            "道路数据":{}
            }

        '''遍历键值对'''
        for key, value in road_data.items():
            del road_data[key]["决策后"]
            traffic_data["道路数据"][key] = road_data[key]

        with open('re_decision_pre.json', 'w', encoding='utf-8') as f:
            json.dump(traffic_data, f, ensure_ascii=False, indent=4)

        """
        决策后
        """

        road_data = data['道路数据']

        traffic_data = {
            "道路数据":{}
            }

        '''遍历键值对'''
        for key, value in road_data.items():
            '''print("{key}: {value}")'''
            '''print(road_data[key]["决策后"])'''
            del road_data[key]["决策前"]
            '''del road_data[key]["决策建议"]'''
    
            traffic_data["道路数据"][key] = road_data[key]

        with open('re_dicision_aft', 'w', encoding='utf-8') as f:
            json.dump(traffic_data, f, ensure_ascii=False, indent=4)
            
        """
        决策建议
        """
        road_data = data['决策建议']


        with open('re_analyse', 'w', encoding='utf-8') as f:
            json.dump(road_data, f, ensure_ascii=False, indent=4)

        file.close()


    def doc_del(self,file_name):
        """
        删除指定的结果文件夹
        传输过来的文件夹名字，直接删除
        """
        fm = FileManager()
        fm.delete_file(file_name)


    def doc_index(filename):
        """
        查找到对应的结果文件夹
        查找传过来的文件夹名字
        """
        fm = FileManager()
        fm.search_files(file_name)

    def file_del(self,result_file_name):
        """
        删除指定的结果文件
        删除传过来的结果文件名字
        """
        fm = FileManager()
        fm.delete_file(result_file_name)

    def file_index(self,result_file_name):
        """
        查找指定的结果文件
        查找传过来的结果文件名字
        """
        fm = FileManager()
        fm.search_files(result_file_name)


    def add_tag(self, tag):
        """
        增加标签
        :param tag: 指定标签
        """
        with open('re_title', 'r') as f:
            tags = json.load(f)
        tags["new_tag"] = "new_value"

    def del_tag(self, tag):
        """
        删除标签

        :param tag: 指定标签
        """
        with open("re_title", "r") as f:
            tags = json.load(f)
            if "tag" in tags:
                del data["tag"]


    def add_file(self,data,tag, file_name):
        """
        在指定标签中增加文件名
        :param data: 包含标签和文件的字典数据
        :param tag: 指定标签
        :param file_name: 文件名
        :return: 修改后的数据
        """
        '''如果标签不存在，则创建'''
        if tag not in data:
            data[tag] = {"files": []}
            print(f"提示: 已创建新标签 '{tag}'")
    
        '''如果标签下没有files列表，则创建'''
        if 'files' not in data[tag]:
            data[tag]['files'] = []
            print(f"提示: 已为标签 '{tag}' 创建文件列表")
    
        '''检查文件是否已存在'''
        if file_name in data[tag]['files']:
            print(f"提示: 文件 '{file_name}' 已在标签 '{tag}' 中存在")
            return data
    
        '''添加文件'''
        data[tag]['files'].append(file_name)
        print(f"成功: 已将文件 '{file_name}' 添加到标签 '{tag}'")
    
        return data

    
    def rm_file(self,data,tag, file_name):
        """
        在指定标签中删除文件名
        :param data: 包含标签和文件的字典数据
        :param tag: 指定标签
        :param file_name: 文件名
        :return: 修改后的数据
        """
        if tag not in data:
            print(f"警告: 标签 '{tag}' 不存在")
            return data
    
        '''检查标签下的文件列表是否存在'''
        if 'files' not in data[tag]:
            print(f"警告: 标签 '{tag}' 下没有文件列表")
            return data
    
        '''尝试删除文件'''
        try:
            data[tag]['files'].remove(file_name)
            print(f"成功: 已从标签 '{tag}' 中删除文件 '{file_name}'")
        except ValueError:
            print(f"警告: 文件 '{file_name}' 不在标签 '{tag}' 的文件列表中")
    
        return data

    def update_file(self,file_name,data):
        """
        更新文件内容信息
        """
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"数据已写入 {file_name}")
