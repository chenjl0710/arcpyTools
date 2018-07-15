import arcpy
arcpy.env.workspace=r"G:\ȫ����\e"#դ���ļ����ļ���·��
rasters = arcpy.ListRasters("*", "img")#��������Ӱ���ʽ�Զ���tif����img
#Coordinate_System������ͶӰ��
Coordinate_System = "PROJCS['WGS_1984_UTM_Zone_53N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',135.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"
for ras in rasters:
    print str(ras)
    arcpy.DefineProjection_management(ras, Coordinate_System)
print("OK")
