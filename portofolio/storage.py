
from cloudinary_storage.storage import MediaCloudinaryStorage


class SenDevCloudinaryStorage(MediaCloudinaryStorage):
    """
    Penyimpanan Cloudinary untuk SenDev.

    - JPG, PNG, WEBP: image
    - PDF (CV): raw
    """

    def _get_resource_type(self, name):
        if str(name).lower().endswith(".pdf"):
            return "raw"

        return "image"
