import os

import pandas as pd 
import numpy as np
import geopandas as gpd
from skimage import io

from osgeo import gdal
from osgeo import osr
from osgeo.gdalconst import *


tiff_path  = "../data/new_info/"


def get_array_row_col(gdal_obj):
    band = gdal_obj.GetRasterBand(1)
    row = gdal_obj.RasterYSize
    col = gdal_obj.RasterXSize

    array = band.ReadAsArray(0,0,col,row)

    return array, row, col



def read_process_info():
    '''
    reads info and turns it into numpy arrays,
    fixes missing values
    
    inputs: nothing, it does things
    outputs: nothing, it produces the information 

    '''
    # dems 

    gdal.AllRegister()

    tif_lst = ["Beira_DEM_Lidar_Post", "Beira_DEM_Lidar_Pre-project",
    "pre_10_year", "pre_5_year", "post_10_year", "post_5_year"]

    tif_final = ["pre_10_year", "pre_5_year", "post_10_year", "post_5_year"]

    tif_files = {}
    tif_arrays = {}


    for tif in tif_lst: 
        print(tiff_path + tif + ".tif")
        file = gdal.Open(tiff_path + tif + ".tif")
        tif_files[tif] = file
        tif_arrays[tif] = get_array_row_col(file)
        
    
    # Creating the arrays: 

    fin_arr = {}

    fin_arr["pre_10_year"] = tif_arrays["Beira_DEM_Lidar_Pre-project"][0] - tif_arrays["pre_10_year"][0]
    fin_arr["pre_5_year"]  = tif_arrays["Beira_DEM_Lidar_Pre-project"][0] - tif_arrays["pre_5_year"][0]

    fin_arr["post_10_year"]  = tif_arrays["Beira_DEM_Lidar_Post"][0] - tif_arrays["post_10_year"][0]
    fin_arr["post_5_year"]  =  tif_arrays["Beira_DEM_Lidar_Post"][0] - tif_arrays["post_5_year"][0]


    for thing_name in tif_final:
        get_driver_save_file(thing_name, tif_arrays[thing_name][2], tif_arrays[thing_name][1],tif_files, fin_arr)

    return None


#Taken and modified from https://gis.stackexchange.com/questions/37238/writing-numpy-array-to-raster-file
def get_driver_save_file(thing_name, cols, rows, tif_files, fin_arr):

    indDs = tif_files[thing_name] 
    if indDs is None:
        print ('Could not create indDs :(')
    driver = indDs.GetDriver()

    if driver is None:
        print ('Could not create driver :(')

    outDs = driver.Create(tiff_path + thing_name + "_out.tif", cols, rows, 1, gdal.GDT_Float32)



    if outDs is None:
        print ('Could not create outputfile :(')


    outBand = outDs.GetRasterBand(1)
    outBand.WriteArray(fin_arr[thing_name], 0, 0)
    outBand.FlushCache()
    outBand.SetNoDataValue(-99999)

    outDs.SetGeoTransform(indDs.GetGeoTransform())
    outDs.SetProjection(indDs.GetProjection())
    
    outDs = None

    del outDs




if __name__ == "__main__":
    read_process_info()








    
