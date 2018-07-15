# -*- coding: cp936 -*-
'''
获取属性表里的
字段名称
字段类型
字段长度
并将结果保存在excel里
'''


import arcpy,os
import xlwt
#写excel
#创建workbook
newbook = xlwt.Workbook(encoding='cp936')
#创建sheet
newsheet = newbook.add_sheet('first')
j = 0
i = 0

FolderPath = r"C:\Users\Administrator\Desktop\wkcheckGeometry"
Folders = os.listdir(FolderPath)
for Folder in Folders:

    print Folder
    shpFolder = os.path.join(FolderPath,Folder)
    ifcF = Folder + "_地类更新.shp"
    ifc = os.path.join(shpFolder,ifcF)


    
    newsheet.write(0,i,Folder)
    
    #往单元格内写内容
    #将book里第一列的数值写入到newbook里，book里其他列的数值不要
    fields = arcpy.ListFields(ifc)
    for field in fields:
        j = j + 1
        newsheet.write(j,i,field.name)
    j = 0
    i = i+ 1

print "ok"

#保存
excelSavePath = FolderPath + "\\" + "属性表字段列表.xls"
newbook.save(excelSavePath)
    
