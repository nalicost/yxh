import FileManager
import os
import json
import re
from typing import Union, Dict, List
from pathlib import Path
import stat

class ReDocManager:
    
    def __init__(self):
        main_folder = r"C:\ReDocManager"
        title_structure_doc = ""
        pre_file_name = ""
        aft_file_name = ""
        suggest_file_name= ""

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
            print("子文件夹 {child_folder} 已存在")
        except Exception as e:
            print("创建文件夹时出错: {str(e)}")
            
    # 函数功能无法实现建议：写相对路径而非绝对路径
    def load_title_structure_doc(self):
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
        path = Path(r"\re_sub_title\re_sub_title.json") 
        if not path.exists():
            raise ValueError(f"文件不存在: ")
            
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.title_structure_doc = json.load(f)
                return self.title_structure_doc
            
        except json.JSONDecodeError as e:
            raise ValueError(f"无效的 JSON 格式: {e}")

    def load_json_doc(self, data):
        """
        读取结果数据头文件的结果文件数量，并加载结果文件模板 -> json
        
        """
        #if re_num == "":
        #    load_title_structure_doc(self)
        #    re_num = self.title_structure_doc.get("re_num")
        #    param_set = self.title_structure_doc.get("param_set")

        #file = open("file_name", 'r', encoding='utf-8')
        #data = json.load(file)

        road_data = data.get('道路数据')

        traffic_data_pre = {
            "道路数据":{}
            }

        traffic_data_aft = {
            "道路数据":{}
            }

        traffic_data_analyse = {
            "道路数据":{}
            }

        '''遍历键值对'''
        for key, value in road_data.items():
            road_data[key].pop("决策后")
            traffic_data_pre["道路数据"][key] = road_data.get(key)
        
        for key, value in road_data.items():
            '''print("{key}: {value}")'''
            '''print(road_data[key]["决策后"])'''
            road_data[key].pop("决策前", None)
            '''del road_data[key]["决策建议"]'''
            traffic_data_aft["道路数据"][key] = road_data.get(key)

        traffic_data_analyse["道路数据"]["决策建议"] = road_data.get("决策建议")

    def doc_json_generator(self, data):
        """
        存储传输过来的三个JSON文件 按要求的命名格式       
        """
        #file = open("file_name", 'r', encoding='utf-8')
        #data = json.load(file)
        """
        决策前
        """
        with open('re_decision_pre.json', 'w', encoding='utf-8') as f:
            json.dump(traffic_data_pre, f, ensure_ascii=False, indent=4)

        """
        决策后
        """

        with open('re_dicision_aft', 'w', encoding='utf-8') as f:
            json.dump(traffic_data_aft, f, ensure_ascii=False, indent=4)
            
        """
        决策建议
        """
        with open('re_analyse', 'w', encoding='utf-8') as f:
            json.dump(road_data_analyse, f, ensure_ascii=False, indent=4)

        #file.close()
        # 此处代码错误


    def doc_del(self,file_name):
        """
        删除指定的结果文件夹
        传输过来的文件夹名字，直接删除
        """
        fm = FileManager.FileManager()
        if fm.delete_file(file_name):
            print("delete successfully")
        else:
            print("delete failure")

    def doc_index(self,file_name):
        """
        查找到对应的结果文件夹
        查找传过来的文件夹名字
        """
        fm = FileManager.FileManager()
        return fm.search_files(file_name)

    def file_del(self,result_file_name):
        """
        删除指定的结果文件
        删除传过来的结果文件名字
        """
        fm = FileManager.FileManager()
        fm.delete_file(result_file_name)

    def file_index(self,result_file_name):
        """
        查找指定的结果文件
        查找传过来的结果文件名字
        """
        fm = FileManager.FileManager()
        fm.search_files(result_file_name)


    def add_tag(self, tag):
        """
        增加标签
        :param tag: 指定标签
        """
        file_name = r're_sub_title\re_sub_title.json'
        with open(file_name, 'r') as f:
            tags = json.load(f)
        tags["tag_" + tag] = "re_sub_title"
        ReDocManager.update_file(file_name,tags)

    def del_tag(self, tag):
  
        """
        删除标签

        :param tag: 指定标签
        """
        file_name = r're_sub_title\re_sub_title.json'
        with open(file_name, "r") as f:
            data = json.load(f)
            if "tag_" + tag in tags:
                data.pop("tag_" + tag)
                # 没有data这一全局变量，无法实现
        ReDocManager.update_file(file_name,data)

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


