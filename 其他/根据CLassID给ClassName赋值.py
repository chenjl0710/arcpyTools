# -*- coding: cp936 -*-
import arcpy
# arcpy.env.workspace = r"F:\������ˮ��\2result\��ˮ�� �ֵؿ�"
iFC = raw_input("������ֵؿ��ļ���·����")
iGetValuefield = "ClassID"
i = 1
print iFC
iCursor = arcpy.UpdateCursor(iFC)
for iRow in iCursor:
#         print i
    iValue = iRow.getValue(iGetValuefield)
    if iValue == "01" :
            #iRow.setValue("ClassID","10")
        iRow.setValue("ClassName","����")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "02" :
            #iRow.setValue("ClassID","20")
        iRow.setValue("ClassName","԰��")
#             iRow.setValue("ClassID","02")
        iCursor.updateRow(iRow)
    elif iValue == "03" :
            #iRow.setValue("ClassID","30")
        iRow.setValue("ClassName","�ֵ�")
#             iRow.setValue("ClassID","03")
        iCursor.updateRow(iRow)
    elif iValue == "04" :
            #iRow.setValue("ClassID","40")
        iRow.setValue("ClassName","�ݵ�")
#             iRow.setValue("ClassID","04")
        iCursor.updateRow(iRow)
    elif iValue == "06" :
            #iRow.setValue("ClassID","50")
        iRow.setValue("ClassName","����ִ��õ�")
#             iRow.setValue("ClassID","06")
        iCursor.updateRow(iRow)
    elif iValue == "07" :
            #iRow.setValue("ClassID","60")
        iRow.setValue("ClassName","סլ�õ�")
#             iRow.setValue("ClassID","07")
        iCursor.updateRow(iRow)
    elif iValue == "101" :
            #iRow.setValue("ClassID","70")
        iRow.setValue("ClassName","��·�õ�")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "102" :
            #iRow.setValue("ClassID","70")
        iRow.setValue("ClassName","��·�õ�")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "103" :
            #iRow.setValue("ClassID","80")
        iRow.setValue("ClassName","�����õ�")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "104" :
            #iRow.setValue("ClassID","90")
        iRow.setValue("ClassName","ũ���·")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "11" :
            #iRow.setValue("ClassID","100")
        iRow.setValue("ClassName","ˮ��ˮ����ʩ�õ�")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    elif iValue == "12" :
            #iRow.setValue("ClassID","100")
        iRow.setValue("ClassName","��������")
#             iRow.setValue("ClassID","01")
        iCursor.updateRow(iRow)
    i = i + 1
del iCursor,iRow