# -*- coding: utf-8 -*-

import arcpy
arcpy.env.overwriteOutput = True 
 
def deleteYFDKFields(YFDK):
    fields = arcpy.ListFields(YFDK)
    for field in fields:
#         print field.name
        if (field.name != "FID" and field.name != "Shape" 
            and field.name != "YFDKBHWY" and field.name != "YFBHWY" and field.name != "YFBH" and field.name != "YFDKBH" 
            and field.name != "COMPLETE" and field.name != "CROPPRI"):
            arcpy.DeleteField_management(YFDK,field.name)   


def deleteYFFields(YF):
    fields = arcpy.ListFields(YF)
    for field in fields:
#         print field.name
        if (field.name != "FID" and field.name != "Shape" 
            and field.name != "YFBHWY" and field.name != "YFBH" and field.name != "CUNDM" and field.name != "XZMC" and field.name != "XZQMC"):
            arcpy.DeleteField_management(YF,field.name)
 
 
 
def YFDKCacu(YBDK,YFDK,tempFolder):
    print "样方"
    arcpy.CalculateField_management(YFDK,"Id","[FID]+1", "VB", "")  #2
#     arcpy.MakeFeatureLayer_management(YBDK, "YBDK_lyr")
#     arcpy.MakeFeatureLayer_management(YFDK, "YFDK_lyr")  #QJCTB_lyr
#     icursor = arcpy.SearchCursor("YFDK_lyr")
#     for row in icursor:
#         igetFID = row.getValue("FID")
#         print igetFID     
#         sql = "'FID' =" + "'" + igetFID + "'"
#         arcpy.SelectLayerByAttribute_management("YFDK_lyr","NEW_SELECTION",sql)
#         arcpy.SelectLayerByLocation_management("YFDK_lyr","INTERSECT","YBDK_lyr","","NEW_SELECTION")##   
    saveName = tempFolder + "\\temp_F2P.shp"
    arcpy.FeatureToPoint_management(YFDK,saveName,"INSIDE")
    out_feature_class = tempFolder + "\\temp_SpJ.shp"
    arcpy.SpatialJoin_analysis(saveName, YBDK, out_feature_class, "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT", "", "")
    arcpy.CalculateField_management(out_feature_class,"YFBHWY","[YFBHWY_1]", "VB", "")  #2
    arcpy.CalculateField_management(out_feature_class,"YFBH","[YFBH_1]", "VB", "")
    arcpy.DeleteField_management(out_feature_class, "Join_Count;TARGET_FID;ORIG_FID;YFBHWY_1;YFBH_1;CUNDM;XZMC")
    arcpy.JoinField_management(YFDK, "Id",out_feature_class, "Id", "Id;YFDKBHWY;YFBHWY;YFBH;YFDKBH;COMPLETE;CROPPRI")
    
    arcpy.CalculateField_management(YFDK,"YFBHWY","[YFBHWY_1]", "VB", "")  #2
    arcpy.CalculateField_management(YFDK,"YFBH","[YFBH_1]", "VB", "")
    arcpy.DeleteField_management(YFDK, "Id_1;YFDKBHWY_1;YFBHWY_1;YFBH_1;YFDKBH_1;COMPLETE_1;CROPPRI_1;area")
    
    icursor = arcpy.UpdateCursor(YFDK) ###
    for row in icursor:
        YFDKBH_Value = row.getValue("YFDKBH")
        if len(YFDKBH_Value) == 3:
            YFDKBH_Value = "0" + YFDKBH_Value
            row.setValue("YFDKBH",YFDKBH_Value)
            icursor.updateRow(row)
        elif len(YFDKBH_Value) == 2:
            YFDKBH_Value = "00" + YFDKBH_Value
            row.setValue("YFDKBH",YFDKBH_Value)
            icursor.updateRow(row)
        elif len(YFDKBH_Value) == 1:
            YFDKBH_Value = "000" + YFDKBH_Value
            row.setValue("YFDKBH",YFDKBH_Value)
            icursor.updateRow(row)
        elif len(YFDKBH_Value) == 4:
            row.setValue("YFDKBH",YFDKBH_Value)
            icursor.updateRow(row)
    del icursor, row
    
    arcpy.CalculateField_management(YFDK, "YFDKBHWY", "[YFBHWY]& [YFDKBH]", "VB", "")
def YFBHWY_Cacu(YBDK):
    print "最后一步了"
    icursor = arcpy.UpdateCursor(YBDK) ###
    for row in icursor:
        CunDm = row.getValue("CUNDM")
        YFBH_Value = row.getValue("YFBH")
        if len(YFBH_Value) == 3:
            YFBH_Value = "0" + YFBH_Value
            row.setValue("YFBH",YFBH_Value)
            YFBHWY_Value = CunDm + YFBH_Value
            row.setValue("YFBHWY",YFBHWY_Value)
            icursor.updateRow(row)
        elif len(YFBH_Value) == 2:
            YFBH_Value = "00" + YFBH_Value
            row.setValue("YFBH",YFBH_Value)
            YFBHWY_Value = CunDm + YFBH_Value
            row.setValue("YFBHWY",YFBHWY_Value)
            icursor.updateRow(row)
        elif len(YFBH_Value) == 1:
            YFBH_Value = "000" + YFBH_Value
            row.setValue("YFBH",YFBH_Value)
            YFBHWY_Value = CunDm + YFBH_Value
            row.setValue("YFBHWY",YFBHWY_Value)
            icursor.updateRow(row)
        elif len(YFBH_Value) == 4:
            YFBHWY_Value = CunDm + YFBH_Value
            row.setValue("YFBHWY",YFBHWY_Value)
            icursor.updateRow(row)
    del icursor, row
        

