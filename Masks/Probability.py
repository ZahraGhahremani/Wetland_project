import numpy as np
import rasterio
import sys

# Functions for saving geotiff
def saveTiff(raster, raster_path, out_path):
    """_summary_
    This function saves geotiff
    Args:
        raster (np array) : input raster
        raster_path (str): path of the input raster dataset
        out_path (str): path of the output raster dataset
    """
    raster = np.expand_dims(raster, axis=0)
    with rasterio.open(raster_path) as src:
        out_meta = src.profile
        out_meta.update({"height": raster.shape[1],"width": raster.shape[2]})
    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(raster)
        
# Function for creating probability raster
def main(argv):
    """_summary_
    A function that uses 10 years data and creates a probability raster
    Args:
        out_path (str) : path of the output raster dataset
    """
    # Create a list of files from which you want to create a probability raster
    path_list = ['/mnt/c/Lynker/Beaver_project/CDL_CropSpace/Downloaded_images/cdl-2012_crop.tif', 
            '/mnt/c/Lynker/Beaver_project/CDL_CropSpace/Downloaded_images/cdl-2013_crop.tif',
            ]
    out_path = str(argv[0])
    with rasterio.open(path_list[0]) as src:
        raster_array = src.read(1)
        size = (raster_array.shape[0], raster_array.shape[1])
    storage = np.zeros(size)
    for path in path_list:
        with rasterio.open(path) as src:
        # Read the raster data as a numpy array
            image = src.read(1)    
        storage = np.add(storage, image)
    storage *= 10
    saveTiff(storage, path_list[0], out_path)
    return storage

if __name__ == "__main__":
    main(sys.argv[1:])