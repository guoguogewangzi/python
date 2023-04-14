module_var  = 1
class module_class:
    mc_classattr = 1
    def __init__(self,mc_instattr = 1):
        self.mcinstattr = mc_instattr
    def mc_func(self):
        return "Method with a count of {}".format(self.mc_classattr)


def module_func():
    print("Module Functino")


print("Module Statement")


