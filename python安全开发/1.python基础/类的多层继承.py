class Earch:
    e1='地球人'
    def run(self):
        print("三维")



class Chinese(Earch):
    c1='中国人'
    def run1(self):
        print('勤奋')


class Sichaun(Chinese):
    s1='四川人'
    def run2(self):
        print('吃辣')

sichuan=Sichaun()
print(sichuan.s1)
print(sichuan.c1)
print(sichuan.e1)
sichuan.run()
sichuan.run1()
sichuan.run2()