def CunCode(YBDK_fc,Cun_fc):

    arcpy.MakeFeatureLayer_management(YBDK_fc, "YBDK_fc_lyr")
    arcpy.MakeFeatureLayer_management(Cun_fc, "Cun_fc_lyr") 

    icursor = arcpy.SearchCursor("Cun_fc_lyr")
    for row in icursor:
        igetFID = row.getValue("FID")
        print igetFID
        igetXZQMC = row.getValue("XZQMC")
        igetXZMC = row.getValue("n_townname")
        igetXZQDM = row.getValue("XZQDM")
        print igetXZQMC
        print igetXZMC
        print igetXZQDM

        sql = '"XZQMC" =' + "'" + igetXZQMC + "'"
        print "sql:",sql
        arcpy.SelectLayerByAttribute_management("Cun_fc_lyr","NEW_SELECTION",sql)
        arcpy.SelectLayerByLocation_management("YBDK_fc_lyr","INTERSECT","Cun_fc_lyr","","NEW_SELECTION")##
        icursor_YBDK_fc = arcpy.UpdateCursor("YBDK_fc_lyr")
        for row_YBDK_fc in icursor_YBDK_fc:
            row_YBDK_fc.setValue("CUNDM",igetXZQDM)
            row_YBDK_fc.setValue("XZMC",igetXZMC)
            icursor_YBDK_fc.updateRow(row_YBDK_fc)
        del icursor_YBDK_fc,row_YBDK_fc
        arcpy.SelectLayerByAttribute_management("YBDK_fc_lyr","CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("Cun_fc_lyr","CLEAR_SELECTION")
    arcpy.Delete_management("YBDK_fc_lyr")
    arcpy.Delete_management("Cun_fc_lyr")

def NewCUNDM(YBDK):
    icursor = arcpy.UpdateCursor(YBDK)
    for row in icursor:
        YFBH2w = row.getValue("YFBHWY")[12:14]
        print YFBH2w
        row.setValue("YFBH",YFBH2w)
        icursor.updateRow(row)
    del icursor, row
    
        
        
    
def YFAddField(YFDK):
    arcpy.AddField_management(YFDK,"YFDKBHWY","TEXT","","","20")
    arcpy.AddField_management(YFDK,"YFBHWY","TEXT","","","20")
    arcpy.AddField_management(YFDK,"YFBH","TEXT","","","30")
    arcpy.AddField_management(YFDK,"YFDKBH","TEXT","","","30")
    arcpy.AddField_management(YFDK,"COMPLETE","SHORT")
    arcpy.AddField_management(YFDK,"CROPPRI","TEXT","","","30")
    
    arcpy.CalculateField_management(YFDK,"YFDKBH","[FID]+1", "VB", "")  #2
    
def YangFangFields(YBDK_fc):
    #添加字段
#     arcpy.AddField_management(YBDK_fc,"YFBHWY","TEXT","","","20")
    arcpy.AddField_management(YBDK_fc,"YFBH","TEXT","","","30")
    arcpy.AddField_management(YBDK_fc,"CUNDM","TEXT","","","30")
    arcpy.AddField_management(YBDK_fc,"XZMC","TEXT","","","30")
    #计算“地块样本编号”
    arcpy.CalculateField_management(YBDK_fc,"CUNDM","[XZQDM]", "VB", "")  #2
    arcpy.CalculateField_management(YBDK_fc,"XZMC","[n_townname]", "VB", "")


if __name__ == "__main__":
    arcpy.env.overwriteOutput = True 
    print "=================Start=================="
    YF = r"C:\Users\Administrator\Desktop\溧水\溧水_code.shp"
    YFDK = r"C:\Users\Administrator\Desktop\溧水\溧水县_村样方.shp"
    
#     CunJie = r"C:\Users\Administrator\Desktop\靖江\村界\靖江村界全.shp"
    tempFolder = r"C:\Users\Administrator\Desktop\靖江\tempFolder"
    print "计算样方字段值"
#     YangFangFields(YF)
    
    print "计算CUNDM"
#     NewCUNDM(YF)
    
    
    
    
    
    #给样方添加字段
    print "给样方添加字段"
    YFAddField(YFDK)
    
    print "计算样方字段"
    YFDKCacu(YF,YFDK,tempFolder)
    
    
    
    print "删除YF多余字段"
    deleteYFFields(YF)
    print "删除YFDK多余字段"
    deleteYFDKFields(YFDK)
    print "finish"

        
        
        