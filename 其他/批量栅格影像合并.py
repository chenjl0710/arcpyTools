# -*- coding: utf-8 -*-

import arcpy
arcpy.env.workspace = r"G:\KunShan_Road\IMG\19"
output_location = r"G:\KunShan_Road\IMG"
inputtst = ""
rsts = arcpy.ListDatasets()
inputtst = rsts[0]
for rst in rsts:
        print rst
        if rst <> rsts[0] :
                inputtst = inputtst + ";" + rst
        else:
                continue
print inputtst
arcpy.MosaicToNewRaster_management(inputtst,output_location,"md_mosaic.tif" ,"", "8_BIT_UNSIGNED", "", "4", "LAST", "FIRST")


print u"处理完成！"
