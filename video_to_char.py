#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 22:31
# @Author  : xiao
# @File    : video_to_char.py
# @Software: PyCharm
# @Desc    : 视频文件转字符画
#            注意: 需要把视频文件放入 files 文件夹内，程序运行过程中会产生大量临时文件，
#                  运行结束后会自动清除，不要去动临时文件！

import os
import sys
from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm  # 进度条
import time


def main():
    """主程序"""

    input("*** 请将需要转换的视频文件放到 files 文件夹下 ***（回车继续...）")

    # 用户输入需要转换的视频文件及参数
    video_name: str = input("请输入视频文件名（包括后缀）：")
    if video_name == '':  # 如果用户没有输入视频文件名
        print("你咋不输入文件名呢？你让我咋处理 (╬▔皿▔)╯，用爱么？")
        sys.exit()
    compress = input("请输入视频压缩倍数（整数，默认为 2，越大视频越模糊）：")
    if compress.isdigit() is False:  # 如果用户输入的不是整数
        print("你输入的不是整数，我生气气了 (* ￣︿￣)   不理你了！")
        sys.exit()
    if compress == "":  # 用户没有填压缩倍数
        print("你没填压缩倍数，那我默认给 2 了，效果不好别怪我 ￣へ￣")
        compress = 2  # 默认给 2
    compress = int(compress)  # 将压缩倍数转成整型

    # 文件路径处理
    now_path: str = os.getcwd()  # 获取程序当前所在文件路径
    file_path: str = now_path + "\\files"  # 视频所处文件夹的路径
    video_path: str = now_path + "\\files\\" + video_name  # 视频文件完整路径
    output_path: str = now_path + "\\output"  # 最终生成文件的路径

    # 判断视频文件是否存在、是否符合格式要求
    if video_name.split('.')[-1] not in ["mp4", "flv", "avi", "mpg", "wmv"]:
        print('你输入的文件格式不支持 ┭┮﹏┭┮')
        print("我只支持使用 mp4、flv、avi、mpg、wmv 格式的文件 =￣ω￣=")
        sys.exit()  # 退出程序
    if video_name not in [f for f in os.listdir(file_path)]:  # files 文件夹下的所有文件名
        print("files 文件夹内没有找到这个文件，检查一下你是不是名字输错了 (⊙o⊙)？")
        sys.exit()

    # 如果没有 output 相关的文件夹，则创建文件夹
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not os.path.exists(f'{output_path}\\temp_pic'):  # 临时图片文件夹
        os.mkdir(f'{output_path}\\temp_pic')
    if not os.path.exists(f'{output_path}\\temp_thumb'):  # 临时缩略图文件夹
        os.mkdir(f'{output_path}\\temp_thumb')
    if not os.path.exists(f'{output_path}\\temp_music'):  # 临时背景音乐文件夹
        os.mkdir(f'{output_path}\\temp_music')
    if not os.path.exists(f'{output_path}\\temp_ascii'):  # 临时字符画图像文件夹
        os.mkdir(f'{output_path}\\temp_ascii')

    # 调用ffmpeg命令获取视频中的音乐
    print("开始提取视频背景音乐...")
    time.sleep(1)  # 等待一秒
    command = f"{now_path}/tool/ffmpeg -i {video_path} -f mp3 {output_path}\\temp_music\\out.mp3"
    os.system(command)
    time.sleep(1)  # 等待一秒
    print("背景音乐提取成功！")

    # 视频转图片，按每一帧分割成图片，调用ffmpeg命令实现视频转为图片 fps=25
    print("视频开始分割成图片...")
    time.sleep(1)  # 等待一秒
    command = f"{now_path}/tool/ffmpeg -i {video_path} -r 25 -f image2 {output_path}\\temp_pic\\image-%1d.jpg"
    os.system(command)
    time.sleep(1)  # 等待一秒
    print('视频转图片成功！')

    # 生成缩略图，改变图像尺寸大小，加快转字符画的速度
    print("开始生成缩略图...")
    time.sleep(1)  # 等待一秒
    pics_list = sorted(os.listdir(f'{output_path}\\temp_pic'))
    for picture in tqdm(pics_list):  # 对每张图片进行操作
        base_name = os.path.basename(picture)  # 提取该图片的图片名
        img = Image.open(os.path.join(f'{output_path}\\temp_pic\\', picture))  # 打开图片
        img_width, img_height = img.size
        size = img_width//compress, img_height//compress  # 缩略图的尺寸
        img.thumbnail(size)  # 改变图片尺寸大小，使用默认的压缩算法
        img.save(os.path.join(f'{output_path}\\temp_thumb\\', base_name))  # 保存缩略图
    time.sleep(1)  # 等待一秒
    print("缩略图生成成功！")

    # 生成字符画
    print("开始生成字符画...")
    time.sleep(1)  # 等待一秒
    symbols = list(r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")  # 灰阶值越大，取越后面的字符
    pics_list = sorted(os.listdir(f'{output_path}\\temp_thumb'))
    for picture in tqdm(pics_list):  # 对每张图片进行操作
        # 将图片转成灰度图
        img = Image.open(os.path.join(f'{output_path}\\temp_thumb', picture)).convert('L')
        (x_size, y_size) = img.size  # 获取图像宽、高
        pixels = list(img.getdata())  # 把图片的像素信息摊平到一维，搞成一个特征向量的形式
        img.close()

        # 生成字符画图片，将灰度图每一个像素点替换成字符
        scale = compress  # 长宽扩大倍数 默认 4
        border = 0  # 边框宽度
        interval_pixel = 2  # 原图片间隔多少个像素点来填充，使图片看起来不密集，提高转化时间
        # img = Image.new('L', (x_size * scale + 2 * border, y_size * scale + 2 * border), 255)  # 新建画布
        img = Image.new('L', (x_size * scale, y_size * scale), 255)  # 新建画布
        font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', int(scale * 3))  # 调用系统字体
        draw = ImageDraw.Draw(img)
        x_border = border
        y_border = border
        for j in range(0, y_size, interval_pixel):  # 遍历图像的行
            for i in range(0, x_size, interval_pixel):  # 遍历图像的列
                draw.text(xy=(x_border, y_border),
                          text=symbols[int(pixels[j * x_size + i] / 256 * len(symbols))],
                          font=font, fill=0)
                x_border += scale * interval_pixel
            x_border = border
            y_border += scale * interval_pixel
        img.save(os.path.join(f'{output_path}\\temp_ascii', picture), "JPEG")  # 将所有替换后的字符画成一幅字符画
    time.sleep(1)  # 等待一秒
    print("字符画生成成功！")

    # 字符画合成视频
    print("开始合成视频文件...")
    time.sleep(1)  # 等待一秒
    output_name = os.path.join('ascii_' + video_name)
    # 调用ffmpeg命令实现图片转为视屏
    command = f"{now_path}/tool/ffmpeg -i {output_path}\\temp_ascii\\image-%1d.jpg {output_path}/NoMusic_{output_name}"
    os.system(command)
    time.sleep(1)  # 等待一秒
    print("视频文件合成成功！")

    # 背景音乐合成进视频
    print("开始合成音频...")
    time.sleep(1)  # 等待一秒
    command = f"{now_path}/tool/ffmpeg -i {output_path}\\temp_music\\out.mp3 -i {output_path}/NoMusic_{output_name} {output_path}/{output_name}"
    os.system(command)
    time.sleep(1)  # 等待一秒
    print("音频合成成功！")

    # 删除临时文件夹（生成的临时图片、字符画、音乐等）
    print("开始清除缓存...")
    time.sleep(1)  # 等待一秒
    for temp_pic in [f for f in os.listdir(f'{output_path}\\temp_pic')]:
        os.remove(f'{output_path}\\temp_pic\\{temp_pic}')
    for temp_thumb in [f for f in os.listdir(f'{output_path}\\temp_thumb')]:
        os.remove(f'{output_path}\\temp_thumb\\{temp_thumb}')
    for temp_ascii in [f for f in os.listdir(f'{output_path}\\temp_ascii')]:
        os.remove(f'{output_path}\\temp_ascii\\{temp_ascii}')
    for temp_music in [f for f in os.listdir(f'{output_path}\\temp_music')]:
        os.remove(f'{output_path}\\temp_music\\{temp_music}')
    os.rmdir(f'{output_path}\\temp_pic')
    os.rmdir(f'{output_path}\\temp_thumb')
    os.rmdir(f'{output_path}\\temp_music')
    os.rmdir(f'{output_path}\\temp_ascii')
    print("缓存清除完成！")
    time.sleep(1)
    print("转换完成啦，视频文件给你放在 output 文件夹中了，快去看看吧 =￣ω￣=")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户主动退出程序")
