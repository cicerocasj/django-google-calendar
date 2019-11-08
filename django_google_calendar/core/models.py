from django.contrib.auth.models import User
from django.db import models

from oauth2client.contrib.django_util.models import CredentialsField


class CredentialsModel(models.Model):
    id = models.OneToOneField(User, primary_key=True)
    credential = CredentialsField()
