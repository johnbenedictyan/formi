from django.urls import path

from .views import FormiListView

urlpatterns = [
    path("", FormiListView.as_view(), name="formi_list"),
]
