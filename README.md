# 快速下载及更新代码
```shell
快速拉取代码：git clone git@github.com:GZWSAMA/Elctronic-Design-Contest-Car.git
快速更新代码：git pull git@github.com:GZWSAMA/Elctronic-Design-Contest-Car.git
```

# 使用代码前请先安装依赖
使用本项目前，请确保通过以下命令配置虚拟环境和安装所需依赖包：
```shell
pip install virtualenv
virtualenv venv
cd ./venv/Scripts
activate
cd ../..
pip install -r requirements.txt
```
# 环境要求
python == 3.10.11

# 目录结构：
```
本项目的目录结构组织如下：
├── datas： 存放数据
├── vision： 视觉核心代码
    ├── vision_location.py：视觉定位
    ├── vision_detection.py：视觉特征匹配
```

# 快速开始
```shell
视觉定位测试：python ./vision/vision_location.py
```