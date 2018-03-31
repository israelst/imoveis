from django.contrib import admin

from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile

from cms.models import Place


class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(150, 150)]


def cached_admin_thumb(instance):
    cached = ImageCacheFile(AdminThumbnailSpec(instance.picture))
    cached.generate()
    return cached


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('details', 'thumbnail',)
    thumbnail = AdminThumbnail(image_field=cached_admin_thumb)


admin.site.register(Place, PlaceAdmin)
