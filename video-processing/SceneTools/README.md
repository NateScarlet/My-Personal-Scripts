# Nuke自动拼色板

## 须知

默认使用nuke10.0v4 其他需要版本更改`path.ini`中的NUKE路径才能使用

## 使用方法

1. 将单帧放到`images`文件夹中
2. 运行 `拼色板.py.bat`

## 增强功能

* 将会每个镜头只保留一个修改日期最新的单帧
* 渲染完成后自动上传，将会在目标文件夹中创建当前日期命名的文件夹

     1. 设置`path.ini`中的服务器路径和文件夹路径
     2. 运行`拼色板.py.bat`
* 场集信息
     1. 设置`path.ini`中的场集信息
     2. 运行`拼色板.py.bat`
* 更换底板

   * 同目录下名称为`灯光合成模板_底板.jpg`的文件会被识别为底板
   * 无底板则会用纯黑色代替
   * 可替换为其他16:9分辨率的图像