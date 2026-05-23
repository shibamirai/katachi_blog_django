from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        """
        与えられたメールアドレスと名前、パスワードでユーザを作成する。
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        与えられたメールアドレスと名前、パスワードでスーパーユーザを作成する。
        """
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="メールアドレス",
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name="名前",
        max_length=100
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        """
        管理サイトへのアクセス可否を返す。管理者権限があればOKとする。
        """
        return self.is_admin
