import  rasterio 
from rasterio.io import MemoryFile

def cropMask(input_raster_path, mask_geometry_gpd, meta_segment):
    """A function to crop the masks based on the predicted raster

    Args:
        input_raster_path (str): path to the mask
        mask_geometry_gpd (_type_): geometry of the predicted raster (segmentation)
        meta_segment (meta) : Segmentation meta

    Returns:
        _type_: _description_
    """

    with rasterio.open(input_raster_path) as input_raster_src:
        # Cropping raster with the mask
        output_image, transformed = rasterio.mask.mask(input_raster_src, mask_geometry_gpd.loc[0], crop=True, all_touched=True, filled=True)
        out_meta = input_raster_src.profile
        out_meta.update({"height": output_image.shape[1],"width": output_image.shape[2], "transform": transformed})
        memfile = MemoryFile()
        with memfile.open(driver= out_meta['driver'],
                dtype=out_meta['dtype'],
                nodata= out_meta['nodata'],
                width= out_meta['width'],
                height= out_meta['height'],
                count= out_meta['count'],
                crs= meta_segment['crs'],
                transform= out_meta['transform'],
                # affine = out_meta['affine']
                ) as dst:
            dst.write(output_image)

    return dst      

