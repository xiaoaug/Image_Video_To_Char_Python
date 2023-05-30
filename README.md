# 图片转字符画、视频转字符动画

程序使用 ffmpeg、OpenCV、PIL 等制作。

- 图片转字符画效果：打开项目文件 `./files/test.txt`
- 视频转字符画效果：[bilibili](https://www.bilibili.com/video/BV1ve4y197qW/)

# 需要做什么准备？

1. PIL: `pip install pillow`
2. tqdm: `pip install tqdm`
3. OpenCV: `pip install opencv-python`

# 如何运行图片转字符画程序？

1. 将需要转字符画的图片放入 files 文件夹下。
2. 运行程序：`python image_to_char.py`
3. 根据提示要求，在终端输入图片名（包括文件后缀），比如：`test.png`
4. 程序会在 files 文件夹下生成字符画 txt 文档，打开文档即可看到字符画。

⚠️注意：打开的文档内，字体应该调整为宋体！否则图像尺寸会出错，影响实际效果。


# 如何运行视频转字符动画程序？

1. 将需要转字符画的视频文件放入 files 文件夹下。
2. 运行程序：`python video_to_char.py`
3. 根据提示要求，在终端输入视频名（包括文件后缀），比如：`test.mp4`
4. 程序会在 output 文件夹下生成字符画视频文件，打开即可观看。

⚠️注意：程序运行过程中会产生大量临时文件，运行结束后会自动清除。程序运行时不要去动临时文件！

# 如何运行视频转字符动画_终端显示版本程序？

1. 将需要转字符画的视频文件放入 files 文件夹下。
2. 运行程序：`python video_to_char_terminal.py`
3. 根据提示要求，在终端输入视频名（包括文件后缀），比如：`test.mp4`
4. 即可在终端实时显示字符画视频。

⚠️注意：为了保证字符画视频的尺寸正常显示，建议使用 cmd 或者 windows terminal 运行程序，在 pycharm 中运行程序会出错！
