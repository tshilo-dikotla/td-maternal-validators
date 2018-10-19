from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow
from edc_appointment.models import Appointment
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


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
