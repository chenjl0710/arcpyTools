# -*- coding: cp936 -*-
import arcpy,os
import time
#�����С����ֵ��ͼ�ߺ��������������ͼ���ں�

arcpy.env.overwriteOutput = True

#���Dissolve��Eli��Area�ֶ�

#����Dissolve�ֶΣ�ʹ֮ΪΨһֵ

#Eli��ֵȫ����ֵΪ0

#����Area���ֵ

#�����С��400��ѡ�����������dissolve��ֵ��ֵ��Eli

#����Eli��Ϊ0��Ҫ�أ����Ҫ�ؼ�ΪFC��Ȼ��ͨ��λ��ѡ�����FC���ڵ�Ҫ��

#�޳���FC���ڵ�Ҫ�����ǵ�·��Ҫ��

#�����ж���FC���ڵ�Ҫ������û����ͬClassID���������400��Ҫ�أ����У������Ҫ�ص�Dissolve��ֵ��ֵ��FC��Dissolve��
#���û�У���ѡ����FC���ڵ��������Ҫ�أ������Ҫ�ص�Dissolve��ֵ��ֵ��FC��Dissolve��

def Select_Copy(inFC):
    arcpy.MakeFeatureLayer_management(inFC,"EliLayer")
    arcpy.SelectLayerByAttribute_management("EliLayer","NEW_SELECTION",'"Area" < 400') #ѡ��һ��
    arcpy.SelectLayerByLocation_management("EliLayer","SHARE_A_LINE_SEGMENT_WITH")#ѡ���ܱߵ�
    copy = os.path.dirname(inFC) + "\\" + "temp" + "\\" + os.path.basename(inFC)[0:-4] + "EliLayer_Copy.shp"
    print "copy:",copy 
    arcpy.CopyFeatures_management("EliLayer",copy)
    return copy

def AddAttribute(inFC):
    #���Dissolve��Eli��Area�ֶ�
    try:
        arcpy.AddField_management(inFC,"Dissolve","LONG")
        arcpy.AddField_management(inFC,"Eli","LONG")
        arcpy.AddField_management(inFC,"Area","DOUBLE")
    except:
        print "already have"
    print "Add Field Successfully"
    
    #����Dissolve�ֶΣ�ʹ֮ΪΨһֵ
    #Eli��ֵȫ����ֵΪ0
    i = 1
    cursor = arcpy.UpdateCursor(inFC)
    for row in cursor:
        row.setValue("Dissolve",i)
        row.setValue("Eli",0)
        cursor.updateRow(row)
        i = i + 1
    del cursor,row
    #����Area���ֵ
    arcpy.CalculateField_management(inFC,"Area", '!SHAPE.AREA!',"PYTHON_9.3")
    print "Calculate area successfully"

def EliminareArea(copy):
        
    ##��·���ֶ�����
    roadID_list = ['101','102','103','104']
    arcpy.MakeFeatureLayer_management(copy,"inLayer")
    #�����С��400��ѡ�����������dissolve��ֵ��ֵ��Eli
    arcpy.SelectLayerByAttribute_management("inLayer","NEW_SELECTION",'"Area" < 400')
    cursor = arcpy.UpdateCursor("inLayer")
    for row in cursor:
        dis = row.getValue("Dissolve")
        row.setValue("Eli",dis)
        cursor.updateRow(row)
    del cursor,row
    print "Dissolve,Eli had have value"
    
    #����Eli��Ϊ0��Ҫ�أ����Ҫ�ؼ�ΪFC��Ȼ��ͨ��λ��ѡ�����FC���ڵ�Ҫ��
    cursor = arcpy.UpdateCursor(copy)
    for row in cursor:
        print row.getValue("FID")
        j = row.getValue("Eli")
        ID = row.getValue("ClassID")
        if j <> 0 and id not in roadID_list:
            sql_str = '"Eli" = ' + str(j)
            arcpy.MakeFeatureLayer_management(copy,"EliLayer")
            arcpy.SelectLayerByAttribute_management("EliLayer","NEW_SELECTION",sql_str) #ѡ��һ��
            arcpy.SelectLayerByLocation_management("EliLayer","SHARE_A_LINE_SEGMENT_WITH")#ѡ���ܱߵ�
            arcpy.SelectLayerByAttribute_management("EliLayer","REMOVE_FROM_SELECTION",sql_str)#�߳����ĵ�Ҫ��
            arcpy.MakeFeatureLayer_management("EliLayer","SameID")
            cur = arcpy.SearchCursor("EliLayer")
            area = 0
            dissolve = 0
    #         ClassName_Value = ""
    #         ClassID_Value = ""
            #print j
            for r in cur:
                #print "boundry",r.getValue("Dissolve")
                if r.getValue("ClassID") not in roadID_list:#�޳���FC���ڵ�Ҫ�����ǵ�·��Ҫ��
                    if r.getValue("ClassID") == ID:#
                        dissolve = r.getValue("Dissolve")
                        arcpy.SelectLayerByAttribute_management("SameID","NEW_SELECTION",'"ClassID" = ' + "'" + str(ID) + "'")
                        c = arcpy.SearchCursor("SameID")
                        for R in c:
                            if R.getValue("Area") > area :
                                area = R.getValue("Area")
                                dissolve = R.getValue("Dissolve")
                        break
                    elif r.getValue("Area") > area:
                        area = r.getValue("Area")
                        dissolve = r.getValue("Dissolve")
                        row.setValue("ClassName",r.getValue("ClassName"))
                        row.setValue("ClassID",r.getValue("ClassID"))
                #else:
                    #print "this is road ",r.getValue("ClassID")
            row.setValue("Dissolve",str(dissolve))
            cursor.updateRow(row)
            arcpy.Delete_management("EliLayer")
            #del cur,r
    del cursor,row
    print "finish Elilayer"
    
