#!/usr/bin/env python
# 生成并保存了一个列出所有支持站点的 Markdown 文件 output/sites.mdx，其中站点信息是按字母顺序排列的。
# data.json 文件被重新排序并覆盖保存
import json
import os


DATA_REL_URI: str = "sherlock_project/resources/data.json"


# 读取data.json文件，data存储
with open(DATA_REL_URI, "r", encoding="utf-8") as data_file:
    data: dict = json.load(data_file)

# 删除 data 中的 $schema 键
social_networks: dict = dict(data)
social_networks.pop('$schema', None)

# 字母数字排序
social_networks: list = sorted(social_networks.items())

# 创建output目录
os.mkdir("output")

# 将支持的站点写入sites.mdx
with open("output/sites.mdx", "w") as site_file:
    site_file.write("---\ntitle: 'List of supported sites'\nsidebarTitle: 'Supported sites'\nicon: 'globe'\ndescription: 'Sherlock currently supports **400+** sites'\n---\n\n")
    for social_network, info in social_networks:
        url_main = info["urlMain"]
        is_nsfw = "**(NSFW)**" if info.get("isNSFW") else ""
        site_file.write(f"1. [{social_network}]({url_main}) {is_nsfw}\n")

# 排序原始data数据并覆盖data.json文件
with open(DATA_REL_URI, "w") as data_file:
    sorted_data = json.dumps(data, indent=2, sort_keys=True)
    data_file.write(sorted_data)
    data_file.write("\n")

print("已完成支持站点列表的更新")

