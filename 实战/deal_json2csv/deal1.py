import json
import csv

# 读取 JSON 数据文件，每行一个 JSON 数据段
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield json.loads(line)

# 写入 CSV 文件
def write_to_csv(data_result, csv_file):
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data_result[0].keys())
        if file.tell() == 0:
            writer.writeheader()
        for entry in data_result:
            # 在写入之前将 id_、lid、vid 字段的值包裹在单引号中
            for key in ['id_', 'lid', 'vid','visitor_id_card']:
                if key in entry:
                    entry[key] = "'" + str(entry[key])
            writer.writerow(entry)

# JSON 数据文件路径
json_file = 'data1.json'

# CSV 文件路径
csv_file = 'data_result1.csv'

# 遍历 JSON 数据文件中的每个 JSON 数据段
for data in read_json_file(json_file):
    # 提取 dataResult 数据
    data_result = data.get('data', {}).get('dataResult', [])
    if data_result:
        # 将数据写入 CSV 文件
        write_to_csv(data_result, csv_file)

print("CSV 文件已生成:", csv_file)
