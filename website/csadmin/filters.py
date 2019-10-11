import django_filters
from status.models import Account,interests,FixedDeposits
from django.contrib.auth.models import User

class AccountFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Account
        fields = ['name']

class UserFilter(django_filters.FilterSet):
    username__first_name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = FixedDeposits
        fields = ['username__first_name']

class UsersFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username']
