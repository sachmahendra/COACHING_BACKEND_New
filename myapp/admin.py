from django.contrib import admin
from .models import *

admin.site.register(customer)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(DownloadCategory)
admin.site.register(DownloadDocument)
admin.site.register(Student)
# admin.site.register(OTPRequest)

@admin.register(OTPRequest)
class OTPRequestAdmin(admin.ModelAdmin):
    list_display = ("mobile_number", "code", "verified", "used", "created_at")
    search_fields = ("mobile_number", "code")
    list_filter = ("verified", "used", "created_at")
    ordering = ("-created_at",)