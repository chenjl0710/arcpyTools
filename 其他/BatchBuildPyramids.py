# -*- coding: cp936 -*-

import os,arcpy,time
import multiprocessing as mp

ISOTIMEFORMAT='%Y-%m-%d %X'
def BuildPyramids(Rst):
    print u"���ڹ���%s�Ľ�������"%Rst
    arcpy.BuildPyramids_management(Rst,"29","NONE","NEAREST","DEFAULT","80","SKIP_EXISTING")
    print u"%s�Ľ�����������ɡ�"%Rst
    
    
if __name__ == "__main__":
    Start_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
    print Start_time
    '''
    pool = mp.Pool(processes = 1)
    ImgsFolder = r"D:\testP"
    arcpy.env.workspace = ImgsFolder
    rasters = arcpy.ListRasters()
#     imgList = []
    for rst1 in rasters:
        rst1 = os.path.join(ImgsFolder,rst1)
#     print imgList
        pool.apply_async(BuildPyramids,(rst1,))
    
    pool.close()
    pool.join()
    '''
    ImgsFolder = r"F:\����GF2\gf2"
    arcpy.env.workspace = ImgsFolder
    rasters = arcpy.ListRasters()
    for rst1 in rasters:
        BuildPyramids(rst1)
    
    End_time = time.strftime(ISOTIMEFORMAT,time.localtime(time.time()))
    print End_time