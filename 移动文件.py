import os
import shutil
path_img='A:\\Users\\羽露\\Desktop\\新建文件夹 (5)'#需要移动的文件所在位置



tag = ['yande','Konachan' ]# 文件名中含有的字
folder = ['y','k']# 目标文件夹名
count = 0
while (count < len(tag)):
	ls = os.listdir(path_img)
	for i in ls:
		if i.find(tag[count])!=-1:
			shutil.move(path_img+'/'+i,"A:/Users/羽露/Desktop/新建文件夹 (5)/"+folder[count]+"/"+i) # 目标文件夹所在位置
	print(tag[count]+"完成")

	count = count + 1
 
print ("fin")