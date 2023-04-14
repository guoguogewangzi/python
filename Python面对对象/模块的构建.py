"这是模块描述"
class module_class:
    mc_classattr = 1
    def __init__(self,mc_instattr = 1):
        self.mc_instattr = mc_instattr
    def mc_func(self):
        return "Method with a count of {}".format(self.mc_classattr)

if __name__=="__main__":
    import sys                                  #测试库放入 __name ==__main__：为了区分
    mc = module_class(sys.argv[1])
    print("Module Statement")
    print(mc.mc_func())
    print(mc.mc_instattr)