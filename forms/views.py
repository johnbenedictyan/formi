from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView

from .forms import FormiForm
from .models import Formi


# Create your views here.
class FormiListView(ListView):
    model = Formi
    template_name = "form_list.html"


class FormiCreateView(CreateView):
    form_class = FormiForm
    model = Formi
    template_name = "form_create.html"


@method_decorator(csrf_exempt, name="dispatch")
class FormiFieldComponentView(TemplateView):
    template_name = "form_field_component.html"

    def delete(self, request, *args, **kwargs):
        return HttpResponse("", status=200)
