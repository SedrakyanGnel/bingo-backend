from django.contrib import admin
from .models import ScanEvent

@admin.register(ScanEvent)
class ScanEventAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "bin", "trash_type", "confidence", "created_at")
    list_filter = ("trash_type", "created_at")
    search_fields = ("user__username", "bin__id")
    readonly_fields = ("image_tag",)

    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height:120px;" />'
        return "-"
    image_tag.allow_tags = True
    image_tag.short_description = "Photo"