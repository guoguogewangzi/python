import os 
import argparse
from tqdm import tqdm

def logo():
    logo0 = r'''
    _______           ______  _____       ____        __ 
   / ____(_)___  ____/ / __ \/ ___/      / __ \__  __/ /_
  / /_  / / __ \/ __  / / / /\__ \______/ / / / / / / __/
 / __/ / / / / / /_/ / /_/ /___/ /_____/ /_/ / /_/ / /_  
/_/   /_/_/ /_/\__,_/\____//____/      \____/\__,_/\__/  
'''

    print(logo0)



def search_files(directory, extensions):
    files = []
    for root,_,filenames in os.walk(directory):
        for filename in filenames:
            for extension in extensions:
                if filename.endswith(extension):
                    files.append(os.path.join(root,filename))
    return files

def search_content(file_path, content):
    match_lines = []
    try:
        with open(file_path, 'r',encoding='utf-8',errors='ingnore') as file:
            for line_num , line in enumerate(file,1):
                try:
                    if content in line:
                        match_lines.append((line_num,line))
                except UnicodeDecodeError as e:
                    print(f"[-] Unicode decode error file {file_path}, line {line_num}:{e}")
                    print()
        return match_lines

    except:
        print(f"[-] Error file {file_path}")
        print()

def write_to_file(output_file,file_path,matching_lines):
    with open(output_file,'a',encoding='utf-8') as f:
        f.write(f"[+] File Path:{file_path}\n")
        f.write(f"[=] Line Rows:{len(matching_lines)}\n")
        for line_num, line in matching_lines:
            f.write(f"[~] In Line {line_num}:{line.strip()}\n")
        f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="FindOS-Out")
    parser.add_argument("-n","--name",help="文件后缀",required=True)
    parser.add_argument("-c","--content",help="搜索的文件内容",required=True)
    parser.add_argument("-o","--output",help="保存的搜索结果,默认'./findout.txt'",default="findout.txt")
    parser.add_argument("-d","--directory",help="指定目录搜索，默认'./'",default="./")
    args = parser.parse_args()

    directory = args.directory                  #目指定目录搜索
    extensions = args.name.split(',')           #文件后缀,['.txt', '.ini']
    content = args.content                      #搜索的文件内容
    output_file = args.output                   #保存的搜索结果
    
    files = search_files(directory,extensions)

    for file_path in tqdm(files,desc = "Seaching files",unit="file"):
        matching_lines = search_content(file_path,content)
        if matching_lines:
            write_to_file(output_file,file_path,matching_lines)
            

if __name__ == '__main__':
    logo()
    print("[+]开始")
    main()
    print("[+]结束！")
    


    








