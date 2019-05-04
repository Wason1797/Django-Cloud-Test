from django.db import models
from django.contrib.postgres.fields import JSONField


class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    person_name = models.CharField(max_length=50, blank=True, null=True)
    person_attributes = JSONField()

    def __str__(self):
        return self.person_id + ": " + self.person_name
