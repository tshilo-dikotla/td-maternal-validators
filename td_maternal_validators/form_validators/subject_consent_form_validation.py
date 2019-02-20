import re
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.utils import relativedelta
from edc_form_validators import FormValidator


class SubjectConsentFormValidator(FormValidator):

    screening_model = 'td_maternal.subjectscreening'

    td_consent_version_model = 'td_maternal.tdconsentversion'

    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.screening_model)

    @property
    def td_consent_version_cls(self):
        return django_apps.get_model(self.td_consent_version_model)

    def clean(self):
        cleaned_data = self.cleaned_data
        try:
            subject_screening = self.subject_screening_cls.objects.get(
                screening_identifier=cleaned_data.get('screening_identifier'))
        except self.subject_screening_cls.DoesNotExist:
            raise ValidationError(
                'Complete the "Subject Screening" form before proceeding.')

        if cleaned_data.get('citizen') != subject_screening.has_omang:
            message = {'citizen':
                       'During screening you said has_omang is {}. '
                       'Yet you wrote citizen is {}. Please correct.'.format(
                           subject_screening.has_omang, cleaned_data.get('citizen'))}
            self._errors.update(message)
            raise ValidationError(message)

        self.clean_full_name_syntax()
        self.clean_initials_with_full_name()
        self.validate_dob(cleaned_data=self.cleaned_data,
                          model_obj=subject_screening)
        self.validate_identity_number(cleaned_data=self.cleaned_data)
        self.validate_recruit_source()
        self.validate_recruitment_clinic()
        self.validate_td_consent(model_obj=subject_screening)

    def clean_full_name_syntax(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if not re.match(r'^[A-Z]+$|^([A-Z]+[ ][A-Z]+)$', first_name):
            message = {'first_name': 'Ensure first name is letters (A-Z) in '
                       'upper case, no special characters, except spaces.'}
            self._errors.update(message)
            raise ValidationError(message)

        if not re.match(r'^[A-Z-]+$', last_name):
            message = {'last_name': 'Ensure last name is letters (A-Z) in '
                       'upper case, no special characters, except hyphens.'}
            self._errors.update(message)
            raise ValidationError(message)

        if first_name and last_name:
            if first_name != first_name.upper():
                message = {'first_name': 'First name must be in CAPS.'}
                self._errors.update(message)
                raise ValidationError(message)
            elif last_name != last_name.upper():
                message = {'last_name': 'Last name must be in CAPS.'}
                self._errors.update(message)
                raise ValidationError(message)

    def clean_initials_with_full_name(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        initials = cleaned_data.get("initials")
        try:
            middle_name = None
            is_first_name = False
            new_first_name = None
            if len(first_name.split(' ')) > 1:
                new_first_name = first_name.split(' ')[0]
                middle_name = first_name.split(' ')[1]

            if (middle_name and
                (initials[:1] != new_first_name[:1] or
                 initials[1:2] != middle_name[:1])):
                is_first_name = True

            elif not middle_name and initials[:1] != first_name[:1]:
                is_first_name = True

            if is_first_name or initials[-1:] != last_name[:1]:
                raise forms.ValidationError(
                    {'initials': 'Initials do not match full name.'},
                    params={
                        'initials': initials,
                        'first_name': first_name,
                        'last_name': last_name},
                    code='invalid')
        except (IndexError, TypeError):
            raise forms.ValidationError('Initials do not match fullname.')

    def validate_identity_number(self, cleaned_data=None):
        if cleaned_data.get('identity_type') == 'country_id':
            if len(cleaned_data.get('identity')) != 9:
                msg = {'identity':
                       'Country identity provided should contain 9 values. '
                       'Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            if cleaned_data.get('identity')[4] != '2':
                msg = {'identity':
                       'Identity provided indicates participant is Male. Please '
                       'correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_dob(self, cleaned_data=None, model_obj=None):
        consent_datetime = cleaned_data.get(
            'consent_datetime') or self.instance.consent_datetime
        consent_age = relativedelta(
            consent_datetime.date(), cleaned_data.get('dob')).years
        if consent_age != model_obj.age_in_years:
            message = {'dob':
                       'In Subject Screening you indicated the participant is {}, '
                       'but age derived from the DOB is {}.'.format(
                           model_obj.age_in_years, consent_age)}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_recruit_source(self):
        self.validate_other_specify(
            field='recruit_source',
            other_specify_field='recruit_source_other',
            required_msg=('You indicated that mother first learnt about the '
                          'study from a source other than those in the list '
                          'provided. Please specify source.'),
        )

    def validate_recruitment_clinic(self):
        clinic = self.cleaned_data.get('recruitment_clinic')
        self.validate_other_specify(
            field='recruitment_clinic',
            other_specify_field='recruitment_clinic_other',
            required_msg=('You CANNOT specify other facility that mother was '
                          f'recruited from as you already indicated {clinic}')
        )

    def validate_td_consent(self, model_obj=None):
        try:
            self.td_consent_version_cls.objects.get(
                screening_identifier=model_obj.screening_identifier)
        except self.td_consent_version_cls.DoesNotExist:
            raise ValidationError(
                'Complete mother\'s consent version form before proceeding')
