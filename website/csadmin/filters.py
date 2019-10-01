import django_filters
from status.models import Account,interests,FixedDeposits
from django.contrib.auth.models import User

class AccountFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Account
        fields = ['name']

class FDFilter(django_filters.FilterSet):
    fdcapital = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = FixedDeposits
        fields = ['fdcapital']

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = interests
        fields = ['username']
