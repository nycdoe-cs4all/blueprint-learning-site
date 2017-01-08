from django.db import models
from django.contrib.postgres.fields import JSONField
import datetime
from django.contrib.auth.models import User


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


# Create your models here.
class Activity(models.Model):
    class Meta:
        # fix django's broken capitalization
        verbose_name_plural = "activities"

    user = models.ForeignKey(User)
    grade = models.ForeignKey(Grade)
    subject = models.ForeignKey(Subject)
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
