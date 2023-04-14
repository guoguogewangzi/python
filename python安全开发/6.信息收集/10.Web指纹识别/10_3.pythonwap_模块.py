
'''
python模块方式实现
通过python-Wappalyzer模块实现：
python3 -m pip install python-Wappalyzer -i https://pypi.mirrors.ustc.edu.cn/simple/

'''
from Wappalyzer import Wappalyzer,WebPage
import json

wappalyzer = Wappalyzer.latest()
webpage = WebPage.new_from_url('https://www.hetianlab.com')
print(wappalyzer.analyze(webpage))
print(wappalyzer.analyze_with_categories(webpage))
print(json.dumps(wappalyzer.analyze_with_versions_and_categories(webpage),indent=2))
