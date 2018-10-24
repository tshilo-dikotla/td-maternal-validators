from django.db import models
from django.db.models.deletion import PROTECT
from edc_appointment.models import Appointment
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow

from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_constants.choices import YES_NO


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class MaternalConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25)

    dob = models.DateField()


class MaternalVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    def save(self, *args, **kwargs):
        self.visit_code = self.appointment.visit_code
        self.subject_identifier = self.appointment.subject_identifier
        super().save(*args, **kwargs)


class MaternalArvPostAdh(models.Model):

    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)


class MaternalArvPreg(models.Model):

    took_arv = models.CharField(
        choices=YES_NO,
        max_length=10)
    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)


class MaternalArv(models.Model):

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg, on_delete=PROTECT)


class MaternalLifetimeArvHistory(models.Model):

    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)

    haart_start_date = models.DateField(
        blank=True,
        null=True)
