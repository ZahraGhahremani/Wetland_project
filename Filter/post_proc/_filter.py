import  rasterio 
import numpy as np

def classesFilter(predict_raster, mask2, mask3):
    """ Function for filtering a tile with different masks (LCMAP and CDL)

    Args:
        predic_raster (np.array): input raster that you want to filter (segmentation)
        mask2 (np.array): urban mask (LCMAP_crop band 1:developed)
        mask3 (np.array): agriculture mask (cdl_crop)
        meta_predicted (dic) : metadata of the predicted map
    """
    # Since LCMAP and CDL masks are probablity masks, we need to consider a threshold 
    
    thresh_dev = 20  #This removes misclassified areas that were urban areas in reality for more than 2 years
    thresh_cdl = 20  #This removes misclassified areas that were crop lands in reality for more than 2 year
    
    # Reading masks
    mask2_arr = mask2.read(1)
    mask3_arr = mask3.read(1)
    with rasterio.open(predict_raster.name) as segmentation_src:
        predict_raster = segmentation_src.read(1)
        
    # False positive (if(input_raster == 1) and (developed > 50 or cdl > 50))
    dev_mask = mask2_arr.copy()
    dev_mask[dev_mask <= thresh_dev] = 0
    dev_mask[dev_mask > thresh_dev] = 1

    cdl_mask = mask3_arr.copy()
    cdl_mask[cdl_mask <= thresh_cdl] = 0
    cdl_mask[cdl_mask > thresh_cdl] = 1
    
    dev_cdl = np.logical_or(dev_mask, cdl_mask)
    
    # Convert a boolean array to an int array
    dev_cdl = dev_cdl * 1
    fp = np.logical_and(dev_cdl, predict_raster)
    
    # Convert a boolean array to an int array
    fp = fp * 1
    count_fp = sum(sum(fp))
    print('count_fp', count_fp)
    
    # Apply fp masks
    predict_raster = np.subtract(predict_raster, fp)
    return predict_raster