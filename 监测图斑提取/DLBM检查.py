# -*- coding: cp936 -*-
import arcpy

'''
ʹ��˵��
����ȷ�����Ա���û�С�F15DLBM���ֶ�
�����жϡ�F15DLBM���ֶ���ĵ�������Ƿ�����ڷ�����ϵ
���������벻�����ڷ�����ϵ�����ڡ�F15DLMC�����ʶ��00���벻��00��
'''

iFc = r"D:\test\Ϋ����2013��DLBM.shp"
Dic_book = {
            "011":"ˮ��","012":"ˮ����","013":"����",
            "021":"��԰","022":"��԰","023":"����԰��",
            "031":"���ֵ�","032":"��ľ�ֵ�","033":"�����ֵ�",
            "041":"��Ȼ���ݵ�","042":"�˹����ݵ�","043":"�����ݵ�",
            "201":"����","202":"������","203":"��ׯ","204":"�ɿ��õ�","205":"�羰��ʤ�������õ�",
            "101":"��·�õ�","102":"��·�õ�","104":"ũ���·","105":"�����õ�","106":"�ۿ���ͷ�õ�","107":"�ܵ������õ�",
            "111":"����ˮ��","112":"����ˮ��","113":"ˮ��ˮ��","114":"����ˮ��","115":"�غ�̲Ϳ","116":"��½̲Ϳ","117":"����","118":"ˮ�������õ�","119":"���������û�ѩ",
            "122":"��ʩũ�õ�","123":"�￲","124":"�μ��","125":"�����","126":"ɳ��","127":"���"
            }


# ���F15DLBM�ֶ�
#arcpy.AddField_management(iFc,"check","TEXT","","","10")
i = 1
iCursor = arcpy.UpdateCursor(iFc)
DLBM_FIELD = "F15DLBM"
print "----------Start----------"
print "F15DLBM����ȷ��FID�ֱ���"
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

print "���޸����ϲ���ȷ��F15DLBM"
print "-------finish---------------"