from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from edc_form_validators.form_validator import FormValidator
from .crf_form_validator import TDCRFFormValidator


class MaternalUltrasoundInitialFormValidator(TDCRFFormValidator, FormValidator):

    def clean(self):

        cleaned_data = self.cleaned_data
        self.subject_identifier = cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        if cleaned_data.get('est_edd_ultrasound') and (
                cleaned_data.get('est_edd_ultrasound') >
                cleaned_data.get('report_datetime').date() +
                relativedelta(weeks=40)):
            msg = {'est_edd_ultrasound': 'Estimated edd by ultrasound cannot be'
                   ' greater than 40 weeks from today'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if cleaned_data.get('ga_by_ultrasound_wks') and(
                cleaned_data.get('ga_by_ultrasound_wks') > 40):
            msg = {'ga_by_ultrasound_wks':
                   ('GA by ultrasound cannot be greater than 40 weeks.')}

            self._errors.update(msg)
            raise ValidationError(msg)

        if cleaned_data.get('ga_by_ultrasound_days') and(
                cleaned_data.get('ga_by_ultrasound_days') > 7):
            msg = {'ga_by_ultrasound_days':
                   ('GA by ultrasound days cannot be greater than 7 days.')}

            self._errors.update(msg)
            raise ValidationError(msg)

        ga_by_ultrasound = cleaned_data.get('ga_by_ultrasound_wks')
        est_edd_ultrasound = cleaned_data.get('est_edd_ultrasound')
        report_datetime = cleaned_data.get('report_datetime')
        self.validate_edd_report_datetime()

        if cleaned_data.get('ga_by_ultrasound_wks'):

            est_conceive_date = (report_datetime.date() -
                                 relativedelta(weeks=ga_by_ultrasound))
            if(est_edd_ultrasound):
                weeks_between = (
                    (est_edd_ultrasound - est_conceive_date).days) / 7

                if (weeks_between + 1) > ga_by_ultrasound:

                    if (int(weeks_between) + 1) not in range(39, 42):
                        msg = {'est_edd_ultrasound':
                               f'Estimated edd by ultrasound {est_edd_ultrasound} '
                               'should match GA by ultrasound'}
                        self._errors.update(msg)
                        raise ValidationError(msg)

    def validate_edd_report_datetime(self):
        if (self.cleaned_data.get('est_edd_ultrasound') and
                self.cleaned_data.get('est_edd_ultrasound') <
                self.cleaned_data.get('maternal_visit').report_datetime.date()):
            raise ValidationError('Expected a future date')
