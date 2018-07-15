# -*- coding: cp936 -*-
import arcpy

'''
使用说明
首先确定属性表里没有“F15DLBM“字段
依次判断“F15DLBM”字段里的地类编码是否存在于分类体系
如果地类编码不存在于分类体系，则在“F15DLMC”里标识“00编码不对00”
'''

iFc = r"D:\test\潍城区2013年DLBM.shp"
Dic_book = {
            "011":"水田","012":"水浇地","013":"旱地",
            "021":"果园","022":"茶园","023":"其他园地",
            "031":"有林地","032":"灌木林地","033":"其他林地",
            "041":"天然牧草地","042":"人工牧草地","043":"其他草地",
            "201":"城市","202":"建制镇","203":"村庄","204":"采矿用地","205":"风景名胜及特殊用地",
            "101":"铁路用地","102":"公路用地","104":"农村道路","105":"机场用地","106":"港口码头用地","107":"管道运输用地",
            "111":"河流水面","112":"湖泊水面","113":"水库水面","114":"坑塘水面","115":"沿海滩涂","116":"内陆滩涂","117":"沟渠","118":"水工建筑用地","119":"冰川及永久积雪",
            "122":"设施农用地","123":"田坎","124":"盐碱地","125":"沼泽地","126":"沙地","127":"裸地"
            }


# 添加F15DLBM字段
#arcpy.AddField_management(iFc,"check","TEXT","","","10")
i = 1
iCursor = arcpy.UpdateCursor(iFc)
DLBM_FIELD = "F15DLBM"
print "----------Start----------"
print "F15DLBM不正确的FID分别是"
for iRow in iCursor:
    iValue = iRow.getValue(DLBM_FIELD)
    if iValue in Dic_book or iValue == "":
        #iRow.setValue("check",Dic_book[iValue])
        print "1"
        print iValue
        print "/"
        iRow.setValue("check","1")
    else :
        print "0"
        print iValue
        print "//"
        iRow.setValue("check","0")
        #print iRow.getValue("FID")
    iCursor.updateRow(iRow)
del iCursor,iRow

print "请修改以上不正确的F15DLBM"
print "-------finish---------------"