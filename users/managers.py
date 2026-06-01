from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra):
        if not email:
            raise ValueError("Email обязателен")
        if not name:
            raise ValueError("Имя обязательно")
        if not surname:
            raise ValueError("Фамилия обязательна")

        normalized = self.normalize_email(email)
        user = self.model(email=normalized, name=name, surname=surname, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, name, surname, password, **extra)