def PanduanArea(inFC):
    fields = arcpy.ListFields(inFC)
    #��Ҫ�ظ��ֶμ���
    #if ("Area" not in fields):
    #    arcpy.AddField_management(inFC,"Area","DOUBLE")
    arcpy.CalculateField_management(inFC,"Area", '!SHAPE.AREA!',"PYTHON_9.3")
    arcpy.MakeFeatureLayer_management(inFC,"xiaoyu400")
    arcpy.SelectLayerByAttribute_management("xiaoyu400", "NEW_SELECTION",'"Area" < 400')
    cursor = arcpy.SearchCursor("xiaoyu400")
    i = 0
    for row in cursor:
        i = i + 1
        if i == 0:
            print "there is no feature area < 400"
            return False
        else:
            print "there is some features area < 400"
            return True
    if i == 0:
        print "there is no feature area < 400"
        return False
    else:
        print "there is some features area < 400"
        return True


def Dissolve(copy, outFC):
    arcpy.Dissolve_management(copy, outFC,["ClassID","ClassName","Dissolve"],"Area SUM","SINGLE_PART")

def Eras_Merge(inFC, outFC, eraseFC, mergeFC):
    arcpy.Erase_analysis(inFC, outFC, eraseFC)
    arcpy.Merge_management([eraseFC, outFC],mergeFC)
    arcpy.Delete_management(inFC)
    #arcpy.CopyRows_management(mergeFC, inFC)
    arcpy.Rename_management(mergeFC, inFC, "FeatureClass")


def digui(inFC,outFC,i):
    #i = 1
    AddAttribute(inFC)
    if PanduanArea(inFC):
        copy = Select_Copy(inFC)
        print "����ѭ����" + str(i) + "��"
        print time.localtime()
        EliminareArea(copy)
        print "start dissolve"
        #arcpy.Dissolve_management(inFC, outFC,["ClassID","ClassName","Dissolve"],"Area SUM","SINGLE_PART")
        Dissolve(copy, outFC)
        Eras_Merge(inFC, outFC, eraseFC, mergeFC)
        print "Finish Dissolve"
        i = i + 1
        if i >3:
            return False
        digui(inFC, outFC,i)
    else:
        print "ssssss"
        return False
        
        
        
if __name__ == "__main__":
    arcpy.env.workspace = r"C:\Users\sherry\Desktop\̩����\temp"
    fcList = arcpy.ListFeatureClasses()
    for inFC in fcList:
        print inFC
        #inFC = r"XinFeng9"
        outFC = r"except_output"
        eraseFC = r"eraseFC"
        mergeFC = r'mergeFC'
        print "kaishi"
        i = 1
    
        print "AddAttribute"
        digui(inFC,outFC,i)
    print "ENDing"

    
        
