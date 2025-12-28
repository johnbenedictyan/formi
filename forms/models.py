from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Formi(models.Model):
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
        verbose_name = _("formi")
        verbose_name_plural = _("formis")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("formi_detail", kwargs={"pk": self.pk})


class FormiField(models.Model):
    name = models.CharField(_("name"), max_length=50)
    help_text = models.CharField(_("help text"), max_length=50)
    field_type = models.CharField(_("field type"), max_length=50)
    formi = models.ForeignKey(Formi, verbose_name=_("formi"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("formi field")
        verbose_name_plural = _("formi fields")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("formi_field_detail", kwargs={"pk": self.pk})


class FormiFieldModifier(models.Model):
    field = models.ForeignKey(
        FormiField, verbose_name=_("field"), on_delete=models.CASCADE
    )
    modifier_type = models.CharField(_("type"), max_length=50)
    value = models.CharField(_("value"), max_length=50)

    class Meta:
        verbose_name = _("formi field modifier")
        verbose_name_plural = _("formi field modifiers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("formi_field_modifier_detail", kwargs={"pk": self.pk})


class FormiResponse(models.Model):
    formi = models.ForeignKey(Formi, verbose_name=_("formi"), on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True
    )

    class Meta:
        verbose_name = _("formi response")
        verbose_name_plural = _("formi responses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("formi_response_detail", kwargs={"pk": self.pk})
