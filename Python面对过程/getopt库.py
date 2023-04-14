import getopt, sys

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:ve", ["distpath=", "clean"])
    for o, a in opts:
        if o == "-h":
            print("发现-h参数")
        elif o == "-v":
            print("发现-v参数")
        elif o == "-i":
            print("发现-i参数及其对应值{}".format(a))
        elif o == "--distpath":
            print("发现-distpath参数及其对应值{}".format(a))
        elif o == "--clean":
            print("发现--clean参数")
        else:
            print("发现未知参数")
except getopt.GetoptError:
    print("命令行参数解析错误")
    sys.exit(2)


