# -*-  coding: utf-8 -*-
import os
import time
import re
from datetime import datetime,timedelta 
from telethon import TelegramClient, events, sync
if ((os.environ.get('api_id'))is None) |((os.environ.get('api_hash'))is None): 
    api_id =  XXXXX
    api_hash = 'XXXXX'
else:
    api_id =  os.environ.get('api_id')
    api_hash = os.environ.get('api_hash')


session_name = "id_" + str(api_id)
client = TelegramClient(session_name, api_id, api_hash)
client.start()

client.send_message("@yyjc_checkin_bot", "/checkin") #第一项是机器人工D,第二项是发送的文字
time.sleep(5) #延时5秒，等待机嘉人回应(一般是秒回应，但也有发生阻塞的可能)
messages = client. get_messages("@yyjc_checkin_bot") 

text=messages[0].text


# text = "您可以在北京时间 2023/04/29 17:40:26 后进行下一次签到"
match = re.search(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}', text)
if match:
    time_str = match.group()
    target_time = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')

else:
    print('未找到时间')
    target_time = datetime.now()
target_time = target_time + timedelta(minutes=1)
output_str = target_time.strftime('%M %H %d %m') + " * ID=345 task yyjc_checkin_bot.py\n"
print(output_str)
with open("/etc/crontabs/root", "r") as f:
    lines = f.readlines()

with open("/etc/crontabs/root", "w") as f:
    for line in lines:
        if "task yyjc_checkin_bot.py" not in line:
            f.write(line)
        else:
            f.write(output_str)


client. send_read_acknowledge("@yyjc_checkin_bot") #将机器人回应设为己读
print("Done! Session name:", session_name)
os._exit(0)

