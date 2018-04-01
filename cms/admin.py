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
    thumbnail = AdminThumbnail(image_field=cached_admin_thumb)
    list_display = ('details', 'thumbnail',)
    readonly_fields = ('thumbnail', 'picture', 'details', 'size', 'price')
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(PlaceAdmin, self).changeform_view(request, object_id, extra_context=extra_context)


admin.site.register(Place, PlaceAdmin)
