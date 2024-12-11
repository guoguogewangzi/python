启动方式一:
执行sherlock_project文件夹下的__main__.py，参数在launch.json



启动方式二：
方法一：
1.安装 pipx：
python3 -m pip install --user pipx


2.将pipx添加到PATH
python3 -m pipx ensurepath
路径：C:\Users\ThinkBook\AppData\Roaming\Python\Python312\Scripts\

3.安装 Sherlock
pipx install sherlock-project

4.添加到PATH
自动：python3 -m pipx ensurepath
手动：C:\Users\ThinkBook\.local\bin\

5.验证，开启新cmd，输入：sherlock -h

方法二：（安装依赖）
如果有 pyproject.toml 文件：
python3 -m pip install .

手动安装torrequest：
python3 -m pip install torrequest

-------------------------------------------------------------------------
其他：
1）pipx安装路径：
系统范围安装（无 --user）：
C:\Program Files\PythonX.Y\Scripts\pipx.exe（其中 X.Y 是 Python 的版本号）

用户范围安装（加上 --user）：
C:\Users\ThinkBook\AppData\Roaming\Python\Python312\Scripts\pipx.exe

2）pipx的用户目录，包含安装的 Python 应用程序、虚拟环境等
C:\Users\ThinkBook\pipx



