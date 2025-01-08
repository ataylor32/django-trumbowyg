from django.conf import settings

EXTRA_MEDIA = getattr(settings, "TRUMBOWYG_EXTRA_MEDIA", {})
UPLOAD_PATH = getattr(settings, "TRUMBOWYG_UPLOAD_PATH", "uploads/")
THUMBNAIL_SIZE = getattr(settings, "TRUMBOWYG_THUMBNAIL_SIZE", None)
TRANSLITERATE_FILENAME = getattr(settings, "TRUMBOWYG_TRANSLITERATE_FILENAME", False)
SEMANTIC = getattr(settings, "TRUMBOWYG_SEMANTIC", "true")
