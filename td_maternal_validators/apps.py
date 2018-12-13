from django.apps import AppConfig as DjangoApponfig
from edc_visit_tracking.apps import (
    AppConfig as BaseEdcVisitTrackingAppConfig)


class AppConfig(DjangoApponfig):
    name = 'td_maternal_validators'
    verbose_name = 'Tshilo Dikotla Maternal Form Validators'


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'td_maternal': ('maternal_visit', 'td_maternal.maternalvisit')}
