from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from edc_form_validators.form_validator import FormValidator


class MaternalUltrasoundInitialFormValidator(FormValidator):

    def clean(self):

        cleaned_data = self.cleaned_data
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

        est_edd = cleaned_data.get('est_edd_ultrasound')
        ga_by_ultrasound = cleaned_data.get('ga_by_ultrasound_wks')
        est_edd_ultrasound = cleaned_data.get('est_edd_ultrasound')
        report_datetime = cleaned_data.get('report_datetime')

        if cleaned_data.get('ga_by_ultrasound_wks'):

            est_conceive_date = (report_datetime.date() -
                                 relativedelta(weeks=ga_by_ultrasound))

            weeks_between = ((est_edd - est_conceive_date).days) / 7

            if (weeks_between + 1) > ga_by_ultrasound:

                if (int(weeks_between) + 1) not in range(39, 42):
                    msg = {'est_edd_ultrasound':
                           f'Estimated edd by ultrasound {est_edd_ultrasound} '
                           'should match GA by ultrasound'}
                    self._errors.update(msg)
                    raise ValidationError(msg)
