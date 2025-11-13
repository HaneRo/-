# -*-  coding: utf-8 -*-

from datetime import datetime, timedelta
import re
import telebot
import serverchan
import yaml
import sys


try:
    with open("notify.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        telegram_token = config["notify"]["bot_token"]
        telegram_chat_id = config["notify"]["chat_id"]
        proxy = config["notify"]["proxy"]
        serverchan_key = config["notify"]["serverchan_key"]
        serverchan_channel = config["notify"]["serverchan_channel"]

except (FileNotFoundError, yaml.YAMLError) as e:
    print(f"配置加载失败: {str(e)}")
    sys.exit(1)

telegram_bot = telebot.TeleBot(token=telegram_token)


def readLog():
    try:
        atk_count = 0
        msg = ""
        sanity = ""  # 理智恢复提示
        drops = {}  # 存储所有掉落物品及其数量
        stages = {}  # 存储关卡信息及其次数

        # 正则表达式匹配掉落统计行
        drop_pattern = re.compile(r"^\[.*?\]\[.*?\]\[.*?\]\s*<.*?>\s*(\S+)\s+掉落统计:")
        item_pattern = re.compile(r"^(.*?)\s*:\s*([\d,]+)")
        action_pattern = re.compile(r"开始行动\s*(?:\d+\s*~\s*)?(\d+)\s*次")

        with open("./debug/gui.log", encoding="utf-8") as log:
            contents = log.readlines()

            current_stage = None  # 当前正在处理的关卡
            reading_drops = False  # 是否正在读取掉落信息
            in_refill_task = False  # 是否在刷理智任务中
            current_task_actions = 0  # 当前刷理智任务的行动次数
            start_time = None  # 任务开始时间
            current_refill_stage = None  # 当前刷理智任务的关卡
            current_task_drops = {}  # 当前刷理智任务的掉落数据
            recruits = ""  # 当前刷理智任务的招募数据

            for line in contents:
                line = line.strip()

                # 检测任务开始，重置计数
                if "开始任务: 开始前脚本" in line:
                    atk_count = 0
                    msg = ""
                    sanity = ""
                    drops = {}
                    stages = {}
                    recruits = ""
                    start_time = datetime.strptime(line[:25], "[%Y-%m-%d %H:%M:%S.%f]")

                # 检测刷理智任务开始
                if "开始任务: 刷理智" in line:
                    in_refill_task = True
                    current_task_actions = 0
                    current_task_drops = {}  # 清空当前任务的掉落数据

                # 检测刷理智任务结束
                if "完成任务: 刷理智" in line:
                    in_refill_task = False
                    atk_count += current_task_actions

                    # 将行动次数分配到对应的关卡
                    if current_refill_stage:
                        if current_refill_stage in stages:
                            stages[current_refill_stage] += current_task_actions
                        else:
                            stages[current_refill_stage] = current_task_actions

                    # 将当前任务的掉落数据合并到总掉落统计中
                    for item_name, count in current_task_drops.items():
                        if item_name in drops:
                            drops[item_name] += count
                        else:
                            drops[item_name] = count

                    # 重置当前刷理智任务的关卡和行动次数
                    current_refill_stage = None
                    current_task_actions = 0
                    current_task_drops = {}

                # 检测行动次数（只在刷理智任务中计算）
                if in_refill_task and "开始行动" in line:
                    # 使用正则表达式提取行动次数
                    action_match = action_pattern.search(line)
                    if action_match:
                        current_task_actions = int(action_match.group(1))
                    else:
                        # 如果没有匹配到范围格式，但有"开始行动"，输出提示
                        msg += ",行动次数计算错误"

                # 检测任务出错
                if "任务出错" in line:
                    msg += ",任务出错"

                # 检测公招信息
                if line.endswith("★ Tags"):
                    pattern = r"(\d+)\s*★\s*Tags"
                    match = re.search(pattern, line)
                    if match:
                        rating = int(match.group(1))
                        if rating >= 5:
                            recruits = ",发现高星干员招募！(" + str(rating) + "★)"
                            if rating > 6:
                                recruits = "招募信息错误:" + line

                # 检测理智信息
                if "理智将在" in line:
                    sanity = line

                # 检测掉落统计开始
                drop_match = drop_pattern.match(line)
                if drop_match:
                    current_stage = drop_match.group(1)
                    # 更新当前刷理智任务的关卡
                    if in_refill_task:
                        current_refill_stage = current_stage
                    reading_drops = True
                    current_task_drops = {}
                    continue

                    # 检测"当前次数"行，说明掉落统计结束
                if line.startswith("当前次数 : "):
                    reading_drops = False
                    continue

                # 如果遇到其他[开头的行，说明掉落统计结束
                if line.startswith("["):
                    reading_drops = False
                    continue

                # 如果正在读取掉落信息
                if reading_drops:
                    # 检测物品掉落
                    item_match = item_pattern.match(line)
                    if item_match:
                        item_name = item_match.group(1).strip()
                        total_count = int(item_match.group(2).replace(",", ""))

                        # 直接覆盖当前任务的掉落数据（因为这已是累计值）
                        current_task_drops[item_name] = total_count
                        continue

        # 生成掉落物品列表
        drop_list = []
        for item, count in drops.items():
            drop_list.append(f"{item}:{count}")

        # 如果还有未计算的刷理智任务，将其行动次数加到总行动次数中
        if in_refill_task:
            atk_count += current_task_actions

            # 将行动次数分配到对应的关卡
            if current_refill_stage:
                if current_refill_stage in stages:
                    stages[current_refill_stage] += current_task_actions
                else:
                    stages[current_refill_stage] = current_task_actions

        # 检查时间差
        if start_time:
            diff = datetime.now() - start_time
            threshold = timedelta(hours=2)
            if diff < threshold:
                print("时间差小于2小时")
            else:
                print("时间差大于等于2小时")
                msg += "\n！！！注意开始时间与当前时间相差2小时以上，请检查程序是否正常运行！！！"

        # 计算关卡统计总次数
        total_stage_count = sum(stages.values())

        # 如果行动次数与关卡统计不一致，将差异分配到"未知关卡"
        if atk_count != total_stage_count:
            diff = atk_count - total_stage_count
            stages["错误记录"] = diff

        # 生成关卡信息
        stage_list = []
        for stage, count in stages.items():
            stage_list.append(f"{stage}({count}次)")

        # 组合信息
        if drop_list:
            msg += ",共获取到" + "、".join(drop_list)

        if stage_list:
            msg += ",关卡:" + "、".join(stage_list)

        msg += recruits
        msg += sanity

        return "MAA操作完成，共行动" + str(atk_count) + "次" + str(msg)
    except Exception as e:
        print(f"读取日志失败: {str(e)}")
        return "读取日志失败"


msg = readLog()
print(msg)
try:
    telegram_bot.send_message(chat_id=telegram_chat_id, text=msg)
    pass
except:
    try:
        serverchan.send(key=serverchan_key, desp=msg, channel=serverchan_channel)
        pass
    except:
        print("ServerChan 发送通知失败")
    print("Telegram Bot 发送通知失败")
