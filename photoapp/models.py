from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import cloudinary
from cloudinary.uploader import upload
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_profile_picture_url(self):
        if self.profile_picture:
            return cloudinary.CloudinaryImage(self.profile_picture).build_url(
                secure=True,
                width=200,
                height=200,
                crop="fill",
                gravity="face"
            )
        return None

class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255)
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_photos', blank=True)

    def __str__(self):
        return self.title

    def get_image_url(self):
        return cloudinary.CloudinaryImage(self.image).build_url(
            secure=True,
            width=800,
            height=600,
            crop="limit",
            quality="auto"
        )

    def get_tags(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]