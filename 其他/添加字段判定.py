# -*- coding: cp936 -*-
import arcpy

'''
��ȵ�shp���Ա��������������ֶ�
ͶӰ���              double
�����                long
Sum_Value             double
�������               double
'''
'''
Ty_Area_Flag��Pnt_Count_Flag��Sum_Value_Flag��Pm_Area_FlagΪtrue
��ʾͶӰ��� ���������Sum_Value�����������Щ�ֶδ���
'''
Ty_Area_Flag = True
Pnt_Count_Flag = True
Sum_Value_Flag = True
Pm_Area_Flag = True


shp = r"D:\test\test.shp"

print "start"

'''
�ж�ĳ������ĳЩ�ֶ��Ƿ���shp����ڣ�
�粻��������Ӹ��ֶΣ���Ty_Area_Flag��Pnt_Count_Flag��Sum_Value_Flag��Pm_Area_FlagΪFlase
����ڣ�����������ֶ�
'''
fields = arcpy.ListFields(shp)
fieldnameList = []
for field in fields:
        print field.baseName
        #�����Ա�����ֶδ����һ���յ��ֶ��б���
        fieldnameList.append(field.baseName)
#���ζ�ȡ�ֶ��б����ֶ����ƣ�����Ҫ��ӵ��ֶ������Ƚϣ�
#�����Ҫ��ӵ��ֶβ�����Flag=False��
for fieldname in fieldnameList:
        if fieldname <> "ͶӰ���":
                Ty_Area_Flag = False
        if fieldname <> "�����":
                Pnt_Count_Flag = False
        if fieldname <> "Sum_Value":
                Sum_Value_Flag = False
        if fieldname <> "�������":
                Pm_Area_Flag = False
#���������жϵ�True��False��ȷ���Ƿ���Ҫ����ֶΡ�                 
if Ty_Area_Flag == False:
        arcpy.AddField_management(shp,"ͶӰ���","double")
        print "ͶӰ��� ��ӳɹ�"
if Pnt_Count_Flag == False:
        arcpy.AddField_management(shp,"�����","long")
        print "����� ��ӳɹ�"
if Pm_Area_Flag == False:
        arcpy.AddField_management(shp,"Sum_Value","double")
        print "Sum_Value ��ӳɹ�"
if Sum_Value_Flag == False:
        arcpy.AddField_management(shp,"�������","double")
        print "������� ��ӳɹ�"

     

