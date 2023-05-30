#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/12 13:00
# @Author  : xiao
# @File    : video_to_char_terminal.py
# @Software: PyCharm
# @Desc    : 视频转字符画程序终端显示版本
# #          需提前将视频放入 files 文件夹下，在终端运行程序后，
#            在命令行输入视频名，程序会在该终端内显示字符动画。

# ---------------------------------------------------------------------
# 下载 opencv 库时，遇到了下载出错的问题。
# 调用中科大源下载：
# pip install opencv-python -i https://pypi.mirrors.ustc.edu.cn/simple
#
# 当然安装完毕后，调用该库时，会出现不显示 cv2 成员函数的问题，软件会提示没有这
# 个函数，解决方法如下：
# 终端里输入： python -c "import cv2; print(cv2.__path__)"
# 会告诉你 cv2 文件的路径，然后打开这个路径，进入到 cv2 的文件夹下，把 cv2.pyd 这个
# 文件复制一份到它的上一级文件夹内就行了，重启 pycharm 即可解决问题。
# ---------------------------------------------------------------------

import cv2  # opencv 计算机视觉，用于读取视频：pip install opencv-python
import os
import time
import numpy
import sys


def video_to_ascii_terminal():
    input("*** 请将需要转换的视频文件放到files文件夹下 ***（回车继续...）")

    # 用户输入需要转换的视频文件及参数
    video_name: str = input("请输入视频文件名（包括后缀）：")
    if video_name == '':  # 如果用户没有输入视频文件名
        print("你咋不输入文件名呢？你让我咋处理 (╬▔皿▔)╯，用爱么？")
        sys.exit()

    # 文件路径处理
    now_path: str = os.getcwd()  # 获取程序当前所在文件路径
    file_path: str = now_path + "\\files"  # 视频所处文件夹的路径
    video_path: str = now_path + "\\files\\" + video_name  # 视频文件完整路径

    # 判断视频文件是否存在、是否符合格式要求
    if video_name.split('.')[-1] not in ["mp4", "flv", "avi", "mpg", "wmv"]:
        print('你输入的文件格式不支持 ┭┮﹏┭┮')
        print("我只支持使用 mp4、flv、avi、mpg、wmv 格式的文件 =￣ω￣=")
        sys.exit()  # 退出程序
    if video_name not in [f for f in os.listdir(file_path)]:  # files文件夹下的所有文件名
        print("files 文件夹内没有找到这个文件，检查一下你是不是名字输错了 (⊙o⊙)？")
        sys.exit()

    video = cv2.VideoCapture(video_path)  # 读取视频文件

    # 字符串集
    gray_lib = list(r"""$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """)

    print('我要开始工作咯 (～o￣3￣)～')
    time.sleep(2)  # 等待两秒，防止用户看不到上面的print
    os.system("cls")  # 将终端清屏，方便演示

    # 循环读取、播放视频每一帧，直到视频结束
    # video.isOpened 判断是否能够读取到文件
    while True:
        success, frame = video.read()  # 读取视频每一帧，success 表示读取成功，frame 为当前帧图像

        # 如果视频没读取到，或者读取完成，则退出循环
        if not success:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 当前帧图像转换成灰度图 0~255
        terminal_size = os.get_terminal_size()  # 获取终端窗口的大小
        resize_frame = cv2.resize(gray_frame, (terminal_size.columns, terminal_size.lines))  # 调整当前帧的尺寸
        frame_array = numpy.array(resize_frame, "f")  # 转换成浮点数，方便后面调用灰度值
        ascii_frame = ""  # 存储每一帧的图像

        for line in frame_array:  # 从第一行开始挨个赋灰度值
            for columns in line:  # 此时，columns 保存了该行的灰度值
                gray_num = int((len(gray_lib) - 1) * columns / 255)  # 计算灰度值用哪个字符串
                ascii_frame += gray_lib[gray_num]  # 取出字符串，赋值给最终图形

        print(ascii_frame)  # 输出图像
        time.sleep(0.01)  # 让程序停止（秒），防止字符画视频播放太快

    video.release()  # 程序结束后，将文件释放掉
    print('\n我播放完成了哦 bye~ ╰(￣ω￣ｏ)')


if __name__ == '__main__':
    try:
        video_to_ascii_terminal()
    except KeyboardInterrupt:
        print("\n用户主动退出程序")
