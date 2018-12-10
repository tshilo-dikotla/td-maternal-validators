from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_appointment.models import Appointment
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow
<<<<<<< HEAD
from edc_registration.model_mixins import (
    UpdatesOrCreatesRegistrationModelMixin)
=======
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_constants.choices import YES_NO, GENDER
>>>>>>> e585469a334e3523fea3cb1230f535ac7fd95ce4


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class MaternalConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=50)

    gender = models.CharField(max_length=25)

    dob = models.DateField()

    consent_datetime = models.DateTimeField()

    version = models.CharField(
        max_length=10,
        editable=False)


class RegisteredSubject(BaseUuidModel):

    first_name = FirstnameField(null=True)

    last_name = LastnameField(verbose_name="Last name")

    gender = models.CharField(max_length=1, choices=GENDER)


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


<<<<<<< HEAD
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
=======
class MaternalUltraSoundInitial(models.Model):

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    ga_confirmed = models.IntegerField()


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


class RapidTestResult(BaseUuidModel):

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    result = models.CharField(max_length=15)


class AntenatalEnrollment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=50)

    enrollment_hiv_status = models.CharField(max_length=15)

    week32_result = models.CharField(max_length=15)

    rapid_test_result = models.CharField(max_length=15)

    rapid_test_date = models.DateField(
        null=True,
        blank=True)


class MaternalObstericalHistory(models.Model):

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    prev_pregnancies = models.IntegerField()


class SubjectScreening(BaseUuidModel):

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)


class TdConsentVersion(BaseUuidModel):

    subjectscreening = models.ForeignKey(
        SubjectScreening, null=True, on_delete=PROTECT)

    version = models.CharField(max_length=3)

    report_datetime = models.DateField(
        null=True,
        blank=True)
>>>>>>> e585469a334e3523fea3cb1230f535ac7fd95ce4
