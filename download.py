# -*- encoding: utf-8 -*-

from FanQieNovelReptile import *

import os
import sys
if len(sys.argv) >= 4:
    self, ip, port, keywords = sys.argv[:4]
    if sys.argv[4:]:
        print(str(sys.argv[4:])+" 变量将不会被使用")
elif len(sys.argv) == 1:
    ip = input("请输入IP:")
    port = input("请输入端口:")
    keywords = input("请输入关键词:")
else:
    print("请按IP 端口 关键词的顺序输入变量")
    exit()

reptile = Reptile("http://"+ip+":"+port)

res = reptile.search(keywords)


for i, book in enumerate(res, start=1):
    print(str(i)+"> "+book[1])

switch = input("请选择需要下载的书籍：")

book_id = res[int(switch)-1][0]
book_name = res[int(switch)-1][1]

if os.path.exists(book_name):
    if os.path.isfile(book_name):
        print("存在同名文件"+book_name+"，请手动删除改文件后再次运行")
        exit()
else:
    os.makedirs(book_name)
print("开始下载" + book_name + book_id)
res = reptile.direct(book_id)

for chapter_list in res:
    chapter_id = chapter_list[0]
    res = reptile.content(chapter_id)
    volume_name = res[0]
    chapter_name = res[1]
    text = res[2]
    if os.path.exists(book_name+'/'+volume_name):
        if os.path.isfile(book_name+'/'+volume_name):
            print("存在同名文件"+volume_name+"，请手动删除改文件后再次运行")
            exit()
    else:
        os.makedirs(book_name+'/'+volume_name)

    # if os.path.exists(book_name+'/'+volume_name+'/'+chapter_name+'.txt'):
    #     if os.path.isfile(book_name+'/'+volume_name+'/'+chapter_name+'.txt'):
    #         print("存在同名文件"+chapter_name+"，请手动删除改文件后再次运行")
    #         continue

    with open(book_name+'/'+volume_name+'/'+chapter_name+'.txt', "w", encoding='utf-8') as chapter:
        chapter.writelines(text)
