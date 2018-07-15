# -*- coding: cp936 -*-
import arcpy,os,shutil,time
arcpy.env.overwriteOutput = True
print u"Auther: 陈金律"
print u"Company: 中科天启"
print u"****输入的文件夹路径中请不要有空格、-字符*****"
ISOTIMEFORMAT='%Y-%m-%d %X'
def CreateTopo(fc):
    ifc = fc
#     print "ifc:",ifc
    
    Coordinate_System = ifc.replace("shp", "prj")
#     print "Coordinate_System",Coordinate_System
#     os.path.join(shpFolder,Folder + "_地类更新.prj")
#     print Coordinate_System
#     File_GDB_Name = os.path.dirname(ifc),os.path.basename(ifc)    #"PLA_Topo.gdb"
    Geodatabase = ifc.replace("shp", "gdb")
    print "Geodatabase:",Geodatabase
    try:
        #新建数据库
        arcpy.CreateFileGDB_management(os.path.dirname(ifc), os.path.basename(ifc).replace("shp", "gdb"), "CURRENT")
    except:
        print "数据库已经建好"
        
    out_dataset_path = Geodatabase
    out_name = os.path.basename(ifc).replace(".shp", "")  #数据集名称
#     print "out_name:",out_name
    print "数据集名称:",out_name
    #创建数据集
    arcpy.CreateFeatureDataset_management(out_dataset_path, out_name, Coordinate_System)

    #向数据集导入shp
    in_features = ifc  #导入的shp名称
    out_path = os.path.join(Geodatabase,out_name)   #shp导入的数据集位置
    #print u"shp导入的数据集位置:" + str(out_path)
    out_name = os.path.basename(ifc).replace(".shp", "") + "_ToPo"    #导入后shp的名称
    #print u"导入后shp的名称:" + str(out_name)
    arcpy.FeatureClassToFeatureClass_conversion (in_features, out_path, out_name)


    # Process: Create Topology
    Topo_name =os.path.basename(ifc).replace(".shp", "") + "_ToPology" #拓扑结构的名称
    #print u"拓扑结构的名称:" + str(Topo_name)
    arcpy.CreateTopology_management(out_path, Topo_name, "")   #zhiduo_tp  拓扑结构

    # Process: Add Feature Class To Topology
    Topology = os.path.join(out_path,Topo_name)  # 拓扑结构的路径
    ##print u"拓扑结构的路径:" + str(Topology)
    ToPoShp = os.path.join(out_path,out_name)    # 要做拓扑的数据集里的shp
    ##print u"要做拓扑的数据集里的shp:" + str(ToPoShp)
    arcpy.AddFeatureClassToTopology_management(Topology, ToPoShp, "1", "1")

    # Process: Add Rule To Topology
    arcpy.AddRuleToTopology_management(Topology, "Must Not Have Gaps (Area)", ToPoShp, "", "", "")
    #print u"正在添加 Must Not Have Gaps 规则"
    arcpy.AddRuleToTopology_management(Topology, "Must Not Overlap (Area)", ToPoShp, "", "", "")
    #print u"正在添加 Must Not Overlap 规则"

    # Process: Validate Topology
    try:
        arcpy.ValidateTopology_management(Topology, "true")
    except:
        print str(ifc) + "的拓扑未成功验证，请人工重新建立拓扑。"

    print "拓扑验证完成" + '\n'
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
    ff = raw_input("请按Enter键结束...")