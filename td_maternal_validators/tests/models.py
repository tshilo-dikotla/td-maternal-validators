from django.db import models
from django.db.models.deletion import PROTECT
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_base.model_mixins import BaseUuidModel, ListModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, GENDER
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class ListModel(ListModelMixin, BaseUuidModel):
    pass


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    screening_identifier = models.CharField(max_length=50)

    gender = models.CharField(max_length=25)

    is_literate = models.CharField(max_length=25,
                                   blank=True,
                                   null=True)

    witness_name = models.CharField(max_length=25,
                                    blank=True,
                                    null=True)

    dob = models.DateField()

    consent_datetime = models.DateTimeField()

    version = models.CharField(
        max_length=10,
        editable=False)


class RegisteredSubject(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

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


class MaternalCrfModel(BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`MaternalVisit`).
    """

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)


class MaternalUltraSoundInitial(models.Model):

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    ga_confirmed = models.IntegerField()


class MaternalArvPreg(models.Model):

    took_arv = models.CharField(
        choices=YES_NO,
        max_length=10)
    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)


class MaternalArvHistory(models.Model):

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    haart_start_date = models.CharField(max_length=50)


class MaternalArv(models.Model):

    maternal_arv_preg = models.ForeignKey(MaternalArvPreg, on_delete=PROTECT)

    arv_code = models.CharField(
        verbose_name="ARV code",
        max_length=35)

    start_date = models.DateField(
        null=True,
        blank=False)

    stop_date = models.DateField(
        null=True,
        blank=True)


class MaternalLifetimeArvHistory(models.Model):

    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)

    haart_start_date = models.DateField(
        blank=True,
        null=True)


class RapidTestResult(BaseUuidModel):

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    result = models.CharField(max_length=15)


class AntenatalEnrollment(BaseUuidModel):

    subject_identifier = models.CharField(max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    last_period_date = models.DateField(
        null=True,
        blank=True)

    current_hiv_status = models.CharField(max_length=15)

    week32_test = models.CharField(max_length=15)

    week32_test_date = models.DateField(
        null=True,
        blank=True)

    enrollment_hiv_status = models.CharField(max_length=15)

    week32_result = models.CharField(max_length=15)

    rapid_test_done = models.CharField(max_length=15)

    rapid_test_result = models.CharField(max_length=15)

    rapid_test_date = models.DateField(
        null=True,
        blank=True)


class MaternalObstericalHistory(models.Model):

    maternal_visit = models.OneToOneField(MaternalVisit, on_delete=PROTECT)

    prev_pregnancies = models.IntegerField()


class MaternalMedicalHistory(models.Model):

    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)

    date_hiv_diagnosis = models.DateField(
        null=True,
        blank=True)


class SubjectScreening(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    screening_identifier = models.CharField(
        max_length=36,
        unique=True,
        editable=False)

    has_omang = models.CharField(max_length=3)

    age_in_years = age_in_years = models.IntegerField()


class TdConsentVersion(BaseUuidModel):

    screening_identifier = models.CharField(max_length=50)

    version = models.CharField(max_length=3)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)


class MaternalLocator(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=50)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    may_sms = models.CharField(
        max_length=3)

    may_call = models.CharField(
        max_length=3)
