# coding: utf-8
import os, sys, re, xlwt, codecs
from xlwt import Workbook

wb = Workbook(encoding='utf8')

print('请输入文件路径')
path = input()
print('请输入计算公式路径')
formulapath = input()
print('最大的层数编号是多少？（若WPJ33.OUT是最大的文件，则输入33）')
maxn = int(int(input())+1)


readformula = codecs.open(formulapath+'/计算公式（加强区）.rtf','r','gbk')
formula = readformula.read()

regexfc= re.compile(r'fc=(?:-|)\d*(?:\.\d*|)')
regexft= re.compile(r'ft=(?:-|)\d*(?:\.\d*|)')
regexAwA= re.compile(r'Aw.A=(?:-|)\d*(?:\.\d*|)')
regexFyv= re.compile(r'Fyv=(?:-|)\d*(?:\.\d*|)')
regexAsv= re.compile(r'Asv=(?:-|)\d*(?:\.\d*|)')
regexs= re.compile(r's=(?:-|)\d*(?:\.\d*|)')
regexγre= re.compile(r're=(?:-|)\d*(?:\.\d*|)')
regexj= re.compile(r'j=(?:-|)\d*(?:\.\d*|)')
regexfy= re.compile(r'fy=(?:-|)\d*(?:\.\d*|)')
regexFv= re.compile(r'Fv=(?:-|)\d*(?:\.\d*|)')
regexAn= re.compile(r'An=(?:-|)\d*(?:\.\d*|)')

fc= regexfc.findall(formula)[0]
ft= regexft.findall(formula)[0]
AwA= regexAwA.findall(formula)[0]
Fyv= regexFyv.findall(formula)[0]
Asv= regexAsv.findall(formula)[0]
s= regexs.findall(formula)[0]
γre= regexγre.findall(formula)[0]
ηj= regexj.findall(formula)[0]
fy= regexfy.findall(formula)[0]
γj= regexj.findall(formula)[1]
Fv= regexFv.findall(formula)[0]
An= regexAn.findall(formula)[0]

fc= float(fc.strip('fc='))
ft= float(ft.strip('ft='))
AwA= float(AwA.strip('Aw/A='))
Fyv= float(Fyv.strip('Fyv='))
Asv= float(Asv.strip('Asv='))
s= float(s.strip('s='))
γre= float(γre.strip('re='))
ηj= float(ηj.strip('j='))
fy= float(fy.strip('fy='))
γj= float(γj.strip('j='))
Fv= float(Fv.strip('Fv='))
An= float(An.strip('An='))

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
        sheet.write(0,3,'H')
        sheet.write(0,4,'b')
        sheet.write(0,5,'As')
        
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
                N = -float(N)
                V = float(V)
                H = float(wall[16:20])
                b = float(wall[11:15])
                H = H*1000
                b = b*1000


                #这里改公式
                N = min(0.6*fc*b*H/1000,N)
                Vm = ((0.4*ft*b*H/1000)+(N*AwA)+(0.8*Fyv*Asv*H/s/1000))/γre
                Vjd = γj*V*γre
                maxV = max(ηj*Vm,Vjd)
                As.insert(int(i-1), int(1000*((maxV-0.8*N)/0.6-Fv*An)/fy))

                
                sheet.write(i,0,str(i))
                sheet.write(i,1,str(N))
                sheet.write(i,2,str(V))
                sheet.write(i,3,str(H))
                sheet.write(i,4,str(b))
                sheet.write(i,5,str(As[i-1]))
                
            except:
                sheet.write(i,0,i)
                sheet.write(i,5,'出错')
                As.insert(int(i-1), '不存在')
                pass
    
    except:
        print(str(n)+' 层不存在')
        pass
    
wb.save('自然层（加强区）.xls')
print('完成整理')
