# -*- coding: utf8 -*-
import os
import arcpy
from vector import sdeSearch
'''
1、	根据项目名称，在相应的数据集下根据项目编号检索并输出数据集至文件数据库file geodatabase。
'''
prjid = arcpy.GetParameterAsText(0).split('--')[0]
outdir = arcpy.GetParameterAsText(1)
sde = sdeSearch()
loca = sde.searchBypeoject(prjid)
sde.exportByloca(loca,prjid,outdir)

