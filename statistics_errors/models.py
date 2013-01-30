
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import datetime
import json

user_model = getattr(settings, 'STATISTICS_ERRORS_USER', User)
date_format = getattr(settings, 'STATISTICS_ERRORS_DATE_FORMAT', '%c')
datetime_format = getattr(settings, 'STATISTICS_ERRORS_DATETIME_FORMAT', '%c')

def _prototype_to_json(instance):
    if not isinstance(instance, models.Model):
        raise TypeError(u"instance is not a Model object!")

    response = {}

    for field in instance._meta.fields:
        if field.get_internal_type() in ( 'ForeignKey', 'OneToOneField',):
            # In case of many-to-one or one-to-one relationships we returns the JSON.
            # representation of the related object.
            relation = getattr(instance, field.name)
            if not relation: continue
            response.update({ field.name: relation.pk })
        elif field.get_internal_type() in ( 'DateField', ):
            # In case of DateField we return a string representation of the object,
            # according to the format given by 'MEDICAL_REPORTS_DATE_FORMAT'
            response.update({ field.name: datetime.date.strftime(
                getattr(instance, field.name), date_format) })
        elif field.get_internal_type() in ( 'DateTimeField', ):
            # In case of DateTimeField we return a string representation of the object,
            # according to the format given by 'MEDICAL_REPORTS_DATETIME_FORMAT'
            response.update({ field.name: datetime.datetime.strftime(
                getattr(instance, field.name), datetime_format) })
        else:
            try:
                response.update({ field.name: json.loads(getattr(instance, field.name)) })
            except (ValueError, TypeError):
                response.update({ field.name: getattr(instance, field.name) })
    return response

class UserError(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(to=user_model, null=True, blank=False, on_delete=models.SET_NULL)
    message     = models.CharField(max_length=256, blank=False, null=True)
    url         = models.CharField(max_length=256, blank=False, null=True)
    loc         = models.PositiveIntegerField(blank=False, null=True)
    os          = models.CharField(max_length=32, blank=False, null=True)
    browser     = models.CharField(max_length=32, blank=False, null=True)
    version     = models.CharField(max_length=32, blank=False, null=True)
    plugins     = models.CharField(max_length=128, blank=False, null=True)
    device      = models.CharField(max_length=256, blank=False, null=True)
    locale      = models.CharField(max_length=64, blank=False, null=True)
    address     = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, blank=False, null=True)

    class Meta:
        verbose_name = _(u"Error Statistic")
        verbose_name_plural = _(u"Error Statistics")

    def to_json(self):
        return _prototype_to_json(self)

class UserStatistic(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(to=user_model, null=True, blank=False, on_delete=models.SET_NULL)
    url         = models.CharField(max_length=256, blank=False, null=True)
    os          = models.CharField(max_length=32, blank=False, null=True)
    browser     = models.CharField(max_length=32, blank=False, null=True)
    version     = models.CharField(max_length=32, blank=False, null=True)
    plugins     = models.CharField(max_length=128, blank=False, null=True)
    device      = models.CharField(max_length=256, blank=False, null=True)
    locale      = models.CharField(max_length=64, blank=False, null=True)
    address     = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, blank=False, null=True)
    referer     = models.CharField(max_length=256, blank=False, null=True)
    querydict   = models.TextField(blank=False, null=True)

    class Meta:
        verbose_name = _(u"Access Statistic")
        verbose_name_plural = _(u"Access Statistics")

    def to_json(self):
        return _prototype_to_json(self)
