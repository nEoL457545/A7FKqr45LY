# 代码生成时间: 2025-09-14 08:47:16
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image

"""
图片尺寸批量调整器组件
提供批量调整图片尺寸的功能
"""

class ImageResizer:
    """
    图片尺寸批量调整器
    """
    def __init__(self, storage, path):
        """
        初始化图片尺寸批量调整器
        :param storage: 文件存储系统
        :param path: 图片文件路径
        """
        self.storage = storage
        self.path = path

    def resize_images(self, new_size):
        """
        批量调整图片尺寸
        :param new_size: 目标尺寸（例如：(300, 200)）
        :return: None
        """
        try:
            # 获取图片文件列表
            image_files = self.get_image_files()

            # 遍历图片文件
            for image_file in image_files:
                # 打开图片文件
                with Image.open(image_file) as img:
                    # 调整图片尺寸
                    img = img.resize(new_size, Image.ANTIALIAS)

                    # 生成新的文件名
                    new_file_name = self.generate_new_file_name(image_file)

                    # 保存图片文件
                    self.save_image(img, new_file_name)

        except Exception as e:
            # 错误处理
            print(f"Error resizing images: {e}")

    def get_image_files(self):
        """
        获取图片文件列表
        :return: 图片文件列表
        """
        # 获取目录下所有文件
        files = os.listdir(self.path)

        # 过滤图片文件
        image_files = [file for file in files if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        return [os.path.join(self.path, file) for file in image_files]

    def generate_new_file_name(self, file):
        """
        生成新的文件名
        :param file: 原始文件名
        :return: 新的文件名
        """
        # 分割文件名和扩展名
        name, ext = os.path.splitext(file)

        # 生成新的文件名
        new_file_name = name + '_resized' + ext

        return new_file_name

    def save_image(self, img, file_name):
        """
        保存图片文件
        :param img: 图片对象
        :param file_name: 文件名
        :return: None
        "