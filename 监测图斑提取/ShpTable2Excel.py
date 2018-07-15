# -*- coding: cp936 -*-
import arcpy
import xlrd
import xlwt
import os
import shutil

def CalcultateClass(infc):
    classes = ["1A","1B","2","3A","3B","7A","7B","8"]
    list_classes = []
    q = 0
    for c in classes:
        q = q + 1
        list_classes.append([q,c,0,0.0,0.0,0.0])
    print len(list_classes)
    cur = arcpy.SearchCursor(infc)
    i = 1
    for row in cur:
        tblx = row.getValue("TBLX")
        for c in list_classes:
            if tblx == str(c[1]):
                c[2] = c[2] + 1
                c[3] = c[3] + row.getValue("JCMJ")
                c[4] = c[4] + row.getValue("ZGDMJ")
                c[5] = c[5] + row.getValue("ZJBNTMJ")
                continue
    for c in list_classes:
        print c
    fields = ["序号","图斑类型","图斑数量","图斑面积（亩）","占耕地面积（亩）","占基本农田面积（亩）"]

    wbk = xlwt.Workbook(encoding = 'cp936')
    wsheet = wbk.add_sheet("sheet1")
    m = 0
    for field in fields:
        wsheet.write(0,m,field)
        m = m + 1
    n = m = 0
    for list_ in list_classes:
        n = 0
        for val in list_:
            wsheet.write(m+1,n,val)
            print val
            n = n + 1
        m = m + 1
    wbk.save("C:\s.xls")
    for i in range(10):
        shutil.copyfile("C:\s.xls","C:\\"+str(i) + "jctb.xls")
    #shutil.copyfile("C:\s.xls","C:\jctb.xls")        
        
if __name__ == "__main__":
    infc = r"D:\山东潍坊统计数据\370725昌乐县jctb.shp"
    CalcultateClass(infc)
