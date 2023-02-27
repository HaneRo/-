# -*-  coding: utf-8 -*-
from tcping import Ping
import psutil
import winreg
import os
import sys
import shutil
import requests
# ConfigFile=r"A:\Users\HaneRo\.config\clash\config.yaml"
ConfigFile=os.path.join(os.environ['USERPROFILE'], '.config','clash', 'config.yaml')
clash=os.path.join(os.getcwd(), 'clash.exe')
ui=os.path.join(os.getcwd(), 'ui')
print(ConfigFile)

def editFile(*argv):
    # if len(sys.argv) < 4:
    #     sys.exit("usage:sed.py argv[2] argv[3] file_name")

    # # 假定程序的参数是正确的
    # # 取参数赋值
    # progran_ame, argv[2], argv[3], argv[1] = sys.argv
    if len(argv) < 4:
        print("usage:sed.py argv[2] argv[3] file_name")

    # 假定程序的参数是正确的
    # 取参数赋值
    # argv[0], argv[1], argv[2], argv[3] = argv
    # print(argv[0], argv[1], argv[2], argv[3])

    if not os.path.exists(argv[1]):
        sys.exit("文件%s不存在" % argv[1])

    # 判断输入的参数是否为绝对路径， 如果是相对路径则取得绝对路径
    if os.path.isabs(argv[1]):
        src_file = argv[1]
    else:
        src_file = os.path.realpath(argv[1])

    # 将原来的文件重新命名，得到备份文件名
    src_path_name = os.path.dirname(src_file)
    src_file_name = os.path.basename(src_file)
    bak_file_name = os.path.splitext(
        src_file_name)[0]+'_bak'+os.path.splitext(src_file_name)[1]
    back_file = src_path_name+os.sep+bak_file_name

    # 备份文件
    shutil.copy(src_file, back_file)

    out_file = open(src_file, 'w', encoding='utf-8')
    # 对文件的每一行进行遍历，同时进行替换操作
    if (argv[0]=="sed"):
        with open(back_file, encoding='utf-8') as f:
            for line in f:
                out_file.writelines(line.replace(argv[2], argv[3]))
    if (argv[0]=="deleteLine"):
        with open(back_file, encoding='utf-8') as f:
            for line in f:
                if argv[2] not in line :
                    out_file.writelines(line) 
    out_file.close()


def setProxy(ProxyEnable,*ProxySetting):
    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0, winreg.KEY_ALL_ACCESS)

    def set_key(name, value):
        _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
    if (ProxyEnable):
        set_key('ProxyEnable', 1)
        try:
            print("设置代理服务器为"+ProxySetting[0])
            set_key('ProxyServer', ProxySetting[0])
        except:print("未获取到ProxyServer")
        try:
            print(ProxySetting[1])
            set_key('ProxyOverride', ProxySetting[1])  # Bypass the proxy for localhost
        except:print("未获取到ProxyOverride")
    else:
        set_key('ProxyEnable', 0)

# setProxy(True,'127.0.0.1:1080','*.local;*.xn--fcsw44g0rau46e.xn--6qq986b3xl')

def checkNet(domain,port,time=200):
    try:
        ping = Ping(domain, port, time)  # 地址、端口、超时时间
        ping.ping(1)  # ping命令执行次数
        if (ping.result.rows[0].successed==0):
            return False
        return True
    except:
        return False

def killProcess(PROC_NAME):
    for proc in psutil.process_iter():
        # check whether the process to kill name matches
        if proc.name() == PROC_NAME:
            proc.kill()

def updateConfig():
    with open("./sub.txt",encoding='utf-8')as f:
        url=f.read()
        print(url)
        open(ConfigFile,"wb").write(requests.get(url).content)
    editFile("sed",ConfigFile,"port: 7890","mixed-port: 1080") 
    editFile("sed",ConfigFile,"socks-port: 7891","secret: zero*9*9") 
    editFile("sed",ConfigFile,"log-level: info","log-level: error") 
    editFile("sed",ConfigFile,"external-controller: :9090","external-controller: :9999") 


if (checkNet("10.10.10.10",1080)):
    print ("关闭Clash，恢复网络")
    setProxy(False)
    killProcess("clash.exe")
else:
    if (checkNet("baidu.com",443)):
        try:
            print ("更新Clash配置文件")
            setProxy(False)
            killProcess("clash.exe")
            updateConfig()
            setProxy(True,"localhost:1080",'*.local;*.xn--fcsw44g0rau46e.xn--6qq986b3xl')
            os.spawnl(os.P_DETACH, clash, "clash", '-ext-ui', ui)
        except:
            print("启动失败，关闭代理")
            setProxy(False)
            killProcess("clash.exe")
    else:
        print("未连接网络，关闭Clash")
        setProxy(False)
        killProcess("clash.exe")


