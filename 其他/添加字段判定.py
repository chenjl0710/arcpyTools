# -*- coding: cp936 -*-
import arcpy

'''
脐橙的shp属性表里必须包含以下字段
投影面积              double
点个数                long
Sum_Value             double
坡面面积               double
'''
'''
Ty_Area_Flag、Pnt_Count_Flag、Sum_Value_Flag、Pm_Area_Flag为true
表示投影面积 、点个数、Sum_Value、坡面面积这些字段存在
'''
Ty_Area_Flag = True
Pnt_Count_Flag = True
Sum_Value_Flag = True
Pm_Area_Flag = True


shp = r"D:\test\test.shp"

print "start"

'''
判断某个或者某些字段是否在shp里存在，
如不存在则添加该字段，即Ty_Area_Flag、Pnt_Count_Flag、Sum_Value_Flag、Pm_Area_Flag为Flase
如存在，则跳过添加字段
'''
fields = arcpy.ListFields(shp)
fieldnameList = []
for field in fields:
        print field.baseName
        #将属性表里的字段存放在一个空的字段列表里
        fieldnameList.append(field.baseName)
#依次读取字段列表里字段名称，与需要添加的字段名作比较，
#如果需要添加的字段不存在Flag=False，
for fieldname in fieldnameList:
        if fieldname <> "投影面积":
                Ty_Area_Flag = False
        if fieldname <> "点个数":
                Pnt_Count_Flag = False
        if fieldname <> "Sum_Value":
                Sum_Value_Flag = False
        if fieldname <> "坡面面积":
                Pm_Area_Flag = False
#根据上面判断的True和False，确定是否需要添加字段。                 
if Ty_Area_Flag == False:
        arcpy.AddField_management(shp,"投影面积","double")
        print "投影面积 添加成功"
if Pnt_Count_Flag == False:
        arcpy.AddField_management(shp,"点个数","long")
        print "点个数 添加成功"
if Pm_Area_Flag == False:
        arcpy.AddField_management(shp,"Sum_Value","double")
        print "Sum_Value 添加成功"
if Sum_Value_Flag == False:
        arcpy.AddField_management(shp,"坡面面积","double")
        print "坡面面积 添加成功"

     

