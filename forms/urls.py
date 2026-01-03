from django.urls import path

from .views import (
    FormiCreatePresetView,
    FormiCreateView,
    FormiFieldComponentView,
    FormiListView,
)

urlpatterns = [
    path("", FormiListView.as_view(), name="formi_list"),
    path(
        "create/presets/<slug:preset>",
        FormiCreatePresetView.as_view(),
        name="formi_create_preset",
    ),
    path("create", FormiCreateView.as_view(), name="formi_create"),
    path(
        "components/field",
        FormiFieldComponentView.as_view(),
        name="formi_field_component",
    ),
]
