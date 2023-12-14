import re
import csv

# 日志文件路径
log_file_path = '228nginx.txt'

# CSV文件保存路径
csv_file_path = '228nginx.csv'

# 用于匹配日志中的各个字段的正则表达式
log_pattern = re.compile(r'^(\S+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" "(.*?)"$')

# 打开日志文件和CSV文件
with open(log_file_path, 'r') as log_file, open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # 写入CSV文件标题行
    csv_writer.writerow(['IP', 'Timestamp', 'HTTP_Method', 'Request_Path', 'HTTP_Status', 'Response_Size', 'Referer', 'User_Agent', 'Server_IP'])
    
    # 逐行处理日志文件
    for line in log_file:
        match = log_pattern.match(line)
        if match:
            ip, timestamp, request, status, size, referer, user_agent, server_ip = match.groups()
            
            # 提取请求路径中的{id}
            request_path = re.sub(r'\{.*?\}', '', request.split()[1])
            
            # 将数据写入CSV文件
            csv_writer.writerow([ip, timestamp, request.split()[0], request_path, status, size, referer, user_agent, server_ip])

print("日志处理完成，已保存为CSV文件。")
