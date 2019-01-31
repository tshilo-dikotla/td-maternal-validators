from edc_constants.constants import YES, OTHER
from edc_form_validators import FormValidator


class MaternalContraceptionFormValidator(FormValidator):
    def clean(self):
        self.required_if(
            YES,
            field='more_children',
            field_required='next_child',
            required_msg='Participant desires more children, '
                         'question on next child cannot be None.',
            not_required_msg='The client does not desire more children, '
                             'question on next child is not required.'
        )

        required_fields = ['contr', 'contraceptive_startdate']
        required_msgs = {
            'contr': 'Participant uses a contraceptive method, '
                     'please select a valid method',
            'contraceptive_startdate': 'Participant uses a contraceptive '
                                       'method, please give a contraceptive '
                                       'startdate.'}
        for required in required_fields:
            self.required_if(
                YES,
                field='uses_contraceptive',
                field_required=required,
                required_msg=required_msgs[required]
            )

        self.required_if(
            YES,
            field='another_pregnancy',
            field_required='pregnancy_date',
            required_msg='Participant is pregnant, please give date '
                         'participant found out.',
            not_required_msg='Participant is not pregnant, do not give a date.'
        )

        self.required_if(
            YES,
            field='pap_smear',
            field_required='pap_smear_date',
            required_msg='Please give the date the pap smear was done.',
            not_required_msg='Pap smear not done, don\'t provide the date'
        )

        self.required_if(
            YES,
            field='pap_smear_result',
            field_required='pap_smear_result_status',
            required_msg='Participant knows her pap smear result, '
                         'please give the status of the pap smear.'
        )

        self.required_if(
            'abnormal',
            field='pap_smear_result_status',
            field_required='pap_smear_result_abnormal',
            required_msg='pap smear results were abnormal, can the participant'
                         ' share the result description.'
        )

        m2m_fields = {'contr': 'contr_other',
                      'contraceptive_relative': 'contraceptive_relative_other'}
        for m2m_field, field in m2m_fields.items():
            self.m2m_other_specify(
                OTHER,
                m2m_field=m2m_field,
                field_other=field)

        self.validate_other_specify(
            field='influential_decision_making',
            other_specify_field='influential_decision_making_other',
        )
