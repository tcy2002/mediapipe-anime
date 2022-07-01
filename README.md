# Mediapipe-Anime

## 目标

根据用户的面部动作生成同步的虚拟形象，并生成虚拟摄像头。目前仅为初步设计，在视频效果、帧率、硬件资源消耗等各方面有所欠缺，将在后续逐步改进完善。

## 算法思路

**面部捕捉**：使用mediapipe对摄像头捕捉到的视频信息进行处理，获取面部的关键点位置信息（landmarks）。

**数据处理**：设计算法将landmarks坐标信息转换为面部动作参数，包括：

* 头部旋转角度（x, y, z)；
* 眼睛开闭程度（左，右）；
* 瞳孔位置（水平方向）；
* 嘴部开闭程度；

其中眉毛形态、竖直方向的瞳孔位置的算法效果不佳，暂时不予考虑。

**虚拟形象构建**：采用文档中所给的`talking-head-anime-2-demo`模型，将经过处理之后的动作数据传入神经网络，根据给定的人物图片，生成相应的动作形象。

**虚拟摄像头**：使用`Unity Capture`生成虚拟摄像头，并通过`pyvirtualcam`库将视频流传入虚拟摄像头。

**软件集成**：最终使用pyinstaller打包为可执行文件供web端调用，后续也可以采用wxpython或opencv增加图形界面以支持客户端的其他功能。

## 模型
神经网络模型文件下载地址：[anime-model](https://jbox.sjtu.edu.cn/l/31zMzF) （交大云盘）

## 使用方法
启动程序后，会自动创建名为VirtualCamera的虚拟摄像头，若视频仍无法正常显示，需要手动运行`/vc/Install.bat`，运行成功后可在web端或其他视频软件调用。

若直接运行此项目，将模型文件的文件夹data直接放在项目文件夹下。
也可通过`pyinstaller`打包为可执行项目包：
```angular2html
pip install pyinstaller
pyinstaller -D -w -n "mediapipe-anime" main.py
```

## 硬件要求
`talking-head-anime-2-demo`项目所给的硬件配置建议：Nvidia RTX 2080，RTX 3080 or better \
本机显卡为GTX 1650Ti，测试略显吃力，暂时见鬼

## 依赖
`talking-head-anime-2-demo`：
* Python >= 3.8
* PyTorch >= 1.7.1 with CUDA support
* SciPY >= 1.6.0
* Matplotlib >= 3.3.4

其他依赖：
* numpy >= 1.19.2 
* opencv-python >= 4.6.0.66 
* mediapipe >= 0.8.10.1 
* pyvirtualcam >= 0.9.1

建议使用conda+pip配置环境