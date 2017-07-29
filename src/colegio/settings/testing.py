

from .base import *
from django.test.runner import DiscoverRunner


class UnManagedModelTestRunner(DiscoverRunner):

    def setup_test_environment(self, *args, **kwargs):
        from django.apps import apps
        self.unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True
        super(UnManagedModelTestRunner, self).setup_test_environment(*args, **kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args, **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False

TEST_RUNNER = 'colegio.settings.testing.UnManagedModelTestRunner'

MIGRATION_MODULES = {
    'utils': 'utils.migrations',
    'register': 'register.migrations',
}

IS_TESTING = True