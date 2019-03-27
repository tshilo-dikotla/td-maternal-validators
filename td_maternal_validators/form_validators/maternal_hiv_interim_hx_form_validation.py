from edc_constants.constants import YES
from edc_form_validators import FormValidator
from .crf_form_validator import TDCRFFormValidator


class MaternalHivInterimHxFormValidator(TDCRFFormValidator,
                                        FormValidator):

    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

        required_fields = ('cd4_date', 'cd4_result')
        for required in required_fields:
            self.required_if(
                YES,
                field='has_cd4',
                field_required=required,
                required_msg=('You indicated that a CD4 count was performed. '
                              f'Please provide the {required}'),
                not_required_msg=('You indicated that a CD4 count was NOT '
                                  f'performed, yet provided a {required} '
                                  'CD4 was performed. Please correct.')
            )
        self.required_if(
            YES,
            field='has_vl',
            field_required='vl_date',
            required_msg=('You indicated that a VL count was performed. '
                          'Please provide the date.'),
            not_required_msg=('You indicated that a VL count was NOT performed, '
                              'yet provided a date VL was performed. Please correct.')
        )
        self.applicable_if(
            YES,
            field='has_vl',
            field_applicable='vl_detectable'
        )
        self.required_if(
            YES,
            field='vl_detectable',
            field_required='vl_result',
            required_msg=('You indicated that the VL was detectable. '
                          'Provide provide VL result.'),
            not_required_msg=('You indicated that the VL was NOT detectable. '
                              'you cannot provide a result.')
        )
