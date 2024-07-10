"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from pgvector.django import VectorField


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class LangChainPgCollection(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    cmetadata = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'langchain_pg_collection'


class LangchainPgEmbedding(models.Model):
    uuid = models.UUIDField(primary_key=True)
    collection = models.ForeignKey(
        LangChainPgCollection, models.DO_NOTHING, blank=True, null=True)
    embedding = VectorField(dimensions=768)
    document = models.TextField(blank=True, null=True)
    cmetadata = models.JSONField()
    custom_id = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'langchain_pg_embedding'


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}: {self.message}'
