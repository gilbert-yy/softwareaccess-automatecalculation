# coding: utf-8
import os, sys, re, xlwt, codecs
from xlwt import Workbook

wb = Workbook(encoding='utf8')

print('请输入文件路径')
path = input()
print('最大的层数编号是多少？（若WPJ33.OUT是最大的文件，则输入33）')
maxn = int(int(input())+1)

for n in range(1,maxn):
    try:
        print('正在处理楼层 '+ str(n))
        readtxt = codecs.open(path+'/WPJ'+str(n)+'.OUT','r','gbk')

        As = []
    
        name = str('自然层 '+str(n)) #创建excel表格—‘name’是工作表的名字
        sheet = wb.add_sheet(name) #创建excel表格—‘name’
        sheet.write(0,0,'墙柱编号')
        sheet.write(0,1,'N')
        sheet.write(0,2,'V')
        sheet.write(0,3,'As')
    
        fullcontent = readtxt.read()

        fullcontent = fullcontent.replace(' ','')
        fullcontent = fullcontent.replace('\n','')
        fullcontent = fullcontent.replace('\\','')
    
        regexwall = re.compile(r'N-WC=.+?WS_XF')
        wallinfo = regexwall.findall(fullcontent)
        
        for i in range(1,len(wallinfo)):
            targetwall = wallinfo[i-1]
        
            try:
                regexN = re.compile(r'N=(?:-|)\d*(?:\.|)\d*') 
                regexV = re.compile(r'V=(?:-|)\d*(?:\.|)\d*')
                wallN = regexN.findall(targetwall)[1]
                wallV = regexV.findall(targetwall)[1]
        
                N = wallN.strip('N=')
                V = wallV.strip('V=')
                V = V.strip('-')
                N = float(N)
                V = float(V)
                As.insert(int(i-1), int(1000*((max(1.3*0,1*1.1*V)-0.8*(-N))/0.6-0*0)/360)) #此处更改计算公式
                sheet.write(i,0,str(i))
                sheet.write(i,1,str(N))
                sheet.write(i,2,str(V))
                sheet.write(i,3,str(As[i-1]))
                
            except:
                sheet.write(i,0,i)
                sheet.write(i,3,'出错')
                As.insert(int(i-1), '不存在')
                pass
    
    except:
        print(str(n)+' 层不存在')
        pass
    
wb.save('自然层表.xls')
print('完成整理')
