from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_appointment.models import Appointment
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class MaternalConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25)

    dob = models.DateField()


class Appointment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    appt_datetime = models.DateTimeField(default=get_utcnow)

    visit_code = models.CharField(max_length=25)


class MaternalVisit(BaseUuidModel):

    appointment = models.OneToOneField(Appointment, on_delete=PROTECT)

    subject_identifier = models.CharField(max_length=25)

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    report_datetime = models.DateTimeField(
        default=get_utcnow)

    def save(self, *args, **kwargs):
        self.visit_code = self.appointment.visit_code
        self.subject_identifier = self.appointment.subject_identifier
        super().save(*args, **kwargs)


class MaternalArvPostAdh(models.Model):

    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)


class MaternalCrfModel(BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`).
    """

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)


class MaternalObstericalHistory(MaternalCrfModel):

    """ A model completed by the user on Obsterical History for all mothers.
    """

    prev_pregnancies = models.IntegerField(
        verbose_name="Including this pregnancy, how many previous pregnancies "
        "for this participant?",
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
        help_text="")

    class Meta:
        app_label = 'td_maternal'
        verbose_name = "Maternal Obsterical History"
        verbose_name_plural = "Maternal Obsterical History"
