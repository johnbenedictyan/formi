from django.urls import path

from .views import (
    FormCreatePresetView,
    FormCreateView,
    FormFieldComponentView,
    FormListView,
)

urlpatterns = [
    path("", FormListView.as_view(), name="form_list"),
    path(
        "create/presets/<slug:preset>",
        FormCreatePresetView.as_view(),
        name="form_create_preset",
    ),
    path("create", FormCreateView.as_view(), name="form_create"),
    path(
        "components/field",
        FormFieldComponentView.as_view(),
        name="form_field_component",
    ),
]
