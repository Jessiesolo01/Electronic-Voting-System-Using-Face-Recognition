from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, matric_no, password, **extra_fields):
        
        """Create and save a User with the given matric_no and password."""
        if not matric_no:
            raise ValueError('The given matric_no must be set')
        matric_no = f'{matric_no}'.upper()
        user = self.model(matric_no=matric_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, matric_no, password=None, **extra_fields):
        """Create and save a regular User with the given matric_no and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(matric_no, password, **extra_fields)

    def create_superuser(self, matric_no, password, **extra_fields):
        """Create and save a SuperUser with the given matric_no and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(matric_no, password, **extra_fields)
