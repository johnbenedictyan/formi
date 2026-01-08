import uuid
from itertools import chain

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class FieldType(models.Model):
    key = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    default_label = models.CharField(max_length=100)
    default_help_text = models.CharField(max_length=300, blank=True)
    default_validations = models.JSONField(default=dict, blank=True)

    supports_choices = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Field Type")
        verbose_name_plural = _("Field Types")

    def __str__(self):
        return self.default_label


def create_default_order_dict():
    return {"xs": 1, "sm": 1, "md": 1, "lg": 1, "xl": 1, "2xl": 1}


class FormFieldGroup(models.Model):
    form = models.ForeignKey(
        "Form", related_name="field_groups", on_delete=models.CASCADE
    )

    key = models.CharField(
        max_length=50, help_text="machine key e.g. address, billing_address"
    )

    label = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.JSONField(
        default=create_default_order_dict,
        blank=True,
    )

    class Meta:
        unique_together = ("form", "key")

    def __str__(self):
        return f"{self.form.title} - {self.label}"

    def get_absolute_url(self):
        return reverse("form_field_group_component", kwargs={"pk": self.pk})

    def get_field_urls(self):
        return [x.get_absolute_url() for x in self.fields.all()]


def create_default_widths_dict():
    return {"xs": 12, "sm": 12, "md": 6, "lg": 4, "xl": 3, "2xl": 3}


class FormField(models.Model):
    form = models.ForeignKey("Form", related_name="fields", on_delete=models.CASCADE)
    conditional_logic = models.JSONField(default=dict, blank=True)
    group = models.ForeignKey(
        "FormFieldGroup",
        related_name="fields",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    field_type = models.ForeignKey(
        FieldType, null=True, blank=True, on_delete=models.PROTECT
    )
    choices = models.ManyToManyField("FieldChoice", through="FormFieldChoiceMembership")
    label = models.CharField(max_length=200, blank=True)
    help_text = models.CharField(max_length=300, blank=True)
    validations = models.JSONField(default=dict, blank=True)
    widths = models.JSONField(
        default=create_default_widths_dict,
        blank=True,
    )
    order = models.JSONField(
        default=create_default_order_dict,
        blank=True,
    )
    optional = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = _("Form Field")
        verbose_name_plural = _("Form Fields")

    def __str__(self):
        return f"{self.group or self.form} - {self.get_label()}"

    def get_absolute_url(self):
        return reverse("form_field_component", kwargs={"pk": self.pk})

    def get_label(self):
        return self.label or self.field_type.default_label

    def get_help_text(self):
        return self.help_text or self.field_type.default_help_text

    def get_choices(self):
        if not self.field_type.supports_choices:
            return None
        return [(c.value, c.label) for c in self.choices.all()]

    def get_template_name(self):
        return f"fields/{self.field_type.key}.html"

    def get_value(self):
        if self.field_type.key == "submission_id":
            return str(uuid.uuid4())


class FieldChoice(models.Model):
    label = models.CharField(max_length=200)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.label} ({self.value})"


class FormFieldChoiceMembership(models.Model):
    field = models.ForeignKey("FormField", on_delete=models.CASCADE)
    choice = models.ForeignKey("FieldChoice", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["field", "choice"], name="unique_field_choice"
            )
        ]


# Sample Validation
# {
#   "required": true,               // boolean, field must be filled
#   "min_length": 3,                // integer, minimum string length
#   "max_length": 50,               // integer, maximum string length
#   "regex": "^[A-Za-z]+$",         // string, regular expression pattern
#   "choices": ["option1","option2"], // array of allowed values
#   "min": 0,                       // number, minimum for numeric fields
#   "max": 100,                     // number, maximum for numeric fields
#   "allowed_domains": ["company.com"], // array, for email domains
#   "custom": {                     // optional, custom validator logic
#     "operator": "$in",            // "$in", "$regex", "$gt", "$lt"
#     "value": ["A", "B", "C"]     // value to compare
#   }
# }


class ValidationType(models.Model):
    key = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)

    applicable_field_types = models.ManyToManyField("FieldType")
    parameter_schema = models.JSONField()
    default_error_message = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Validation Type")
        verbose_name_plural = _("Validation Types")

    def __str__(self):
        return self.label


class Form(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("owner"), on_delete=models.CASCADE
    )
    title = models.CharField(_("title"), max_length=50)
    created_at = models.DateTimeField(
        _("created at"), blank=False, auto_now=False, auto_now_add=True
    )
    expiration_date = models.DateTimeField(
        _("expiration date"), blank=False, auto_now=False, auto_now_add=False
    )

    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Forms")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("form_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("form_update", kwargs={"pk": self.pk})

    def get_field_urls(self):
        return [
            y.get_absolute_url()
            for y in chain(
                self.fields.filter(group__isnull=True).all(), self.field_groups.all()
            )
        ]


class FormResponse(models.Model):
    form = models.ForeignKey(Form, verbose_name=_("form"), on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True
    )

    class Meta:
        verbose_name = _("Form Response")
        verbose_name_plural = _("Form Responses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("form_response_detail", kwargs={"pk": self.pk})


class FormFieldResponse(models.Model):
    response = models.ForeignKey(
        FormResponse, verbose_name=_("form response"), on_delete=models.CASCADE
    )

    field = models.ForeignKey(
        FormField, verbose_name=_("form field"), on_delete=models.CASCADE
    )

    value = models.JSONField()

    created_at = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True
    )

    class Meta:
        verbose_name = _("Form Field Response")
        verbose_name_plural = _("Form Field Responses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("form_field_response_detail", kwargs={"pk": self.pk})
