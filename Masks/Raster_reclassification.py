import numpy as np
import rasterio
import sys

# Functions for raster reclassification and saving geotiff
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

def main(argv):
   """_summary_
   This function reclassify the raster dataset from CDL (https://nassgeodata.gmu.edu/CropScape/) into crop and no crop 
   Args:
      raster_path (str): path of the input raster dataset
      out_path (str) : path of the output raster dataset
   """
   raster_path = str(argv[0])
   out_path = str(argv[1])
   with rasterio.open(raster_path) as src:
   # Read the raster data as a numpy array
      raster_array = src.read(1)
   crop = raster_array.copy()
   crop[(crop > 60)|(crop < 1)&(crop < 66)|(crop > 80)&(crop < 196)|(crop > 255)] = 0
   crop[crop > 0] = 1
   crop[crop <= 0] = 0
   saveTiff(crop,raster_path, out_path)
   return crop


if __name__ == "__main__":
   main(sys.argv[1:])