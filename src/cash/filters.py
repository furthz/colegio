import django_filters
from .models import Remesa
from .forms import ConsignmentForm


class ConsignmentFilter(django_filters.FilterSet):


    class Meta:
        model = Remesa
        fields = {
            'fechacreacion': ['range'],
        }

        @classmethod
        def filter_for_lookup(cls, f, lookup_type):
            # override date range lookups
            if isinstance(f, Remesa.DateField) and lookup_type == 'range':
                return django_filters.DateRangeFilter, {}

            # use default behavior otherwise
            return super(ConsignmentFilter, cls).filter_for_lookup(f, lookup_type)