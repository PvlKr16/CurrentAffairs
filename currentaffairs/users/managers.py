from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Superuser must have an email")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return super().create_superuser(
            username=email,  # подставляем username автоматически
            email=email,
            password=password,
            **extra_fields
        )
