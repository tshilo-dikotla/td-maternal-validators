from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_form_validators import FormValidator
from edc_constants.constants import POS, YES


class MaternalLabDelFormValidator(FormValidator):

    maternal_arv_model = 'td_maternal.maternalarv'
    rapid_test_result_model = 'td_maternal.rapidtestresult'
    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def rapid_testing_model_cls(self):
        return django_apps.get_model(self.rapid_test_result_model)

    @property
    def antenatal_enrollment_model_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    @property
    def maternal_arv_cls(self):
        return django_apps.get_model(self.maternal_arv_model)

    @property
    def status_result(self):
        try:
            antenatal_enrollment = self.antenatal_enrollment_model_cls.objects.get(
                subject_identifier=self.cleaned_data.get('subject_identifier'))
            condition = (antenatal_enrollment.enrollment_hiv_status == POS or
                         antenatal_enrollment.week32_result == POS or
                         antenatal_enrollment.rapid_test_result == POS)
            if condition:
                status = POS
            else:
                rapid_test_result = self.self.rapid_testing_model_cls.objects.\
                    filter().order_by('created').last()
                status = rapid_test_result.result
        except self.antenatal_enrollment_model_cls.DoesNotExist:
            raise ValidationError('Fill out Antenatal Enrollment Form.')

        return status

    def clean(self):
        self.validate_initiation_date(cleaned_data=self.cleaned_data)
        self.validate_valid_regime_hiv_pos_only(cleaned_data=self.cleaned_data)

    def validate_initiation_date(self, cleaned_data=None):
        subject_identifier = cleaned_data.get('subject_identifier')
        maternal_arv = self.maternal_arv_cls.objects.filter(
            maternal_arv_preg__maternal_visit__appointment__subject_identifier=subject_identifier,
            stop_date__isnull=True).order_by('-start_date').first()
        if maternal_arv:
            initiation_date = cleaned_data.get('arv_initiation_date')
            if initiation_date != maternal_arv.start_date:
                message = {'arv_initiation_date':
                           'ARV\'s initiation date must match start date '
                           'in pregnancy form, pregnancy form start date is '
                           '{}, got {}.'.format(
                               maternal_arv.start_date, initiation_date)}
                self._errors.update(message)
                raise ValidationError(message)

    def validate_valid_regime_hiv_pos_only(self, cleaned_data=None):
        if self.status_result == POS:
            if cleaned_data.get('valid_regiment_duration') != YES:
                message = {'valid_regiment_duration':
                           'Participant is HIV+ valid regimen duration '
                           'should be YES. Please correct.'}
                self._errors.update(message)
                raise ValidationError(message)
            self.required_if(
                YES,
                field='valid_regiment_duration',
                field_required='arv_initiation_date',
                required_msg='You indicated participant was on valid regimen, '
                'please give a valid arv initiation date.'
            )
