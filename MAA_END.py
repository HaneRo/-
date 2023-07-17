# -*-  coding: utf-8 -*-

from datetime import datetime, timedelta
import re
import telebot
import serverchan


telegram_bot = telebot.TeleBot("XXXXXXXX:XXXXXXXXXX")
telegram_chat_id = XXXXXXXXXX
serverchan_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
serverchan_channel = '9'


def readLog():
    try:
        atk_count = 0
        msg = ""
        getlist = ""
        counts = {}
        with open('./debug/gui.log', encoding='utf-8') as log:
            should_read = False  # 是否开始读取标志
            lines_to_read = []  # 存储需要读取的行
            # 读取文件
            contents = log.readlines()
            for line in contents:
                line = re.sub(r'\([^)]*\)', '', line).strip()
                if "开始任务: 开始前脚本" in line:
                    atk_count = 0
                    msg = ""
                    getlist = ""
                    lines_to_read = []
                    counts = {}
                    start_time = datetime.strptime(
                        line[:25], '[%Y-%m-%d %H:%M:%S.%f]')
                # if "开始任务: Fight" in line:
                #     print("开始任务")
                if "完成任务: Fight" in line:
                    for item in lines_to_read:
                        key, value = item.split(':')
                        if key in counts:
                            counts[key] += int(value)
                        else:
                            counts[key] = int(value)
                if "已开始行动" in line:
                    atk_count += 1
                if "任务出错" in line:
                    msg += ",任务出错"
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

        result = [f'{key}:{value}' for key, value in counts.items()]
        print(counts)
        getlist += '、'.join(result)
        if len(getlist) != 0:
            msg += ",共获取到"
        msg += getlist

        diff = datetime.now() - start_time
        # 定义时间阈值为2小时
        threshold = timedelta(hours=2)
        # 比较时间差是否小于阈值
        if diff < threshold:
            print("时间差小于2小时")
        else:
            print("时间差大于等于2小时")
            msg += "\n！！！注意开始时间与当前时间相差2小时以上，请检查程序是否正常运行！！！"
        return "MAA操作完成，共行动"+str(atk_count)+"次"+str(msg)
    except:
        print("读取日志失败")
        return "读取日志失败"


msg = readLog()
print(msg)
try:
    telegram_bot.send_message(chat_id=telegram_chat_id, text=msg)
except:
    try:
        serverchan.send(key=serverchan_key, desp=msg,
                        channel=serverchan_channel)
    except:
        print("ServerChan 发送通知失败")
    print("Telegram Bot 发送通知失败")
