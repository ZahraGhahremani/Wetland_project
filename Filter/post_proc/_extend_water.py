
import numpy as np
from skimage.morphology import disk, dilation, closing
from skimage.morphology import disk, erosion, closing

# A function for joining up the waterways
def joinWtr(clipped_array):
    """Function for joining up the waterways
    Args:
        clipped_array (np.array): input clipped back array 
    """
    wtr = clipped_array.copy()
    wtr[(wtr != 1)] = 0  # Water class binary
    aqua = clipped_array.copy()
    aqua[aqua != 2] = 0  # Aquatic class binary
    other_classes = clipped_array.copy()  # Class 3 to 6
    other_classes[other_classes < 3] = 0
    # Dilation
    kernel = disk(3.5)
    dilated_mask = dilation(wtr, kernel)
    filled_mask = closing(dilated_mask, kernel)
    # Erosion
    kernel = disk(2.75)
    eroded_mask = erosion(filled_mask, kernel)
    # Perform closing to fill gaps and smooth out the river boundaries
    filled_mask_erosion = closing(eroded_mask, kernel)
    aqua_bed = aqua.copy()
    aqua_bed = np.where(aqua_bed == 0, 1, 0)
    aqua_erosion = np.multiply(aqua_bed, filled_mask_erosion)
    aqua_wtr = np.sum([aqua_erosion, aqua], axis = 0)
    no_water = other_classes.copy()
    no_water = np.where(no_water == 0, 1, 0)
    mask_water = np.multiply(no_water, aqua_wtr)
    final_array = np.sum([other_classes, mask_water], axis = 0)
    return final_array