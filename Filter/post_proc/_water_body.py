import numpy as np
import cv2

# A function to fill in the water bodies
def waterBody(final_array):
    """Function for filling in the water bodies
    Args:
        final_array (np.array): input an array 
    """
    wtr_class = final_array.copy()
    wtr_class[(wtr_class > 2)] = 0
    wtr_class[(wtr_class == 2)] = 1
    # Ensure wtr_class is in the correct format (CV_8UC1)
    wtr_class = wtr_class.astype(np.uint8)
    # Find contours in the binary image
    contours, _ = cv2.findContours(wtr_class, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Define aspect ratio threshold to exclude straight contours
    max_aspect_ratio = 3.3  # Adjust as needed
    # Create a mask for valid contours (excluding straight contours)
    valid_mask = np.zeros_like(wtr_class, dtype=np.uint8)
    for contour in contours:
        if len(contour) >= 5:  # Fitting requires at least 5 points
            ellipse = cv2.fitEllipse(contour)
            major_axis = max(ellipse[1])
            minor_axis = min(ellipse[1])
            if minor_axis != 0:  # Check for non-zero minor axis
                aspect_ratio = major_axis / minor_axis
                if aspect_ratio < max_aspect_ratio:
                    cv2.drawContours(valid_mask, [contour], -1, 1, thickness=cv2.FILLED)  # Use 1 instead of 255 for contours
    seg_copy = final_array.copy()
    seg_copy[(final_array > 0)] = 0
    seg_copy[(final_array == 0)] = 1
    seg_array = np.multiply(seg_copy, valid_mask)
    seg_array = np.add(seg_array, final_array)
    return seg_array