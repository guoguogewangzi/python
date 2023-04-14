import re, random, time


def genStr():
    global sigma
    s = ""
    for i in range(32):
        s += sigma[random.randint(0, 15)]
    return s


sigma = "0123456789ABCDEF"
regex = re.compile(r'[1-2][^2-8][D-F]0+[A-F]')
count = 0
start = time.perf_counter()
match = regex.search(genStr())
while not match:
    count += 1
    match = regex.search(genStr())
print("程序匹配：猜测{}次，{}->{}".format(count, match.string, match.group(0)))
end = time.perf_counter()
print("程序用时：{:.5f}秒".format(end - start))
