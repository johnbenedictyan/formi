from django.views.generic import ListView
from .models import Formi


# Create your views here.
class FormiListView(ListView):
    model = Formi
    template_name = "form_list.html"
