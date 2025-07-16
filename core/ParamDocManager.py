import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import shutil
import re
class ParamDocManager:
    def __init__(self, base_path: str = "./param_docs",):
        """
        初始化基础目录，自动创建路径
        
        :param base_path: 基础存储路径,你想他在那个路径就填哪个，否则默认为当前工作目录
         """
         #跨平台将字符串转化为path对象
        self.base_path = Path(base_path).resolve()
      

    def doc_name_generator(self,user_name: str):
        #生成对应用户名的文件夹
        self.base_path.mkdir(exist_ok=True, parents=True)
        if not re.match(r'^[a-z0-9_]+$', user_name):
            return 0
        
        # 组装目标路径
        target_dir = self.base_path / f"{user_name}_param_doc"
        # 重复性检查
        if target_dir.exists():
            return 0
        target_dir.mkdir()
        return 1

    @staticmethod
    def count_files(path, recursive=False):
        #统计对应路径的文件数量
        print(type(path))
        path = Path(path)
        if recursive:
            return sum(1 for file in path.rglob('*') if file.is_file())
        else:
            return sum(1 for file in path.iterdir() if file.is_file())

    def load_title_structure_doc(self, header_list:list,user_name: str):
        '''
        放入对应的参数列表在对应用户名的路径下生成头文件
        参数列表为[road_info,road_names……]
                  
        '''
        target_dir = self.base_path / f"{user_name}_param_doc"
        road_info = header_list[0]
        road_names = header_list[1:]
        param_count = 0
        # 生成头文件
        header = {
            "road_info": road_info,
            **{f"road_name{i+1}": name for i, name in enumerate(road_names)},  
            "param_num": param_count
        }
        if os.path.exists(target_dir / "origin_param_title.json"):
            return 0
        with (target_dir / "origin_param_title.json").open('w', encoding='utf-8') as f:
                json.dump(header, f, indent=2,ensure_ascii=False)
        return 1
     


    def load_json_doc(self,param_list: list) -> Dict:
        """
        放入参数列表转化为对应的字典
        参数列表格式为["start_time",[["name", "range", "level", "re"],…………],[["content", "location", "time"],…………]]
        """
        special_list = param_list[1]
        decision_list = param_list[2]
        special_list_dict = [dict(zip(("name", "range", "level", "re"), item)) for item in special_list]
        decision_list_dict = [dict(zip(("content", "location", "time"), item)) for item in decision_list]
        param = {
            "start_time": param_list[0],
            **{f"special{i+1}": name for i, name in enumerate(special_list_dict)},
            **{f"decision{i+1}": name for i, name in enumerate(decision_list_dict)}
        }
        return param
   
        
    def doc_json_generator(self,param,user_name: str) -> None:
        """
        将所给json文件放入对应用户名文件夹
        """
        count = 0
        target_dir = self.base_path / f"{user_name}_param_doc"

        with open(target_dir / "origin_param_title.json",'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data["param_num"] += 1 
                    count =  data["param_num"]
        with (target_dir / f"origin_param{count}.json").open('w', encoding='utf-8') as f:
                json.dump(param, f, indent=2,ensure_ascii=False)
        
        with (target_dir / "origin_param_title.json").open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2,ensure_ascii=False)
        


    def doc_index(self, pattern: str = "*_param_doc") -> Path:
        """查找对应的参数集文件夹"""
        return self.base_path / pattern
    

    def doc_del(self, doc_name: str) -> None:
        """删除对应的参数集文件夹"""
        target = self.doc_index(doc_name)
        print(target)
        if not target.exists():
            raise FileNotFoundError(f"参数集 {doc_name} 不存在")
        shutil.rmtree(target)


    def file_index(self, user_name: str, doc_name: str) -> Path:
        """输入用户名及文件名获取参数文件路径"""
        return self.base_path / f"{user_name}_param_doc" / Path(doc_name)
    

    def file_del(self,user_name: str, doc_name: str) -> None:
        """输入用户名文件名删除指定参数文件"""
        target = self.file_index(user_name, doc_name)
        print(type(target))
      
        target.unlink()





    

    
   
  
