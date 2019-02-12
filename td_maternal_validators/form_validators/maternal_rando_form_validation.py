from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from edc_constants.constants import POS
from edc_form_validators import FormValidator


class MaternalRandoFormValidator(FormValidator):

    antenatal_enrollment_model = 'td_maternal.antenatalenrollment'

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        self.verify_hiv_status()

    @property
    def antenatal_enrollment(self):
        """Return antenatal enrollment.
        """
        try:
            antenatal_enrollment = self.antenatal_enrollment_cls.objects.get(
                subject_identifier=self.cleaned_data.get('maternal_visit').appointment.subject_identifier)
        except ObjectDoesNotExist:
            msg = {'sid':
                   f'Antenatal Enrollment for subject {self.subject_identifier} must exist'}
            self._errors.update(msg)
            raise ValidationError(msg)
        return antenatal_enrollment

    def verify_hiv_status(self):
        if self.antenatal_enrollment.enrollment_hiv_status != POS:
            msg = {'sid':
                   'Cannot Randomize mothers that are not HIV POS. '
                   f'Got {self.antenatal_enrollment.enrollment_hiv_status}. See Antenatal Enrollment.'}
            self._errors.update(msg)
            raise ValidationError(msg)
