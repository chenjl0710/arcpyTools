# -*- coding: cp936 -*-
import arcpy,os,shutil,time
arcpy.env.overwriteOutput = True
print u"Auther: �½���"
print u"Company: �п�����"
print u"****������ļ���·�����벻Ҫ�пո�-�ַ�*****"
ISOTIMEFORMAT='%Y-%m-%d %X'
def CreateTopo(fc):
    ifc = fc
#     print "ifc:",ifc
    
    Coordinate_System = ifc.replace("shp", "prj")
#     print "Coordinate_System",Coordinate_System
#     os.path.join(shpFolder,Folder + "_�������.prj")
#     print Coordinate_System
#     File_GDB_Name = os.path.dirname(ifc),os.path.basename(ifc)    #"PLA_Topo.gdb"
    Geodatabase = ifc.replace("shp", "gdb")
    print "Geodatabase:",Geodatabase
    try:
        #�½����ݿ�
        arcpy.CreateFileGDB_management(os.path.dirname(ifc), os.path.basename(ifc).replace("shp", "gdb"), "CURRENT")
    except:
        print "���ݿ��Ѿ�����"
        
    out_dataset_path = Geodatabase
    out_name = os.path.basename(ifc).replace(".shp", "")  #���ݼ�����
#     print "out_name:",out_name
    print "���ݼ�����:",out_name
    #�������ݼ�
    arcpy.CreateFeatureDataset_management(out_dataset_path, out_name, Coordinate_System)

    #�����ݼ�����shp
    in_features = ifc  #�����shp����
    out_path = os.path.join(Geodatabase,out_name)   #shp��������ݼ�λ��
    #print u"shp��������ݼ�λ��:" + str(out_path)
    out_name = os.path.basename(ifc).replace(".shp", "") + "_ToPo"    #�����shp������
    #print u"�����shp������:" + str(out_name)
    arcpy.FeatureClassToFeatureClass_conversion (in_features, out_path, out_name)


    # Process: Create Topology
    Topo_name =os.path.basename(ifc).replace(".shp", "") + "_ToPology" #���˽ṹ������
    #print u"���˽ṹ������:" + str(Topo_name)
    arcpy.CreateTopology_management(out_path, Topo_name, "")   #zhiduo_tp  ���˽ṹ

    # Process: Add Feature Class To Topology
    Topology = os.path.join(out_path,Topo_name)  # ���˽ṹ��·��
    ##print u"���˽ṹ��·��:" + str(Topology)
    ToPoShp = os.path.join(out_path,out_name)    # Ҫ�����˵����ݼ����shp
    ##print u"Ҫ�����˵����ݼ����shp:" + str(ToPoShp)
    arcpy.AddFeatureClassToTopology_management(Topology, ToPoShp, "1", "1")

    # Process: Add Rule To Topology
    arcpy.AddRuleToTopology_management(Topology, "Must Not Have Gaps (Area)", ToPoShp, "", "", "")
    #print u"������� Must Not Have Gaps ����"
    arcpy.AddRuleToTopology_management(Topology, "Must Not Overlap (Area)", ToPoShp, "", "", "")
    #print u"������� Must Not Overlap ����"

    # Process: Validate Topology
    try:
        arcpy.ValidateTopology_management(Topology, "true")
    except:
        print str(ifc) + "������δ�ɹ���֤�����˹����½������ˡ�"

    print "������֤���" + '\n'
    print 


if __name__ == "__main__":
    road = raw_input("Input Road Shapefile:")
    landuse = raw_input("Input Landuse Shapefile:")
    
    temp = os.path.join(os.path.dirname(landuse),"temp")
    if os.path.exists(temp):
        shutil.rmtree(temp)
        os.mkdir(temp)
    else:
        os.mkdir(temp)
    Start_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
    print Start_time
    print "Merging..."
    mergelist = []
    mergelist.append(road)
    mergelist.append(landuse)
    merge_landuse = os.path.join(temp,"merge.shp") 
    arcpy.Merge_management(mergelist,merge_landuse)
    print "merge_landuse Topoing..."
    CreateTopo(merge_landuse)
    End_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
    print End_time
#     print "merge with topo time:",End_time-Start_time
#     print "Updating..."
#     update_landuse = os.path.join(temp,"Update.shp")
#     arcpy.Update_analysis(landuse,road,update_landuse)
#     print "update_landuse Topoing..."
#     CreateTopo(update_landuse)
#     End_time2 = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
#     print End_time2
#     print "update with topo time:",End_time2-End_time
    ff = raw_input("�밴Enter������...")