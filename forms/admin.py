from django.contrib import admin

from .models import (
    FieldPreset,
    FieldType,
    Form,
    FormField,
    FormFieldResponse,
    FormFieldRule,
    FormResponse,
)

# Register your models here.
admin.site.register(Form)
admin.site.register(FormField)
admin.site.register(FormFieldResponse)
admin.site.register(FormFieldRule)
admin.site.register(FormResponse)
admin.site.register(FieldPreset)
admin.site.register(FieldType)
