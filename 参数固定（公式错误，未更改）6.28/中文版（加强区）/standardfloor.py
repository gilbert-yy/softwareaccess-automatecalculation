# coding: utf-8
import os, sys, re, xlwt, codecs
from xlwt import Workbook


print('请输入文件路径')
path = input()
print('最大的层数编号是多少？（若WPJ33.OUT是最大的文件，则输入33）')
maxn = int(int(input())+1)

wb = Workbook(encoding='utf8')

sheet = wb.add_sheet('sheet 1') #创建excel表格—‘name’
sheet.write(1,0,'墙柱编号')

m=1

for n in range(1,maxn):
    As = []
    try:
        print('正在处理楼层 '+ str(n))
        readtxt = codecs.open(path+'/WPJ'+str(n)+'.OUT','r','gbk')
        #原始数据文档的路径

        sheet.write(0,5*int(m)-4,str(n)+'号自然层')
        sheet.write(1,1+5*(m-1),'N')
        sheet.write(1,2+5*(m-1),'V')
        sheet.write(1,3+5*(m-1),'H')
        sheet.write(1,4+5*(m-1),'b')
        sheet.write(1,5*m,'As')

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
                regexH = re.compile(r'B.H.Lwc.m.=\d+(?:\.|)\d+.\d*(?:\.|)\d*.\d*(?:\.|)\d*')
                wallN = regexN.findall(targetwall)[1]
                wallV = regexV.findall(targetwall)[1]
                wall = regexH.findall(targetwall)[0]
                
                N = wallN.strip('N=')
                V = wallV.strip('V=')
                V = V.strip('-')
                N = float(N)
                V = float(V)
                H = float(wall[16:20])
                b = float(wall[11:15])
                H = H*1000
                b = b*1000

                try:
                    sheet.write(i+1,0,str(i))
                except:
                    pass

                Vm = (0.4*1.43*H*b+0.1*N+0.8*360*101*H/200/1000)/0.85
                maxVm = max(1*1.1*V,1.3*Vm)
                As.insert(int(i-1), int(1000*((100-0.8*(-N))/0.6-0*0)/360)) #此处更改计算公式
                sheet.write(i+1,1+5*(m-1),str(N))
                sheet.write(i+1,2+5*(m-1),str(V))
                sheet.write(i+1,3+5*(m-1),str(H))
                sheet.write(i+1,4+5*(m-1),str(b))
                sheet.write(i+1,5*m,str(As[i-1]))
                
                
            except:
                try:
                    sheet.write(i+1,0,str(i))
                except:
                    pass
                
                sheet.write(i+1,5*m,'出错')
                As.insert(int(i-1), 'N/A')
                pass

        m=m+1
    
    except:
        print(str(n)+' 层不存在')
        pass


wb.save('标准层表.xls')
print('完成整理')
