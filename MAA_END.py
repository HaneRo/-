# -*-  coding: utf-8 -*-
import telebot
from datetime import datetime, timedelta
import re
bot = telebot.TeleBot("XXXXXXXXXX:XXXXXXXXXXXXXXXXXXXX")

def remove_brackets(input_string):
    output_string = re.sub(r'\([^)]*\)', '', input_string)
    return output_string.strip()

try:
    atk_count = 0
    msg=""

    with open('./debug/gui.log', encoding='utf-8') as log:
        should_read = False  # 是否开始读取标志
        lines_to_read = []  # 存储需要读取的行
        # 读取文件
        contents = log.readlines()
        for line in contents:
            line= remove_brackets(line)
            if "开始任务: Fight" in line:
                atk_count = 0
                msg=""
                start_time=datetime.strptime(line[:25], '[%Y-%m-%d %H:%M:%S.%f]')
                # print(start_time)
            if "已开始行动" in line:
                atk_count += 1
            if "任务出错" in line:
                msg+=",任务出错"
            if "<>" in line:
                # 检测到结束关键字，停止读取
                should_read = False
            if should_read:
                # 已经开始读取，将当前行添加到列表中
                lines_to_read.append(line.replace(" ", ""))

            if "掉落统计" in line:
                # 检测到起始关键字，开始读取
                should_read = True
                lines_to_read = [] 

    msg+=",共获取到"
    msg+='、'.join(lines_to_read)
    diff = datetime.now() - start_time

    # 定义时间阈值为2小时
    threshold = timedelta(hours=2)
    # 比较时间差是否小于阈值
    if diff < threshold:
        print("时间差小于2小时")
    else:
        print("时间差大于等于2小时")
        msg+="\n！！！注意开始时间与当前时间相差2小时以上，请检查程序是否正常运行！！！"
    bot.send_message(chat_id='1439363098',
                     text="MAA操作完成，共行动"+str(atk_count)+"次"+str(msg))
    print("MAA操作完成，共行动"+str(atk_count)+"次"+str(msg))
except:
    print("error")
    pass
