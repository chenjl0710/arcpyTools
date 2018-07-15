# -*- coding: cp936 -*-
import arcpy
# arcpy.env.workspace = r"F:\江西渝水区\2result\渝水区 粗地块"
iFC = raw_input("请输入粗地块文件夹路径：")
iGetValuefield = "ClassID"
i = 1
print iFC
iCursor = arcpy.UpdateCursor(iFC)
for iRow in iCursor:
#         print i
    iValue = iRow.getValue(iGetValuefield)
    if iValue == "01" :
            #iRow.setValue("ClassID","10")
        iRow.setValue("ClassName","耕地")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "02" :
            #iRow.setValue("ClassID","20")
        iRow.setValue("ClassName","园地")
#             iRow.setValue("ClassID","02")
        iCursor.updateRow(iRow)
    elif iValue == "03" :
            #iRow.setValue("ClassID","30")
        iRow.setValue("ClassName","林地")
#             iRow.setValue("ClassID","03")
        iCursor.updateRow(iRow)
    elif iValue == "04" :
            #iRow.setValue("ClassID","40")
        iRow.setValue("ClassName","草地")
#             iRow.setValue("ClassID","04")
        iCursor.updateRow(iRow)
    elif iValue == "06" :
            #iRow.setValue("ClassID","50")
        iRow.setValue("ClassName","工矿仓储用地")
#             iRow.setValue("ClassID","06")
        iCursor.updateRow(iRow)
    elif iValue == "07" :
            #iRow.setValue("ClassID","60")
        iRow.setValue("ClassName","住宅用地")
#             iRow.setValue("ClassID","07")
        iCursor.updateRow(iRow)
    elif iValue == "101" :
            #iRow.setValue("ClassID","70")
        iRow.setValue("ClassName","铁路用地")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "102" :
            #iRow.setValue("ClassID","70")
        iRow.setValue("ClassName","公路用地")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "103" :
            #iRow.setValue("ClassID","80")
        iRow.setValue("ClassName","街巷用地")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "104" :
            #iRow.setValue("ClassID","90")
        iRow.setValue("ClassName","农村道路")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "11" :
            #iRow.setValue("ClassID","100")
        iRow.setValue("ClassName","水域及水利设施用地")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "12" :
            #iRow.setValue("ClassID","100")
        iRow.setValue("ClassName","其他土地")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    i = i + 1
del iCursor,iRow