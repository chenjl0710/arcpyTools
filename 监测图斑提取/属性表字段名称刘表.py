# -*- coding: cp936 -*-
'''
��ȡ���Ա����
�ֶ�����
�ֶ�����
�ֶγ���
�������������excel��
'''


import arcpy,os
import xlwt
#дexcel
#����workbook
newbook = xlwt.Workbook(encoding='cp936')
#����sheet
newsheet = newbook.add_sheet('first')
j = 0
i = 0

FolderPath = r"C:\Users\Administrator\Desktop\wkcheckGeometry"
Folders = os.listdir(FolderPath)
for Folder in Folders:

    print Folder
    shpFolder = os.path.join(FolderPath,Folder)
    ifcF = Folder + "_�������.shp"
    ifc = os.path.join(shpFolder,ifcF)


    
    newsheet.write(0,i,Folder)
    
    #����Ԫ����д����
    #��book���һ�е���ֵд�뵽newbook�book�������е���ֵ��Ҫ
    fields = arcpy.ListFields(ifc)
    for field in fields:
        j = j + 1
        newsheet.write(j,i,field.name)
    j = 0
    i = i+ 1

print "ok"

#����
excelSavePath = FolderPath + "\\" + "���Ա��ֶ��б�.xls"
newbook.save(excelSavePath)
    
