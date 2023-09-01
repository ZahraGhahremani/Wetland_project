import numpy as np
import  rasterio 
from rasterio.io import MemoryFile

# A function for reclassifying the model output into water and No water 
def waterReclass(input_array, meta):
    """Function for reclassifying the model's output into water and no water class (1 and 0)
    Args:
        input_array (np.array): input raster array (segmentation)
        meta (dic) : meta data of the input rater array
    """

    water_raster = input_array.copy()
    water_raster[(water_raster != 1)] = 0
    
    # Expanding the dimension 
    water_src = np.expand_dims(water_raster, axis=0)
    
    # Create a MemoryFile object (this is because we don't want to have a physical file on disk)
    memfile = MemoryFile()
    with memfile.open(driver= meta['driver'],
            dtype=meta['dtype'],
            nodata= meta['nodata'],
            width= meta['width'],
            height= meta['height'],
            count= meta['count'],
            crs= meta['crs'],
            transform= meta['transform'],
            # affine = meta['affine']
            ) as dst:
        dst.write(water_src)
    return dst

# reclassify to aquatic bed and No aquatic bed function
def aquaReclass(input_array, meta):
    """Function for reclassifying the model's output into aquatic bed and no aquatic bed (1 and 0)
    Args:
        input_array (np.array): input raster array
        meta (dic) : meta data of the input rater array
    """
    aqua_raster = input_array.copy()
    aqua_raster[(aqua_raster != 2)] = 0
    aqua_raster[(aqua_raster == 2)] = 1
    aqua_src = np.expand_dims(aqua_raster, axis=0)
    # Create a MemoryFile object
    memfile = MemoryFile()
    with memfile.open(driver= meta['driver'],
            dtype=meta['dtype'],
            nodata= meta['nodata'],
            width= meta['width'],
            height= meta['height'],
            count= meta['count'],
            crs= meta['crs'],
            transform= meta['transform'],
            # affine = meta['affine']
            ) as dst:
        dst.write(aqua_src)
    return dst


# reclassify to emergent and No emergent function
def emergReclass(input_array, meta):
    """Function for reclassifying the model's output into emergent and no emergent (1 and 0)
    Args:
        input_array (np.array): input raster array
        meta (dic) : meta data of the input rater array
    """
    emerg_raster = input_array.copy()
    emerg_raster[(emerg_raster != 3)] = 0
    emerg_raster[(emerg_raster == 3)] = 1
    emerg_src = np.expand_dims(emerg_raster, axis=0)
    # Create a MemoryFile object
    memfile = MemoryFile()
    with memfile.open(driver= meta['driver'],
            dtype=meta['dtype'],
            nodata= meta['nodata'],
            width= meta['width'],
            height= meta['height'],
            count= meta['count'],
            crs= meta['crs'],
            transform= meta['transform'],
            # affine = meta['affine']
            ) as dst:
        dst.write(emerg_src)

    return dst


# reclassify to Scrub and No Scrub function
def scrubReclass(input_array, meta):
    """Function for reclassifying the model's output into shrub scrub and no shrub scrub (1 and 0)
    Args:
        input_array (np.array): input raster array
        meta (dic) : meta data of the input rater array
    """
    scrub_raster = input_array.copy()
    scrub_raster[(scrub_raster != 4)] = 0
    scrub_raster[(scrub_raster == 4)] = 1
    scrub_src = np.expand_dims(scrub_raster, axis=0)
    # Create a MemoryFile object
    memfile = MemoryFile()
    with memfile.open(driver= meta['driver'],
            dtype=meta['dtype'],
            nodata= meta['nodata'],
            width= meta['width'],
            height= meta['height'],
            count= meta['count'],
            crs= meta['crs'],
            transform= meta['transform'],
            # affine = meta['affine']
            ) as dst:
        dst.write(scrub_src)
    return dst

# reclassify to forest and No forest function
def forestReclass(input_array, meta):
    """Function for reclassifying the model's output into forest and no forest (1 and 0)
    Args:
        input_array (np.array): input raster array
        meta (dic) : meta data of the input rater array
    """
    forest_raster = input_array.copy()
    forest_raster[(forest_raster != 5)] = 0
    forest_raster[(forest_raster == 5)] = 1
    forest_src = np.expand_dims(forest_raster, axis=0)
    # Create a MemoryFile object
    memfile = MemoryFile()
    with memfile.open(driver= meta['driver'],
            dtype=meta['dtype'],
            nodata= meta['nodata'],
            width= meta['width'],
            height= meta['height'],
            count= meta['count'],
            crs= meta['crs'],
            transform= meta['transform'],
            # affine = meta['affine']
            ) as dst:
        dst.write(forest_src)
    return dst


# reclassify to shoreline and No shoreline function
def shoreReclass(input_array, meta):
    """Function for reclassifying the model's output into shoreline and no shoreline (1 and 0)
    Args:
        input_array (np.array): input raster array
        meta (dic) : meta data of the input rater array
    """
    shore_raster = input_array.copy()
    shore_raster[(shore_raster != 6)] = 0
    shore_raster[(shore_raster == 6)] = 1
    shore_src = np.expand_dims(shore_raster, axis=0)
    # Create a MemoryFile object
    memfile = MemoryFile()
    with memfile.open(driver= meta['driver'],
            dtype=meta['dtype'],
            nodata= meta['nodata'],
            width= meta['width'],
            height= meta['height'],
            count= meta['count'],
            crs= meta['crs'],
            transform= meta['transform'],
            # affine = meta['affine']
            ) as dst:
        dst.write(shore_src)
    return dst


