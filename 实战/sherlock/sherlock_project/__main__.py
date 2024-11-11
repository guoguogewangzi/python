#启动文件

import sys


if __name__ == '__main__':

    python_version = sys.version.split()[0]

    if sys.version_info <(3,8):
        print(f"Sherlock 需要 Python 3.8+\n 你使用的版本为{python_version},Sherlock不支持该版本")
        sys.exit(1)

    from sherlock_project import sherlock
    sherlock.main()




