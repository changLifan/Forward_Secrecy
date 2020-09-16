1. 安装软件的命令
sudo apt-get update
sudo apt-get install XXXXX


2. 查看Java版本
java -version


3. 将文件分割：
split mylog(filename) -l 1000(linenum)


4. 将 a.txt b.txt 的文件中的内容合并到c.txt文本中
cat a.txt b.txt > c.txt


5. Geany 安装
sudo apt-get install geany


6. 打log
logcat grep | ""


7. 显示隐藏文件夹
Ctrl + H


8. 环境配置
git config --global user.name "Your Name"
git config --global user.email Your_email@gm.com
使用XXXXX邮箱生成公钥 : ssh-keygen -t rsa -C XXXXX邮箱
将公钥添加到gerrit上面 : 修改.ssh/config文件将以下:


9.  连接设备的三种方式：
    （1）使用网线(网口)连接设备：
        adb connect 192.168.1.100
        adb shell 


    （2）使用小板子加上串口链接设备
        首先配置minicom(ttyUSB2)
        sudo minicom


    （3）USB线连接设备


10.  获得root权限：
    获得root权限：su 或者 adb root
    退出root权限： ctrl + C


11.  





















