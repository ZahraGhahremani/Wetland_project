import  rasterio 
from rasterio.io import MemoryFile
from rasterio.warp import reproject, calculate_default_transform, CRS, Resampling

def resampleRaster(raster_src, seg_src):
    """A function for resampling

    Args:
        raster_src: src of mask
        seg_src : src of segmentation
    
    """
    with rasterio.open(raster_src.name) as dataset_src:
        dataset_meta = dataset_src.meta
        target_meta = seg_src.meta
        transform, width, height = calculate_default_transform(dataset_src.crs, seg_src.crs, seg_src.width, seg_src.height, *dataset_src.bounds)
        output_profile = dataset_src.profile
        output_profile.update(transform=transform, width=width, height=height)
        memfile = MemoryFile()
        rst = memfile.open(driver= dataset_meta['driver'],
            dtype=dataset_meta['dtype'],
            nodata= dataset_meta['nodata'],
            width= target_meta['width'],
            height= target_meta['height'],
            count= dataset_meta['count'],
            crs= dataset_meta['crs'],
            transform= transform # new_transform
            )
        for i in range(1, dataset_src.count+1):
            reproject(
                source=rasterio.band(dataset_src, i),
                destination=rasterio.band(rst, i),
                src_transform=dataset_src.transform,
                src_crs=dataset_src.crs,
                dst_transform=transform,
                dst_crs=dataset_src.crs,
                resampling=rasterio.enums.Resampling.nearest)
    return rst
    
