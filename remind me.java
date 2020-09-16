111
222

Forward_Secrecy

echo "# Forward_Secrecy" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M master
git remote add origin https://github.com/changLifan/Forward_Secrecy.git
git push -u origin master


…or push an existing repository from the command line
git remote add origin https://github.com/changLifan/Forward_Secrecy.git
git branch -M master
git push -u origin master

1. 下载安装Git客户端
https://blog.csdn.net/ezreal_tao/article/details/81609883

Windows下TortoiseGit客户端安装到Git分支使用详细教程（非必要）
https://blog.csdn.net/hello_world_qwp/article/details/80857558


2. 配置用户名密码
git config --global user.name  ""  
git config --global user.email  "@163.com"



