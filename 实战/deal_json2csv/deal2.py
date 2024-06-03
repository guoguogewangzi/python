import json
import csv

# 从文件中读取 JSON 数据
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data.get('data', {})

# 将数据写入 CSV 文件
def write_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['ID', 'Name', 'Mobile', 'Photo', 'Email'])
        writer.writeheader()
        for key, value in data.items():
            writer.writerow({
                'ID': key,
                'Name': value.get('name', ''),
                'Mobile': value.get('mobile', ''),
                'Photo': value.get('photo', ''),
                'Email': value.get('email', '')
            })

# JSON 数据文件路径
json_file = 'data2.json'

# CSV 文件路径
csv_file = 'data_result2.csv'

# 读取 JSON 数据
data = read_json_file(json_file)

# 将数据转换为 CSV 格式并写入文件
write_to_csv(data, csv_file)

print("CSV 文件已生成:", csv_file)
