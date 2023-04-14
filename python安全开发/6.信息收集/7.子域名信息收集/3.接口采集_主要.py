# #fofa,shodan,zoomeyes

'''
shodan,接口
SHODAN_API_KEY = "3CHq7AkQRBecviizC8CwTOn0xtrgmjGD"   #自己的
'''
import shodan

# KEY='3CHq7AkQRBecviizC8CwTOn0xtrgmjGD'
# api = shodan.Shodan(KEY)
# res = api.search('title="EG易网关"')
# #print(res)
# subdomain = [x["hostnames"] for  x in res["matches"]]
# print(subdomain)

SHODAN_API_KEY = "v3eQEl5MAavEqyY4CXAUsYfKeaX8uMyZ"
api = shodan.Shodan(SHODAN_API_KEY)
file_object = open(r'F:\python study\project\poc or exp\targets.txt', 'w')
try:
    cmd='title="EG易网关"'
    results = api.search(cmd)
    print ('Results found: %s' % results['total'])
    for result in results['matches']:         
            file_object.writelines(result['ip_str']+':'+ str(result['port']) +'\n')
except shodan.APIError as e:
    print ('Error: %s' % e)
file_object.close()

'''
fofa接口
'''

#"https://fofa.so/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={}"

# import requests
# import base64


# FOFA_EMAIL = 'om2bg0ey9wfmdtaz1yhruk4so1f0@open_wechat'
# FOFA_KEY = '1e3c0fafac33e251dbc603ed9741e1e2'

# cmd = 'app="齐治科技-堡垒机"'
# #cmd='domain="baidu.com"'
# q = base64.b64encode(cmd.encode()).decode()
# res = requests.get(f'https://fofa.so/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={q}&size=10000')

# #print(res.text)
# #print(res.json()['results'])

# for i in res.json()['results']:
#     print(i[0])

# print(len(res.json()['results']))

# with open('targets.txt','w',encoding='utf-8') as f:
#     for i in res.json()['results']:
#         f.write(i[0]+'\n')