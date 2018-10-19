from django.conf import settings

if settings.APP_NAME == 'td_maternal_validators':
    from .tests import models
