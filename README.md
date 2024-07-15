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
    ├── vision_location_point.py：视觉点定位
    ├── vision_detection_SIFT.py：视觉SIFT特征匹配
    ├── vision_detection_coutour.py：视觉Contour特征匹配
    ├── vision_location_line.py：视觉边线定位
```

# 快速开始
```shell
视觉边线定位测试：python ./vision/vision_location_line.py #已弃用,原因：效率低，易受干扰
视觉SIFT特征匹配测试：python ./vision/vision_detection_SIFT.py #已弃用，原因：效率低，易受干扰
视觉点定位测试：python ./vision/vision_location_point.py
视觉Contour特征匹配测试：python ./vision/vision_detction_coutour.py
```