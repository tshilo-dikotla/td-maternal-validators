from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow, relativedelta
from ..form_validators import MaternalVisitFormValidator


@tag('mv')
class TestMaternalVisitFormValidator(TestCase):

    def setUp(self):
        self.options = {
            'report_datetime': get_utcnow(),
            'survival_status': 'unknown',
            'last_alive_date': None
        }

    def test_report_datetime_not_before_consent(self):
        self.options['report_datetime'] = (get_utcnow() - 
                                           relativedelta(days=25)).datetime()
        materna_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, materna_visit.validate)

    def test_report_datetime_not_after_consent(self):
        self.options['report_datetime'] = get_utcnow()
        materna_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        materna_visit.validate()
        self.assertEqual({}, materna_visit._errors)

    def test_last_alive_date_none(self):
        self.options['survival_status'] = 'alive'
        materna_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        self.assertRaises(ValidationError, materna_visit.validate)

    def test_last_alive_date_not_none(self):
        self.options['survival_status'] = 'alive'
        self.options['last_alive_date'] = get_utcnow()
        materna_visit = MaternalVisitFormValidator(cleaned_data=self.options)
        materna_visit.validate()
        self.assertEqual({}, materna_visit._errors)
