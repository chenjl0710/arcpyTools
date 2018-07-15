# -*- coding: utf8 -*-
import os
import arcpy
from vector import sdeSearch

productType = arcpy.GetParameterAsText(0)
Resolution = arcpy.GetParameterAsText(1)
productID = arcpy.GetParameterAsText(2)
out = arcpy.GetParameterAsText(3)

sde = sdeSearch()
prj_id = productID.split("-")[0]
loca = sde.searchBypeoject(prj_id)
sde.exportByloca(loca, prj_id, out)
