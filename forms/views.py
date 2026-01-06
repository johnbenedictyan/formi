from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from .forms import FormForm
from .models import Form, FormField


# Create your views here.
class FormListView(ListView):
    model = Form
    template_name = "form_list.html"


class FormCreateView(CreateView):
    form_class = FormForm
    model = Form
    template_name = "form_create_start.html"


class FormUpdateView(UpdateView):
    model = Form
    template_name = "form_update.html"


class FormDetailView(DetailView):
    model = Form
    template_name = "form_detail.html"


@method_decorator(csrf_exempt, name="dispatch")
class FormFieldComponentView(TemplateView):
    template_name = "form_field_component.html"

    def delete(self, request, *args, **kwargs):
        return HttpResponse("", status=200)


class FormCreatePresetView(RedirectView):
    url = reverse_lazy("Form_list")

    def get(self, request, *args, **kwargs):
        preset = self.kwargs["preset"]
        print(preset)

        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class FormFieldTemplateView(DetailView):
    model = FormField

    def get_template_names(self):
        field_type = (
            self.object.field_type
            and self.object.field_type.key  # TODO: Is this troublesome?
        ) or self.object.preset.field_type.key
        return [f"fields/{field_type}.html"]

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
