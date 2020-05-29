from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Class responsible for wrapping django's users
    and store additional data
    """
