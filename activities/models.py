from django.db import models
from django.contrib.postgres.fields import JSONField
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Concept(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Software(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    organization = models.CharField(max_length=255, default="", blank=True)
    link = models.CharField(max_length=255, default="", blank=True)
    full_name = models.CharField(max_length=255, default="", blank=True)


# Create your models here.
class Activity(models.Model):
    class Meta:
        # fix django's broken capitalization
        verbose_name_plural = "activities"

    user = models.ForeignKey(User)
    grade = models.ForeignKey(Grade)
    subject = models.ForeignKey(Subject)
    software = models.ForeignKey(Software)
    # devices = models.ManyToManyField(Device)

    date_added = models.DateTimeField(auto_now_add=True)

    title = models.CharField(max_length=255)
    # grade_name = models.CharField(max_length=255)
    # subject_name = models.CharField(max_length=255)

    google_file_id = models.CharField(max_length=255)

    html_body = models.TextField()
    plain_body = models.TextField()
    body = JSONField()

    approved = models.BooleanField(default=False)

    def _get_copy_url(self):
        return self.google_file_id.replace('edit', 'copy')

    copy_url = property(_get_copy_url)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
