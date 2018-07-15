# -*- coding: cp936 -*-

import arcpy,os


# Local variables:



# jctb = raw_input('请输入JCTB:')
# JBNT = raw_input('请输入JBNT:')
# saveFolder = raw_input('请输入中间文件存储文件夹路径:')
# raw_input('开始计算')
def CalcuZGDMJ(JCTBshp,GDTB,saveFolder):
    Input_Features = []
    Input_Features.append(JCTBshp)
    Input_Features.append(GDTB)
    print Input_Features
    Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_GDTB" + "_intersect.shp")
    print Output_Feature_Class
    arcpy.Intersect_analysis(Input_Features, Output_Feature_Class, "ALL", "", "INPUT")
    
    # Process: Add Field
    #arcpy.AddField_management(Output_Feature_Class, "ZJBNTMJ", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
    # Process: Calculate Field
    arcpy.CalculateField_management(Output_Feature_Class, "ZGDMJ", "!SHAPE.AREA!", "PYTHON_9.3", "")
    
    # Process: Dissolve
    Dissolve_Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_GDTB" + "_intersect_Dissolve.shp")
    print "dissolving..."
    arcpy.Dissolve_management(Output_Feature_Class,Dissolve_Output_Feature_Class, "BSM", "ZGDMJ SUM", "MULTI_PART", "DISSOLVE_LINES")
    
    print "JoinFielding..."
    arcpy.JoinField_management(JCTBshp, "BSM",Dissolve_Output_Feature_Class, "BSM", "BSM;SUM_ZGDMJ")
    
    print "CalculateFielding..."
    arcpy.CalculateField_management(JCTBshp, "ZGDMJ", "!SUM_ZGDMJ!","PYTHON_9.3", "")
    arcpy.CalculateField_management(JCTBshp, "ZGDMJ", '!SUM_ZGDMJ!/666.7',"PYTHON_9.3", "")
    
def CalcuZJBNTMJ(JCTBshp,JBNTTB,saveFolder):
    Input_Features = []
    Input_Features.append(JCTBshp)
    Input_Features.append(JBNTTB)
    print Input_Features
    
    Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_JBNTTB" + "_intersect.shp")
    print Output_Feature_Class
    arcpy.Intersect_analysis(Input_Features, Output_Feature_Class, "ALL", "", "INPUT")
    
    # Process: Add Field
    #arcpy.AddField_management(Output_Feature_Class, "ZJBNTMJ", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
    # Process: Calculate Field
    arcpy.CalculateField_management(Output_Feature_Class, "ZJBNTMJ", "!SHAPE.AREA!", "PYTHON_9.3", "")
    
    # Process: Dissolve
    Dissolve_Output_Feature_Class = os.path.join(saveFolder,JCTBshp[:-4] + "_JBNTTB" + "_intersect_Dissolve.shp")
    print "dissolving..."
    arcpy.Dissolve_management(Output_Feature_Class,Dissolve_Output_Feature_Class, "BSM", "ZJBNTMJ SUM", "MULTI_PART", "DISSOLVE_LINES")
    
    print "JoinFielding..."
    arcpy.JoinField_management(JCTBshp, "BSM",Dissolve_Output_Feature_Class, "BSM", "BSM;SUM_ZJBNTM")
    
    print "CalculateFielding..."
    arcpy.CalculateField_management(JCTBshp, "ZJBNTMJ", "!SUM_ZJBNTM!","PYTHON_9.3", "")
    arcpy.CalculateField_management(JCTBshp, "ZJBNTMJ", '!SUM_ZJBNTM!/666.7',"PYTHON_9.3", "")
    
    arcpy.DeleteField_management(JCTBshp,"BSM_1")
    arcpy.DeleteField_management(JCTBshp,"SUM_ZJBNTM")
    
if __name__ == "__main__":
    print "--------------Start-----------"
    saveFolder = r"C:\Users\Administrator\Desktop\test"
    JCTBshp = r"C:\Users\Administrator\Desktop\test\370785高密市jctb.shp"
    JBNTTB = r"C:\Users\Administrator\Desktop\test\JBNTBHTB.SHP"
    GDTB = r"C:\Users\Administrator\Desktop\test\潍坊2013耕地.shp"
    CalcuZJBNTMJ(JCTBshp,JBNTTB,saveFolder)
    CalcuZGDMJ(JCTBshp,GDTB,saveFolder)
    print "------------finish-------------"
    
