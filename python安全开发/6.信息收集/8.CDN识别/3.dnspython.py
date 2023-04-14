import dns.resolver


domain = 'www.taobao.com'
cname = dns.resolver.resolve(domain,'CNAME')
print(cname.response.answer)
for  i in cname.response.answer:
    for j in i.items:
        print(j)
        print(type(j))
        print(j.to_text())
        print(type(j.to_text()))

