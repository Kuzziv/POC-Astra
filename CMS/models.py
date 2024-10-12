# CMS_backend/CMS/models.py
import uuid
from django.db import models


# User model
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Increased size for hashed passwords
    email = models.EmailField(unique=True)
    personal_phone = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.id})"


# ParentPhone model for storing multiple parent phone numbers
class ParentPhone(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="parent_phones"
    )
    phone_number = models.CharField(max_length=20)
    parent_name = models.CharField(
        max_length=255, blank=True
    )  # Optional parent name for identification

    def __str__(self):
        return f"{self.parent_name if self.parent_name else 'Parent'} - {self.phone_number} ({self.user.username})"


# Character model
class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="characters")
    race = models.ForeignKey("Race", on_delete=models.SET_NULL, null=True, blank=True)
    religion = models.ForeignKey(
        "Religion", on_delete=models.SET_NULL, null=True, blank=True
    )
    xp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# Race model
class Race(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# Religion model
class Religion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
