import mimetypes


async def upload_to_s3(
    s3_client,
    bucket: str,
    file_name: str,
    body: bytes,
    content_disposition: str):
    mime_type, _ = mimetypes.guess_type(file_name)
    upload_params = {
        "Bucket": bucket,
        "Key": file_name,
        "ContentType": mime_type,
        "Body": body,
        "ContentDisposition": content_disposition,
    }
    await s3_client.put_object(**upload_params)
