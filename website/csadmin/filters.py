import django_filters
from status.models import Account,interests
from django.contrib.auth.models import User

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Account
        fields = ['name']
