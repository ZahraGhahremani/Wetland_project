import os
import boto3

def addMeta_final(memfile_io, file_bucket, dst, aws_access_key_id, aws_secret_access_key, s3_bucket_name):
    """A function for saving the output on S3

    Args:
        memfile_io: BytesIO object
        file_bucket (str): name of the tile
    """
    
    output_name = os.path.join('22Modified_'+file_bucket[25:-4]+'.tif')
    
    
    output_name = 'GIS_processing/' + output_name
    
    # Upload the in-memory TIFF file to AWS S3
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='us-west-2'
    )

    s3_client = session.client('s3')
    try:
        memfile_io.seek(0)
        s3_client.put_object(Bucket=s3_bucket_name, Key=output_name, Body=memfile_io.getvalue())
        print("TIFF file uploaded successfully to AWS S3.")
    except Exception as e:
        print(f"Error uploading the TIFF file to AWS S3: {str(e)}")
    finally:
        memfile_io.close()
    return dst