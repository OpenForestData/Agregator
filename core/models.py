from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Class responsible for wrapping django's users
    and store additional data
    """