if __name__ == "__main__" :
    # os.chmod(r"C:\Users\吉毅诚\Desktop\ReDocManager2\ReDocManager\ReDocManager\re_sub_title\re_sub_title.json",stat.S_IRWXU)
    #huxiong = ReDocManager()
    # result1 = huxiong.doc_name_generator("test1")
    # print(result1)
    # doc_name_generator 测试无问题 可生成文件 可重复生成
    # result3 =huxiong.load_title_structure_doc()
    # print(result3)
    # load_title_structure_doc 函数测试未通过 无法实现功能 建议：写相对路径而非绝对路径
    # huxiong.doc_json_generator({'道路数据': {'广富林路': {'决策后': [{'时段': '12:00-12:30', '平均速度': 22.8, '拥堵频率': 52.1, '排队通过率': 115.4, '拥堵指数': 0.7, '变化': '平均速度↑25.3% 拥堵频率↓20.3% 排队长度↓19.2%'}, {'时段': '12:30-13:00', '平均速度': 26.1, '拥堵频率': 45.7, '排队通过率': 98.3, '拥堵指数': 0.63, '变化': '平均速度↑21.4% 拥堵频率↓21.6% 排队长度↓21.7%'}, {'时段': '13:00-13:30', '平均速度': 29.4, '拥堵频率': 38.6, '排队通过率': 84.2, '拥堵指数': 0.55, '变化': '平均速度↑19.0% 拥堵频率↓21.4% 排队长度↓22.3%'}, {'时段': '13:30-14:00', '平均速度': 33.7, '拥堵频率': 31.5, '排队通过率': 70.8, '拥堵指数': 0.47, '变化': '平均速度↑19.1% 拥堵频率↓21.6% 排队长度↓23.5%'}]}, '文汇路': {'决策后': [{'时段': '12:00-12:30', '平均速度': 18.9, '拥堵频率': 62.4, '排队通过率': 138.7, '拥堵指数': 0.8, '变化': '平均速度↓7.8% 拥堵频率↑6.3% 排队长度↑8.0%'}, {'时段': '12:30-13:00', '平均速度': 21.3, '拥堵频率': 55.8, '排队通过率': 121.6, '拥堵指数': 0.73, '变化': '平均速度↓7.8% 拥堵频率↑9.0% 排队长度↑8.3%'}, {'时段': '13:00-13:30', '平均速度': 23.7, '拥堵频率': 49.1, '排队通过率': 106.2, '拥堵指数': 0.66, '变化': '平均速度↓8.1% 拥堵频率↑10.1% 排队长度↑8.9%'}, {'时段': '13:30-14:00', '平均速度': 27.1, '拥堵频率': 41.5, '排队通过率': 91.4, '拥堵指数': 0.59, '变化': '平均速度↓7.2% 拥堵频率↑9.8% 排队长度↑9.2%'}]}, '人民北路': {'决策后': [{'时段': '12:00-12:30', '平均速度': 20.6, '拥堵频率': 58.2, '排队通过率': 127.3, '拥堵指数': 0.77, '变化': '平均速度↓7.6% 拥堵频率↑6.6% 排队长度↑7.2%'}, {'时段': '12:30-13:00', '平均速度': 23.1, '拥堵频率': 51.4, '排队通过率': 111.6, '拥堵指数': 0.7, '变化': '平均速度↓6.9% 拥堵频率↑8.7% 排队长度↑7.9%'}, {'时段': '13:00-13:30', '平均速度': 25.4, '拥堵频率': 44.8, '排队通过率': 97.2, '拥堵指数': 0.63, '变化': '平均速度↓7.6% 拥堵频率↑8.7% 排队长度↑8.2%'}, {'时段': '13:30-14:00', '平均速度': 28.7, '拥堵频率': 38.1, '排队通过率': 83.4, '拥堵指数': 0.56, '变化': '平均速度↓7.1% 拥堵频率↑9.8% 排队长度↑9.0%'}]}, '银泽路': {'决策后': [{'时段': '12:00-12:30', '平均速度': 14.3, '拥堵频率': 75.6, '排队通过率': 168.4, '拥堵指数': 0.92, '变化': '平均速度↓9.5% 拥堵频率↑6.0% 排队长度↑6.4%'}, {'时段': '12:30-13:00', '平均速度': 16.7, '拥堵频率': 67.8, '排队通过率': 147.3, '拥堵指数': 0.84, '变化': '平均速度↓9.2% 拥堵频率↑6.8% 排队长度↑6.2%'}, {'时段': '13:00-13:30', '平均速度': 19.3, '拥堵频率': 59.2, '排队通过率': 128.1, '拥堵指数': 0.76, '变化': '平均速度↓9.0% 拥堵频率↑7.4% 排队长度↑6.4%'}, {'时段': '13:30-14:00', '平均速度': 22.4, '拥堵频率': 51.3, '排队通过率': 110.5, '拥堵指数': 0.68, '变化': '平均速度↓8.9% 拥堵频率↑7.3% 排队长度↑6.4%'}]}}})
    # doc_json_generator 测试有问题 具体见上
    # huxiong.doc_del("test1")
    # doc_del 测试通过
    # huxiong.file_del()
    # huxiong.file_index()
    # result2 = huxiong.doc_name_generator("Hi")
    # print(result2)
    # doc_name_generator 测试无问题
    # 缺少删除文件夹的方法
    # update file在文件生成中调用 不要让其独立调用 需要做一个组合 组成一个完整的函数(传高阶函数进update_file)
    # huxiong.doc_del("pao_re_doc")
    # doc_del 测试无误
    # huxiong.doc_index()
    # huxiong.add_tag("决策建议")
    # huxiong.update_file()
