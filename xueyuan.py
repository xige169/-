
import requests
import json

res = requests.get('http://aqjy.hfut.edu.cn/addons/rexam/user/group')
content = res.text
content_dict = json.loads(content)

data = content_dict.get('data')

academys = []

for i in data:
    name = i.get('name')
    academys.append(name)


my_academy = ''
my_id = ''
my_name = ''

#24-25学年第二学期期末考试
#期末考试
#第七届国家安全知识竞赛
examine = ''


