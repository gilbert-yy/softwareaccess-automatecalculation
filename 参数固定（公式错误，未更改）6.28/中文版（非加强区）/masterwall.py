#coding=<utf8>
import os, sys, re, codecs, xlwt
from xlwt import Workbook

print('请输入文件路径')
path = input()
print('最大的层数编号是多少？（若WPJ33.OUT是最大的文件，则输入33）')
maxn = int(int(input())+1)

wb = Workbook(encoding='utf8')

sheet = wb.add_sheet('sheet 1') #创建excel表格—‘name’
sheet.write(0,0,'墙柱编号')
sheet.write(0,1,'自然层号')
sheet.write(0,2,'As')

breakflag = False

for i in range(1,100000):
    As = []
    try:
        if i >= wallamount+1:
            breakflag = True
            break
        else:
            pass
    except:
        pass

    
    for n in range(1,maxn):
        try:
            readtxt = codecs.open(path+'/WPJ'+str(n)+'.OUT','r','gbk')#
            fullcontent = readtxt.read()
        
            fullcontent = fullcontent.replace(' ','') 
            fullcontent = fullcontent.replace('\n','')
            fullcontent = fullcontent.replace('\\','')
        
            regexwall = re.compile(r'N-WC=.+?WS_XF')
            wallinfo = regexwall.findall(fullcontent)
            wallamount = len(wallinfo)

            try:
                targetwall = wallinfo[i-1]
            except:
                As.insert(int(n-1),-10086)                
                continue
                
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
                As.insert(int(n-1), int(1000*((max(1.3*0,1*1.1*V)-0.8*(-N))/0.6-0*0)/360)) #此处更改公式
            except:
                As.insert(int(n-1),-10086)
                pass

            n = wallamount+1
                
        except:
            As.insert(int(n-1),-10086)
            pass
    
    maxAs = max(As)
    maxAsfloor = As.index(maxAs)+1
    sheet.write(i,0,str(i))
    sheet.write(i,1,str(maxAsfloor))
    sheet.write(i,2,str(maxAs))
    continue
    
wb.save('标准层表(最大As).xls')
print('完成整理')
