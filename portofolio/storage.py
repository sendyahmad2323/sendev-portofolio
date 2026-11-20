"""Cloudinary storage for both images and PDF resumes, with a single backend.

Only enabled when CLOUDINARY_URL is present in Django settings. Existing ImageField
and FileField declarations keep working without schema or migration changes.
"""
from cloudinary_storage.storage import MediaCloudinaryStorage


class SenDevCloudinaryStorage(MediaCloudinaryStorage):
    """Upload photos as Cloudinary 'image' and PDF documents as 'raw'."""

    def _get_resource_type(self, name):
        if str(name).lower().endswith('.pdf'):
            return 'raw'
        return 'image'
