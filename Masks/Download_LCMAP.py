# Import Packages
import geopandas as gp
import os
import rasterio as rio
import pandas as pd
import pandas as pd
import numpy as np
import sys
import rasterio.mask

# code from https://code.usgs.gov/lcmap/1a_lcmap_direct_access/-/tree/main  -Modified by Zahra Ghahremani

# Set up Lookup Tables for region, version, and products
region_dict = {'CU': 'conus', 'HI': 'hawaii'}
rv_dict = {'CU':['version_13', 'V13'], 'HI': ['version_10', 'V10']}
prod_dict = {'LCPRI': 'primary-landcover', 'LCSEC': 'secondary-landcover', 'LCPCONF': 'primary-confidence',
             'LCSCONF': 'secondary-confidence', 'LCACHG': 'cover-change', 'SCTIME': 'change-day', 'SCMAG': 'change-magnitude',
             'SCLAST': 'spectral-lastchange', 'SCSTAB': 'spectral-stability', 'SCMQA': 'model-quality'}

# Define base URL
b_url = "https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/lcmap/public/full_extent_downloads/"  # Base URL

# Define function
def main(argv):
    roi = str(argv[0])  # Shapefile of region of interest
    region = str(argv[1]) # Use 'CU' for Conterminous US or 'HI' for Hawaii
    years = [2010]
    products = ['LCPRI']
    # Below is a list of all products, remove hash if all products are desired
    # products = ['LCPRI', 'LCSEC', 'LCACHG', 'LCSCONF', 'LCPCONF', 'SCTIME', 'SCMAG', 'SCLAST', 'SCMQA', 'SCSTAB'] 
    # Verify region
    region = region.upper()
    if region not in ["CU", "HI"]:
        print('Invalid region submitted. Options include "CU" for Conterminous United States and "HI" for Hawaii.')
        return 

    # Open ROI
    try:
        ROI = gp.read_file(roi)
    except:
        print(f'Unable to open {roi}. Valid file types include GeoJSON and Shapefile. Also, verify the location of {roi}.')
        return
    roi_name = os.path.basename(roi).rsplit(".", 1)[0]

    # Create output directory
    out_dir = './outputs/'
    os.makedirs(out_dir, exist_ok=True)

    # Loop through each year and each product
    for year in years:
        # Verify year
        if region == 'CU' and year not in np.arange(1985, 2022, 1): 
            print('Desired year is outside of the range (1985-2021)')
            continue
        elif region == 'HI' and year not in np.arange(2000, 2021, 1): 
            print('Desired year is outside of the range (2000-2020)')
            continue

        for product in products:
            # Verify product
            if product not in prod_dict.keys():
                print("Invalid product shortname. Valid names are:")
                for p in prod_dict.keys(): print(p)
                continue
            # Construct URL
            prod_url = f"LCMAP_{region}_{year}_{rv_dict[region][1]}_{product}"
            url = f"{b_url}{rv_dict[region][0]}/{prod_dict[product]}_{region_dict[region]}_year_data/{prod_url}/{prod_url}.tif"
            
            # Open and extract data
            try:
                with rio.open(url) as lcmap:
                    try:
                        lcmap_data, lcmap_transform = rio.mask.mask(lcmap, [ROI.to_crs(lcmap.crs)['geometry'][0]], crop=True)
                    except (rio.errors.WindowError, ValueError):
                        print(f"{roi} did not intersect {region_dict[region]}. Verify the ROI and please try again.")
                        return
                    # Export with colormap
                    meta = lcmap.meta
                    try:
                        colors = lcmap.colormap(1)
                    except:
                        # Create custom colormap for Confidence products
                        if 'CONF' in product:
                        # Loop through all values (0-255) and define a black-white stretch for initial classifier results
                            conf_colors = ["#000000"]
                            start_value = 70
                            for idx in range(1, 101):
                                conf_colors.append(f'#{start_value:02x}{start_value:02x}{start_value:02x}')
                                if idx in [4,12,20,27,35,43,51,58,66,74,81,89,97]:
                                    start_value += 1
                                else:
                                    start_value += 2

                            # Assign discrete colormap for secondary analysis and rule-based approach results
                            for idx in range(101, 200):
                                if idx == 151:
                                    conf_colors.append('#7300a8')
                                elif idx == 152:
                                    conf_colors.append('#c533ff')
                                else:
                                    conf_colors.append('#ffffff')  # Not used
                            for idx in range(200, 256):
                                conf_colors.append('#d95f02')
                            colors = {}
                            for j,c in enumerate(conf_colors):
                                colors[j] = tuple(int(c.lstrip('#')[i:i + 6 // 3], 16) for i in range(0, 6, 6 // 3)) + (255,)

                        # Retrieve color map for SCMQA Product
                        elif 'SCLAST' not in product and 'SCSTAB' not in product:
                            for retry in range(0,3):
                                try:
                                    colormap_url = "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/"
                                    color = pd.read_csv(f'{colormap_url}LCMAP_{product}.txt', header=None)
                                    colors = {}
                                    for c in color.iterrows():
                                        colors[c[1][0]] = (c[1][1],c[1][2],c[1][3],c[1][4])
                                    break
                                except:
                                    print(f"Unable to access colormap file, attempt {retry+1}/3")
                                    colors = None

            except rio.errors.RasterioIOError as e:
                if str(e).startswith('Read or write failed'):
                    print('Unable to subset data using this vector file. Please try a different vector file.')
                else:
                    print(f"Unable to access {url} Please try again later.")
                continue
                
            # Update metadata and create output filename
            meta.update({'width': lcmap_data.shape[2], 'height': lcmap_data.shape[1], 'transform': lcmap_transform})
            out_file_name = f"{roi_name.replace(' ', '_').replace(',','')}_{prod_url}.tif"
            out_file_path = os.path.join(out_dir, out_file_name)

            # Export subset as GeoTIFF
            with rio.open(out_file_path, 'w', **meta, compress='lzw', tiled=True, blockxsize=256, blockysize=256) as out_file:
                out_file.write(lcmap_data)
                if product is not 'SCMAG' and product is not 'SCLAST' and product is not 'SCSTAB':
                    try:
                        out_file.write_colormap(1, colors)
                    except:
                        pass

            # Print results
            print(f"Completed processing of {year} {product} in {roi_name}, available at {out_file_path}")
            
if __name__ == "__main__":
    main(sys.argv[1:])