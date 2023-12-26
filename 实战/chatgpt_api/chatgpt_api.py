'''
api文档：都要收费
https://platform.openai.com/docs/guides/text-generation/chat-completions-api

'''

#内置库
import os
import json

#第三方库
import openai


os.environ["HTTP_PROXY"] = "http://127.0.0.1:33210"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:33210"

#测试是否走代理
###############################
# import requests

# url = "https://jsonip.com/"

# res = requests.get(url)
# print(res.text)
###############################


def get_api_key():
    openai_key_file = '.\\openai_key.json'
    with open(openai_key_file,'r',encoding='utf-8') as f:
        openai_key = json.loads(f.read())
    return openai_key['api']

openai.api_key = get_api_key()


class ChatGPT:
    def __init__(self,user) -> None:
        self.user = user
        self.messages = [{"role":"system","content":"一个有10年Python开发经验的资深算法工程师"}]
        self.filename = "./user_messages.json"
    
    def ask_gpt(self):
        rsp = openai.ChatCompletion.create(model='gpt-3.5-turbo',messages = self.messages)
        print(rsp)
        print("----------------------------------")
        print(rsp.get("choices")[0]["message"]["content"])

        return rsp.get("choices")[0]["message"]["content"]
    
    def writeTojson(self):
        try:
            if not os.path.exists(self.filename):
                with open(self.filename,"w") as f:
                    pass
            with open(self.filename,'r',encoding='utf-8') as f:
                content = f.read()
                msgs = json.loads(content) if len(content) > 0 else {}
            msgs.update({self.user : self.messages})

            with open(self.filename,'w',encoding='utf-8') as f:
                json.dump(msgs,f)

        except Exception as e:
            print(f"错误代码：{e}")


def main():
    user = input("请输入用户名称：")
    chat = ChatGPT(user)
    while 1:
        if len(chat.messages) >=11:
            print("*")
            print("*重置*")
            print("*")

            chat.writeTojson()
            user = input("请输入用户名称：")
            chat = ChatGPT(user)
        q = input(f"请提问：【{chat.user}】")

        if q == "0":
            print("*退出*")
            chat.writeTojson()
            break
        elif q == "1":
            print("*")
            print("*重置*")
            print("*")
            chat.writeTojson()
            user = input("请输入用户名称：")
            chat = ChatGPT(user)
            continue
        chat.messages.append({"role":"user","content":q})
        answer = chat.ask_gpt()

        print(f"【ChatGPT】{answer}")

        chat.messages.append({"role":"assistant","content":answer})

if __name__ == '__main__':
    main()
