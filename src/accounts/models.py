#import authtools
#from django.db import models
# Create your models here.
#class UserCustom(authtools.User):

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):

  def authenticate(self, username=None, password=None, **kwargs):
    UserModel = get_user_model()
    if username is None:
        username = kwargs.get(UserModel.USERNAME_FIELD)
    try:
        if '@' in username:
            UserModel.USERNAME_FIELD = 'email'
        else:
            UserModel.USERNAME_FIELD = 'name'

        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        UserModel().set_password(password)
    else:
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

"""
class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(name=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

"""