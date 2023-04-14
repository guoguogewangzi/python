import requests
r = requests.get('https://api.github.com/user',\
                 auth=('user','pass'))

status=r.status_code
header=r.headers['content-type']
endoing=r.encoding
text=r.text


f = open("pachong.txt","w")
f.write(str(status))
f.write(header)
f.write(endoing)
f.write(text)

f.close()
