#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/11 10:47
# @Author  : xiao
# @File    : image_to_txt.py
# @Software: PyCharm
# @Desc    : 图片转字符画程序
#            需提前将图片放入 files 文件夹下，运行程序后在命令行输入图片名，
#            程序会在该文件夹下生成字符画文档。
#            注意：打开的文档内，字体应该调整为宋体！不然图像尺寸会出错

from PIL import Image  # 导入图像处理包 pip install pillow
import os
import sys


def image_to_char():
    input("*** 请将需要转换的图片文件放到 files 文件夹下 ***（回车继续...）")

    # 用户输入需要转换的视频文件及参数
    image_name: str = input("请输入图片文件名（包括后缀）：")
    if image_name == '':  # 如果用户没有输入视频文件名
        print("你咋不输入文件名呢？你让我咋处理 (╬▔皿▔)╯，用爱么？")
        sys.exit()  # 退出程序

    # 文件路径处理
    now_path: str = os.getcwd()  # 获取程序当前所在文件路径
    file_path: str = now_path + "\\files"  # 图片所处文件夹的路径
    image_path: str = now_path + "\\files\\" + image_name  # 图片文件完整路径

    # 判断视频文件是否存在、是否符合格式要求
    if image_name.split('.')[-1] not in ["jpg", "png"]:
        print('你输入的文件格式不支持 ┭┮﹏┭┮')
        print("我只支持使用 jpg、png 格式的文件 =￣ω￣=")
        sys.exit()  # 退出程序
    if image_name not in [f for f in os.listdir(file_path)]:  # 遍历 files 文件夹下的所有文件名
        print("files 文件夹内没有找到这个文件，检查一下你是不是名字输错了 (⊙o⊙)？")
        sys.exit()  # 退出程序

    img_ascii = ""  # 用于保存转换后的字符
    image_resize = 0.5  # 输出的字符画图像显示倍数，默认输出图像为缩小一倍（0.5）

    # image_file = open(image_path, "rb")   # 以二进制方式打开图片
    img = Image.open(image_path)  # 导入图片，有 PIL 包就不需要上面这种方式导入图片了

    # 重新改变图片大小，防止因图片太大导致生成的字符画太大
    img = img.resize((int(img.size[0] * image_resize), int(img.size[1] * image_resize * 0.504)))
    img_gray = img.convert("L")  # 将图像转换为黑白图片

    # 字符串集
    gray_lib = list(r"""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """)

    # 对图像每个像素赋值不同的字符
    for img_y in range(0, img_gray.size[1]):  # [1]：纵向     [0]：横向
        for img_x in range(0, img_gray.size[0]):
            current_gray = img_gray.getpixel((img_x, img_y))  # 获取当前的图像灰度值
            img_ascii += gray_lib[int((len(gray_lib) * current_gray) / 256)]  # 映射

        img_ascii = img_ascii + "\n"  # 映射完一行之后换行

    # image_txt = transform(img)  # 将图像转换为字符
    create_txt = open((file_path + "\\image.txt"), "w")  # 生成结果文件
    create_txt.write(img_ascii)  # 将字符画输出到生成文件内
    create_txt.close()  # 关闭文件系统

    print("转换完成啦，文件放在 files 文件夹下了，名字叫 image.txt 哦，快去看看叭 ╰(￣ω￣ｏ)")


if __name__ == '__main__':
    image_to_char()
