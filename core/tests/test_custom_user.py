import pytest
from core.models import CustomUser


@pytest.mark.django_db
def test_user_create():
    """
    Tests custom user creation
    :return: Pass or Fail
    """
    CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert CustomUser.objects.count() == 1
