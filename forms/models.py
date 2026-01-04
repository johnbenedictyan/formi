from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class FieldType(models.Model):
    key = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Field Type")
        verbose_name_plural = _("Field Types")

    def __str__(self):
        return self.label


class FieldPreset(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    field_type = models.ForeignKey(FieldType, on_delete=models.PROTECT)
    default_label = models.CharField(max_length=200)
    default_help_text = models.CharField(max_length=300, blank=True)
    default_validations = models.JSONField(default=dict)

    class Meta:
        verbose_name = _("Field Preset")
        verbose_name_plural = _("Field Presets")

    def __str__(self):
        return self.name


class FormField(models.Model):
    form = models.ForeignKey("Form", on_delete=models.CASCADE)
    preset = models.ForeignKey(FieldPreset, on_delete=models.PROTECT)

    label = models.CharField(max_length=200, blank=True)
    help_text = models.CharField(max_length=300, blank=True)

    validations_override = models.JSONField(default=dict, blank=True)

    order = models.PositiveIntegerField()
    conditional_logic = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _("Form Field")
        verbose_name_plural = _("Form Fields")

    def __str__(self):
        return f"{self.form.title} - {self.label or self.preset.name}"


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
        settings.AUTH_USER_MODEL, verbose_name=_(""), on_delete=models.CASCADE
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
        return reverse("Form_detail", kwargs={"pk": self.pk})


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
        return reverse("Form_response_detail", kwargs={"pk": self.pk})


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


class FormFieldRule(models.Model):
    field = models.ForeignKey(
        FormField, verbose_name=_("form field"), on_delete=models.CASCADE
    )

    condition = models.JSONField()

    action = models.JSONField()

    class Meta:
        verbose_name = _("Form Field Rule")
        verbose_name_plural = _("Form Field Rules")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("form_field_rule_detail", kwargs={"pk": self.pk})
