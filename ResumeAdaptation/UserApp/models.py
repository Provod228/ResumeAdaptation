import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from .services.mixin import SlugMixin



# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)

    social_avatar = models.URLField(blank=True, verbose_name="Аватар из соцсети")
    social_id = models.CharField(max_length=255, blank=True, verbose_name="ID в соцсети")
    provider = models.CharField(max_length=50, blank=True, verbose_name="Провайдер")
    email_verified = models.BooleanField(default=False, verbose_name="Email подтвержден")

    nickname = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Отображаемое имя",
        help_text="Имя, которое видят другие пользователи"
    )

    avatar = models.ImageField(
        upload_to='users/avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Аватар (загруженный)",
        help_text="Загрузите изображение для аватара"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="Slug пользователя",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Администратор",
        help_text="Имеет доступ к админ-панели Django"
    )

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            base_username = self.email.split('@')[0]
            self.username = base_username

            original_username = self.username
            counter = 1
            while User.objects.filter(username=self.username).exists():
                if self.pk and User.objects.get(pk=self.pk).username == self.username:
                    break
                self.username = f"{original_username}_{counter}"
                counter += 1

        elif not self.username:
            self.username = f"user_{uuid.uuid4().hex[:8]}"

        if self.pk:
            try:
                old = User.objects.get(pk=self.pk)

                name_changed = old.username != self.username


                if name_changed:
                    self.slug = SlugMixin.generate_unique_slug(
                        model_class=self.__class__,
                        instance=self,
                        title_field='username',
                    )

            except User.DoesNotExist:
                pass

        if not self.slug:
            self.slug = SlugMixin.generate_unique_slug(
                model_class=self.__class__,
                instance=self,
                title_field='username',
            )

        if not self.nickname:
            self.nickname = "user_" + uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self._delete_avatar_file()
        super().delete(*args, **kwargs)


    def _delete_avatar_file(self):
        # Универсальное удаление через storage API — работает и с Cloudinary.
        if self.avatar:
            try:
                self.avatar.delete(save=False)
            except Exception:
                pass

    def __str__(self):
        return self.username or self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']
        indexes = [
            models.Index(fields=['username', 'nickname']),
            models.Index(fields=['social_id', 'provider']),
        ]