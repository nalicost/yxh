import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Union


class FileManager:
    """
    文件管理类，封装常见的文件和文件夹操作
    """

    def __init__(self, base_path: str = None):
        """
        初始化文件管理器

        :param base_path: 基础路径，如果不指定则使用当前工作目录
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def _get_full_path(self, path: Union[str, Path]) -> Path:
        """获取完整路径"""
        path = Path(path)
        return self.base_path / path if not path.is_absolute() else path

    def exists(self, path: str) -> bool:
        """检查文件或目录是否存在"""
        return self._get_full_path(path).exists()

    def is_file(self, path: str) -> bool:
        """检查是否是文件"""
        return self._get_full_path(path).is_file()

    def is_dir(self, path: str) -> bool:
        """检查是否是目录"""
        return self._get_full_path(path).is_dir()

    def create_file(self, file_path: str, content: str = "", overwrite: bool = False) -> bool:
        """
        创建文件

        :param file_path: 文件路径
        :param content: 文件内容
        :param overwrite: 是否覆盖已存在文件
        :return: 是否创建成功
        """
        full_path = self._get_full_path(file_path)
        if full_path.exists() and not overwrite:
            return False

        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    def read_file(self, file_path: str) -> str:
        """读取文件内容"""
        full_path = self._get_full_path(file_path)
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def append_to_file(self, file_path: str, content: str) -> None:
        """追加内容到文件"""
        full_path = self._get_full_path(file_path)
        with open(full_path, 'a', encoding='utf-8') as f:
            f.write(content)

    def copy_file(self, src_path: str, dest_path: str, overwrite: bool = False) -> bool:
        """
        复制文件

        :param src_path: 源文件路径
        :param dest_path: 目标文件路径
        :param overwrite: 是否覆盖已存在文件
        :return: 是否复制成功
        """
        src = self._get_full_path(src_path)
        dest = self._get_full_path(dest_path)

        if not src.exists():
            return False
        if dest.exists() and not overwrite:
            return False

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        return True

    def move_file(self, src_path: str, dest_path: str, overwrite: bool = False) -> bool:
        """
        移动/重命名文件

        :param src_path: 源文件路径
        :param dest_path: 目标文件路径
        :param overwrite: 是否覆盖已存在文件
        :return: 是否移动成功
        """
        src = self._get_full_path(src_path)
        dest = self._get_full_path(dest_path)

        if not src.exists():
            return False
        if dest.exists() and not overwrite:
            return False

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(src, dest)
        return True

    def delete_file(self, file_path: str) -> bool:
        """
        删除文件

        :return: 是否删除成功
        """
        full_path = self._get_full_path(file_path)
        if not full_path.exists():
            return False
        os.remove(full_path)
        return True

    def create_dir(self, dir_path: str, parents: bool = True, exist_ok: bool = True) -> bool:
        """
        创建目录

        :param dir_path: 目录路径
        :param parents: 是否创建父目录
        :param exist_ok: 如果目录已存在是否忽略
        :return: 是否创建成功
        """
        full_path = self._get_full_path(dir_path)
        try:
            full_path.mkdir(parents=parents, exist_ok=exist_ok)
            return True
        except:
            return False

    def list_dir(self, dir_path: str = "", recursive: bool = False) -> List[str]:
        """
        列出目录内容

        :param dir_path: 目录路径
        :param recursive: 是否递归列出
        :return: 文件/目录列表
        """
        full_path = self._get_full_path(dir_path)
        if recursive:
            return [str(p.relative_to(self.base_path))
                    for p in full_path.rglob('*')]
        return [str(p.relative_to(self.base_path))
                for p in full_path.glob('*')]

    def copy_dir(self, src_dir: str, dest_dir: str, overwrite: bool = False) -> bool:
        """
        复制目录

        :param src_dir: 源目录路径
        :param dest_dir: 目标目录路径
        :param overwrite: 是否覆盖已存在目录
        :return: 是否复制成功
        """
        src = self._get_full_path(src_dir)
        dest = self._get_full_path(dest_dir)

        if not src.exists():
            return False
        if dest.exists() and not overwrite:
            return False

        shutil.copytree(src, dest, dirs_exist_ok=overwrite)
        return True

    def delete_dir(self, dir_path: str, recursive: bool = False) -> bool:
        """
        删除目录

        :param dir_path: 目录路径
        :param recursive: 是否递归删除非空目录
        :return: 是否删除成功
        """
        full_path = self._get_full_path(dir_path)
        if not full_path.exists():
            return False

        if recursive:
            shutil.rmtree(full_path)
        else:
            full_path.rmdir()
        return True

    def get_file_size(self, file_path: str) -> int:
        """获取文件大小(字节)"""
        full_path = self._get_full_path(file_path)
        return full_path.stat().st_size

    def get_modify_time(self, path: str) -> datetime:
        """获取最后修改时间"""
        full_path = self._get_full_path(path)
        return datetime.fromtimestamp(full_path.stat().st_mtime)

    def change_permissions(self, path: str, mode: int) -> bool:
        """
        修改文件/目录权限

        :param path: 路径
        :param mode: 权限模式，如0o755
        :return: 是否修改成功
        """
        full_path = self._get_full_path(path)
        try:
            full_path.chmod(mode)
            return True
        except:
            return False

    def search_files(self, pattern: str, recursive: bool = True) -> List[str]:
        """
        搜索文件

        :param pattern: 匹配模式，如"*.txt"
        :param recursive: 是否递归搜索
        :return: 匹配的文件列表
        """
        if recursive:
            return [str(p.relative_to(self.base_path))
                    for p in self.base_path.rglob(pattern) if p.is_file()]
        return [str(p.relative_to(self.base_path))
                for p in self.base_path.glob(pattern) if p.is_file()]