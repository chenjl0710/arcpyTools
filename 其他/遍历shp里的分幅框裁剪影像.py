# -*- coding: cp936 -*-
import arcpy
import os
irst = r"G:\湖南\CJL\E112D8_N28D3_20130930_DOM_4_fus.pix"
ifc = r"D:\tset\clip\clip_Shp.shp"
arcpy.MakeFeatureLayer_management(ifc, "lyr") 
save_floder = r"D:\tset\clip"
icursor = arcpy.SearchCursor(ifc)
for row in icursor:
    igetvalue = row.getValue("FID")
    print igetvalue
    #clip_shp = 
    arcpy.SelectLayerByAttribute_management("lyr","NEW_SELECTION",'"FID" = %s'%igetvalue)
    rst_name = os.path.basename(os.path.splitext(irst)[0]) + "_" + '%s'%igetvalue + ".tif"
    outsave = os.path.join(save_floder,rst_name)
    arcpy.Clip_management(irst,"",outsave,"lyr","65536","ClippingGeometry","NO_MAINTAIN_EXTENT")
    arcpy.SelectLayerByAttribute_management("lyr","CLEAR_SELECTION")
print "over"