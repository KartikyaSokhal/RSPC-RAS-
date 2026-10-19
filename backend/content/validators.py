from pathlib import Path
import warnings
from django.core.exceptions import ValidationError
from PIL import Image


def validate_image(uploaded):
    if uploaded.size > 5 * 1024 * 1024:
        raise ValidationError('Images must be at most 5 MB.')
    try:
        uploaded.seek(0)
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            image = Image.open(uploaded)
            if image.format not in ('PNG', 'JPEG', 'WEBP') or image.width * image.height > 16000000:
                raise ValidationError('Use a PNG, JPEG or WebP image of at most 16 megapixels.')
            image.verify()
    except (OSError, ValueError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise ValidationError('The image could not be validated.') from None
    finally:
        uploaded.seek(0)


def validate_pdf_upload(uploaded):
    from django.conf import settings
    if not uploaded.size or uploaded.size > settings.PDF_MAX_BYTES or Path(uploaded.name).suffix.lower() != '.pdf':
        raise ValidationError('Upload a PDF of at most 20 MB.')
    if getattr(uploaded, 'content_type', 'application/pdf') not in ('application/pdf', 'application/octet-stream'):
        raise ValidationError('The uploaded type must be PDF.')
    uploaded.seek(0); signature = uploaded.read(5); uploaded.seek(0)
    if signature != b'%PDF-': raise ValidationError('The file is not a PDF.')
