import django_filters
from users.models import Account

class AccountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields=['graduation_year']

