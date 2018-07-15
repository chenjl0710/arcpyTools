# -*- coding: cp936 -*-
import arcpy
import time
import os,shutil
#将面积小于阈值的图斑和其相邻面积最大的图斑融合

arcpy.env.overwriteOutput = True


def EliminateSamllArea(shp):
#     try:
#         arcpy.AddField_management(shp,"Area","LONG",9,2)
#     except:
#         print "Area field already exists!"
#         
#     print "Calculating Area field..."
#     arcpy.CalculateField_management(shp,"Area", '!SHAPE.AREA!',"PYTHON_9.3")
#     print "finish Calculate Area field!"
    temp = os.path.join(os.path.dirname(shp),"temp")
    arcpy.MakeFeatureLayer_management(shp,"shp")
#     sql = '"Area" < 400'
    arcpy.SelectLayerByAttribute_management("shp","NEW_SELECTION", '"Area" = 0')
    print "Eliminating..."
    Eliminate = os.path.join(temp,"Eliminate.shp" )
    print Eliminate
    arcpy.Eliminate_management("shp", Eliminate, "AREA") 
    flag = True
    i = 1
    while flag:
        print i
        arcpy.CalculateField_management(Eliminate,"Area", '!SHAPE.AREA!',"PYTHON_9.3")
        arcpy.MakeFeatureLayer_management(Eliminate,"Eliminate")
        arcpy.SelectLayerByAttribute_management("Eliminate","NEW_SELECTION",'"Area" = 0')
        FirstSelectionCount = arcpy.GetCount_management("Eliminate")
        print "FirstSelectionCount:",int(FirstSelectionCount.getOutput(0))
        arcpy.SelectLayerByLocation_management("Eliminate", "SHARE_A_LINE_SEGMENT_WITH", "Eliminate", "", "NEW_SELECTION")
        SecondSelectionCount = arcpy.GetCount_management("Eliminate")
        print "SecondSelectionCount:",int(SecondSelectionCount.getOutput(0))
        Chacount = int(SecondSelectionCount.getOutput(0)) - int(FirstSelectionCount.getOutput(0))
        print "Chacount:",Chacount
        i = i + 1
        if Chacount > 0:
            flag = True
            Eliminate = os.path.join(os.path.join(os.path.dirname(shp),"temp"),"Eliminate" + str(i) + ".shp" )
            arcpy.Eliminate_management("Eliminate", Eliminate, "AREA") 
        else:
            flag = False
            arcpy.Copy_management(Eliminate, os.path.join(os.path.dirname(shp),"Result"))
    
    
    
    print Eliminate
        
        
if __name__ == "__main__":
#     xunhuanNUM = 1
#     arcpy.env.workspace = r"F:\fenkuai.gdb"#改了
    inFC = r"C:\Users\sherry\Desktop\泰和县\JiangXi_TaiHe_Landuse_20160818.shp"
#     outFC = r"XinFeng1_Diss"
    print "~~~~~~~~~~~~~Start~~~~~~~~~~~~"
    print time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime())
    
    Fielfolder = os.path.dirname(inFC)
    temp = os.path.join(Fielfolder,"temp")
    if os.path.exists(temp):
        shutil.rmtree(temp)
        os.mkdir(temp)
    else:
        os.mkdir(temp)
    print temp
    
    Result = os.path.join(Fielfolder,"Result")
    if os.path.exists(Result):
        shutil.rmtree(Result)
        os.mkdir(Result)
    else:
        os.mkdir(Result)
    print Result
    
    EliminateSamllArea(inFC)
    print time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime())
    print "~~~~~~~~~~~~Ending~~~~~~~~~~~"

    
        

