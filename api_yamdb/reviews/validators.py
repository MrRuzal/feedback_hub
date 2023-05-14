from django.utils import timezone
from rest_framework.serializers import ValidationError


def validet_year(year):
    if year > timezone.now().year:
        raise ValidationError('Такого года быть не может')
