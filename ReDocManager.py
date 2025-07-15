import os
import json
import shutil


class ReDocManager:
    """
    结果文档管理器类，用于管理报告文档的生成、存储和操作
    
    主要功能包括：
    - 创建文档存储的目录结构
    - 生成结果文档的JSON文件
    - 对文档进行标签管理
    - 文档的删除和索引
    
    属性:
        main_folder (str): 文档存储的主目录路径，默认为'./re_doc/'
    """
    
    def __init__(self, path="./re_doc/"):
        """初始化结果文档管理器
        
        Args:
            path (str, optional): 文档存储的主目录路径. 默认为'./re_doc/'
        """
        self.main_folder = rf"{path}"

    def main_dir_structure_generator(self, base_name):
        """
        创建主文档目录结构
        
        生成父结果文件夹，命名规范：{base_name}_re_doc
        在父文件夹中创建re_title.json文件用于记录子文件夹数量
        
        Args:
            base_name (str): 用户给定的基础名称，用于构建父文件夹名称
        """
        parent_folder = f"{base_name}_re_doc"  # 父文件夹名称
        par_path = self.main_folder + parent_folder  # 完整父路径
        os.makedirs(par_path)  # 创建父目录
        
        # 初始化re_title.json文件，记录子文档数量
        with open(rf'{par_path}/re_title.json', 'w', encoding='utf-8') as f:
            tem = {'num': 0}  # 初始数量为0
            f.write(json.dumps(tem))

    def load_title_structure_doc(self, path, param_set):
        """
        创建子文档目录结构
        
        在指定父文件夹中创建新的子文件夹(re_subN)，并记录参数集信息
        
        Args:
            path (str): 父文件夹的相对路径
            param_set (dict): 需要保存的参数集信息
        """
        path = self.main_folder + path  # 获取完整父路径
        
        # 读取父文件夹中的标题信息
        with open(rf'{path}/re_title.json', 'r') as f:
            re_info = json.load(f)
        
        re_info['num'] += 1  # 子文档计数器+1
        chi_folder = rf'{path}/re_sub{re_info["num"]}'  # 子文件夹路径
        os.makedirs(chi_folder)  # 创建子目录
        
        # 更新父文件夹的标题信息
        with open(rf'{path}/re_title.json', 'w') as f:
            f.write(json.dumps(re_info))
        
        # 在子文件夹中创建参数集记录文件
        sub_json = chi_folder + '/re_sub_title.json'
        with open(sub_json, 'w', encoding='utf-8') as f:
            data = {'param_set': param_set}
            f.write(json.dumps(data, ensure_ascii=False))

    @staticmethod
    def load_json_doc(data):
        """
        解析结果数据，分离出决策前、决策后和决策建议三部分
        
        Args:
            data (dict): 包含完整结果数据的字典
            
        Returns:
            tuple: 包含三个元素的元组
                - traffic_data_pre (dict): 决策前的道路数据
                - traffic_data_aft (dict): 决策后的道路数据
                - traffic_data_analyse (dict): 决策建议数据
        """
        # 初始化数据结构
        traffic_data_pre = {"道路数据": {}}
        traffic_data_aft = {"道路数据": {}}
        traffic_data_analyse = {}
        
        # 遍历输入数据
        for key, value in data.items():
            if key == '道路数据':
                # 提取决策前数据
                for k, v in value.items():
                    traffic_data_pre['道路数据'][k] = v['决策前']
                # 提取决策后数据
                for k, v in value.items():
                    traffic_data_aft['道路数据'][k] = v['决策后']
            elif key == '决策建议':
                # 提取决策建议
                traffic_data_analyse[key] = value
                
        return traffic_data_pre, traffic_data_aft, traffic_data_analyse

    def doc_json_generator(self, data_list, file_name_list):
        """
        生成结果JSON文件
        
        将三个部分的数据分别写入对应的JSON文件中
        
        Args:
            data_list (list): 包含三个数据部分的列表 [决策前数据, 决策后数据, 决策建议]
            file_name_list (list): 包含三个文件路径的列表 [决策前文件路径, 决策后文件路径, 决策建议文件路径]
        """
        # 遍历三个数据部分
        for item in range(3):
            doc_path = self.main_folder + file_name_list[item]  # 完整文件路径
            # 写入JSON文件
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(data_list[item], ensure_ascii=False))

    def doc_del(self, file_name):
        """
        删除指定的结果文件夹（递归删除）
        
        Args:
            file_name (str): 要删除的文件夹相对路径
        """
        doc_path = self.main_folder + file_name  # 完整路径
        shutil.rmtree(doc_path)  # 递归删除文件夹

    def doc_index(self, file_name):
        """
        获取文档的完整路径
        
        Args:
            file_name (str): 文档的相对路径
            
        Returns:
            str: 文档的完整路径
        """
        return self.main_folder + file_name

    def file_index(self, file_name):
        """
        获取文件的完整路径（功能与doc_index相同）
        
        Args:
            file_name (str): 文件的相对路径
            
        Returns:
            str: 文件的完整路径
        """
        return self.main_folder + file_name

    def add_tag(self, tag, file_name):
        """
        在JSON文件中添加新标签
        
        Args:
            tag (str): 要添加的标签名称
            file_name (str): 目标JSON文件的相对路径
        """
        path_tit = self.main_folder + file_name  # 完整文件路径
        
        # 读取现有数据
        with open(path_tit, 'r') as f:
            data = json.load(f)
        
        if "tag_" + tag in data:
            raise ValueError
        # 添加新标签（格式为"tag_标签名"）
        data["tag_" + tag] = []
        
        # 更新文件内容
        self.update_file(file_name, data)

    def index_tag(self, file_name, path):
        """
        在标签索引文件中查找包含指定文件名的标签
        
        Args:
            file_name (str): 要查找的文件名
            path (str): 标签索引文件的相对路径
            
        Returns:
            list: 包含该文件名的标签列表
        """
        path_tit = self.main_folder + path  # 完整索引文件路径
        tag_li = []  # 结果列表
        
        # 读取索引文件
        with open(path_tit, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 遍历所有标签项
        for item in data:
            if file_name in item:
                tag_li.append(item)
                
        return tag_li

    def del_tag(self, tag, file_name):
        """
        从JSON文件中删除指定标签
        
        Args:
            tag (str): 要删除的标签名称
            file_name (str): 目标JSON文件的相对路径
        """
        path_tit = self.main_folder + file_name  # 完整文件路径
        
        # 读取现有数据
        with open(path_tit, "r", encoding='utf-8') as f:
            data = json.load(f)
            
        # 检查标签是否存在
        if "tag_" + tag not in data:
            raise ValueError(f"标签 {tag} 不存在")
        
        # 删除标签
        del data["tag_" + tag]
        
        # 更新文件
        self.update_file(file_name, data)

    def add_file(self, path, tag, file_name):
        """
        在指定标签下添加文件名
        
        Args:
            path (str): 标签索引文件的相对路径
            tag (str): 目标标签名称
            file_name (str): 要添加的文件名
            
        Raises:
            ValueError: 如果标签不存在或文件名已存在
        """
        path_tit = self.main_folder + path  # 完整索引文件路径
        
        # 读取索引数据
        with open(path_tit, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查标签是否存在
        if "tag_" + tag not in data:
            raise ValueError(f"标签 {tag} 不存在")
            
        # 检查文件名是否已存在
        if file_name in data["tag_" + tag]:
            raise ValueError(f"文件名 {file_name} 已存在于标签中")
        
        # 添加文件名
        data["tag_" + tag].append(file_name)
        
        # 更新文件
        self.update_file(path, data)

    def rm_file(self, path, tag, file_name):
        """
        从标签中移除文件名
        
        Args:
            path (str): 标签索引文件的相对路径
            tag (str): 目标标签名称
            file_name (str): 要移除的文件名
            
        Raises:
            ValueError: 如果标签不存在或文件名不在标签中
        """
        path_tit = self.main_folder + path  # 完整索引文件路径
        
        # 读取索引数据
        with open(path_tit, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查标签是否存在
        if "tag_" + tag not in data:
            raise ValueError(f"标签 {tag} 不存在")
            
        # 检查文件名是否存在
        if file_name not in data["tag_" + tag]:
            raise ValueError(f"文件名 {file_name} 不在标签中")
        
        # 移除文件名
        data["tag_" + tag].remove(file_name)
        
        # 更新文件
        self.update_file(path, data)

    def update_file(self, file_name, data):
        """
        更新JSON文件内容
        
        Args:
            file_name (str): 目标文件的相对路径
            data (dict): 要写入的新数据
        """
        path_tit = self.main_folder + file_name  # 完整文件路径
        
        # 写入更新后的数据
        with open(path_tit, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    # 示例用法
    hx = ReDocManager()
    
    # 测试数据
    data_use = {
  "权重配置": {
    "平均速度": 0.45,
    "拥堵频率": 0.30,
    "排队通过率": 0.25,
    "计算说明": "拥堵指数 = (1-平均速度/50)×0.45 + (拥堵频率/100)×0.30 + (排队长度/200)×0.25，自由流速度取50km/h，最大排队长度取200米"
  },
  "道路数据": {
    "广富林路": {
      "决策前": [
        {
          "时段": "12:00-12:30",
          "平均速度": 18.2,
          "拥堵频率": 65.4,
          "排队通过率": 142.8,
          "拥堵指数": 0.82,
          "说明": "暴雨峰值期，积水严重"
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 21.5,
          "拥堵频率": 58.3,
          "排队通过率": 125.6,
          "拥堵指数": 0.75,
          "说明": "降雨强度减弱"
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 24.7,
          "拥堵频率": 49.1,
          "排队通过率": 108.3,
          "拥堵指数": 0.68,
          "说明": "积水开始消退"
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 28.3,
          "拥堵频率": 40.2,
          "排队通过率": 92.5,
          "拥堵指数": 0.60,
          "说明": "暴雨影响减弱"
        }
      ],
      "决策后": [
        {
          "时段": "12:00-12:30",
          "平均速度": 22.8,
          "拥堵频率": 52.1,
          "排队通过率": 115.4,
          "拥堵指数": 0.70,
          "变化": "平均速度↑25.3% 拥堵频率↓20.3% 排队长度↓19.2%"
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 26.1,
          "拥堵频率": 45.7,
          "排队通过率": 98.3,
          "拥堵指数": 0.63,
          "变化": "平均速度↑21.4% 拥堵频率↓21.6% 排队长度↓21.7%"
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 29.4,
          "拥堵频率": 38.6,
          "排队通过率": 84.2,
          "拥堵指数": 0.55,
          "变化": "平均速度↑19.0% 拥堵频率↓21.4% 排队长度↓22.3%"
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 33.7,
          "拥堵频率": 31.5,
          "排队通过率": 70.8,
          "拥堵指数": 0.47,
          "变化": "平均速度↑19.1% 拥堵频率↓21.6% 排队长度↓23.5%"
        }
      ]
    },
    "文汇路": {
      "决策前": [
        {
          "时段": "12:00-12:30",
          "平均速度": 20.5,
          "拥堵频率": 58.7,
          "排队通过率": 128.4,
          "拥堵指数": 0.76
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 23.1,
          "拥堵频率": 51.2,
          "排队通过率": 112.3,
          "拥堵指数": 0.69
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 25.8,
          "拥堵频率": 44.6,
          "排队通过率": 97.5,
          "拥堵指数": 0.62
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 29.2,
          "拥堵频率": 37.8,
          "排队通过率": 83.7,
          "拥堵指数": 0.55
        }
      ],
      "决策后": [
        {
          "时段": "12:00-12:30",
          "平均速度": 18.9,
          "拥堵频率": 62.4,
          "排队通过率": 138.7,
          "拥堵指数": 0.80,
          "变化": "平均速度↓7.8% 拥堵频率↑6.3% 排队长度↑8.0%"
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 21.3,
          "拥堵频率": 55.8,
          "排队通过率": 121.6,
          "拥堵指数": 0.73,
          "变化": "平均速度↓7.8% 拥堵频率↑9.0% 排队长度↑8.3%"
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 23.7,
          "拥堵频率": 49.1,
          "排队通过率": 106.2,
          "拥堵指数": 0.66,
          "变化": "平均速度↓8.1% 拥堵频率↑10.1% 排队长度↑8.9%"
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 27.1,
          "拥堵频率": 41.5,
          "排队通过率": 91.4,
          "拥堵指数": 0.59,
          "变化": "平均速度↓7.2% 拥堵频率↑9.8% 排队长度↑9.2%"
        }
      ]
    },
    "人民北路": {
      "决策前": [
        {
          "时段": "12:00-12:30",
          "平均速度": 22.3,
          "拥堵频率": 54.6,
          "排队通过率": 118.7,
          "拥堵指数": 0.71
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 24.8,
          "拥堵频率": 47.3,
          "排队通过率": 103.4,
          "拥堵指数": 0.64
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 27.5,
          "拥堵频率": 41.2,
          "排队通过率": 89.8,
          "拥堵指数": 0.58
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 30.9,
          "拥堵频率": 34.7,
          "排队通过率": 76.5,
          "拥堵指数": 0.51
        }
      ],
      "决策后": [
        {
          "时段": "12:00-12:30",
          "平均速度": 20.6,
          "拥堵频率": 58.2,
          "排队通过率": 127.3,
          "拥堵指数": 0.77,
          "变化": "平均速度↓7.6% 拥堵频率↑6.6% 排队长度↑7.2%"
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 23.1,
          "拥堵频率": 51.4,
          "排队通过率": 111.6,
          "拥堵指数": 0.70,
          "变化": "平均速度↓6.9% 拥堵频率↑8.7% 排队长度↑7.9%"
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 25.4,
          "拥堵频率": 44.8,
          "排队通过率": 97.2,
          "拥堵指数": 0.63,
          "变化": "平均速度↓7.6% 拥堵频率↑8.7% 排队长度↑8.2%"
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 28.7,
          "拥堵频率": 38.1,
          "排队通过率": 83.4,
          "拥堵指数": 0.56,
          "变化": "平均速度↓7.1% 拥堵频率↑9.8% 排队长度↑9.0%"
        }
      ]
    },
    "银泽路": {
      "决策前": [
        {
          "时段": "12:00-12:30",
          "平均速度": 15.8,
          "拥堵频率": 71.3,
          "排队通过率": 158.2,
          "拥堵指数": 0.88
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 18.4,
          "拥堵频率": 63.5,
          "排队通过率": 138.7,
          "拥堵指数": 0.80
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 21.2,
          "拥堵频率": 55.1,
          "排队通过率": 120.4,
          "拥堵指数": 0.72
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 24.6,
          "拥堵频率": 47.8,
          "排队通过率": 103.9,
          "拥堵指数": 0.64
        }
      ],
      "决策后": [
        {
          "时段": "12:00-12:30",
          "平均速度": 14.3,
          "拥堵频率": 75.6,
          "排队通过率": 168.4,
          "拥堵指数": 0.92,
          "变化": "平均速度↓9.5% 拥堵频率↑6.0% 排队长度↑6.4%"
        },
        {
          "时段": "12:30-13:00",
          "平均速度": 16.7,
          "拥堵频率": 67.8,
          "排队通过率": 147.3,
          "拥堵指数": 0.84,
          "变化": "平均速度↓9.2% 拥堵频率↑6.8% 排队长度↑6.2%"
        },
        {
          "时段": "13:00-13:30",
          "平均速度": 19.3,
          "拥堵频率": 59.2,
          "排队通过率": 128.1,
          "拥堵指数": 0.76,
          "变化": "平均速度↓9.0% 拥堵频率↑7.4% 排队长度↑6.4%"
        },
        {
          "时段": "13:30-14:00",
          "平均速度": 22.4,
          "拥堵频率": 51.3,
          "排队通过率": 110.5,
          "拥堵指数": 0.68,
          "变化": "平均速度↓8.9% 拥堵频率↑7.3% 排队长度↑6.4%"
        }
      ]
    }
  }
,"决策建议":" "
}
  
    
    # 示例操作
    # hx.main_dir_structure_generator("test")
    # hx.load_title_structure_doc("test_re_doc", 'Pao')
    # pre, aft, sug = hx.load_json_doc(data_use)
    # hx.doc_json_generator([pre, aft, sug], [
    #     "test_re_doc/re_sub1/pre_decision.json",
    #     "test_re_doc/re_sub1/aft_decision.json",
    #     "test_re_doc/re_sub1/suggestion.json"
    # ])
    # hx.doc_del("test_re_doc/re_sub4")
    # hx.add_tag("xiaomi","test_re_doc/re_title.json")
    # hx.del_tag("xiaomi","test_re_doc/re_title.json")
    # hx.add_file("test_re_doc/re_title.json","dyl","ex")
    # hx.rm_file("test_re_doc/re_title.json","dyl","ex")
    