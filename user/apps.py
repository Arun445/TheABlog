from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class UserConfig(AppConfig):
    name = 'user'


    def ready(self):
        import user.signals