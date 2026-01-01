from django.urls import path

from .views import FormiCreateView, FormiFieldComponentView, FormiListView

urlpatterns = [
    path("", FormiListView.as_view(), name="formi_list"),
    path("/create", FormiCreateView.as_view(), name="formi_create"),
    path(
        "/components/field",
        FormiFieldComponentView.as_view(),
        name="formi_field_component",
    ),
]
