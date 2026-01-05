from django.urls import path

from .views import (
    FormCreatePresetView,
    FormCreateView,
    FormDetailView,
    FormFieldComponentView,
    FormListView,
    FormUpdateView,
)

urlpatterns = [
    path("", FormListView.as_view(), name="form_list"),
    path(
        "create/presets/<slug:preset>",
        FormCreatePresetView.as_view(),
        name="form_create_preset",
    ),
    path("create", FormCreateView.as_view(), name="form_create"),
    path("<int:pk>/update", FormUpdateView.as_view(), name="form_update"),
    path("<int:pk>", FormDetailView.as_view(), name="form_detail"),
    path(
        "components/field",
        FormFieldComponentView.as_view(),
        name="form_field_component",
    ),
]
