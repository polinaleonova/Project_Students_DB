from os import path
from django.db import models


class Student(models.Model):
    student_name = models.CharField(max_length=50)
    date_birthday = models.DateField(null=True)
    ticket_number = models.IntegerField(null=True)
    foto = models.ImageField(
        upload_to='img/foto',
        null=True,
        blank=True
    )
    group = models.ForeignKey('Group',
                              blank=True,
                              # null=True
    )

    def __unicode__(self):
        return self.student_name


class Group(models.Model):
    name_group = models.CharField(max_length=50)
    praepostor = models.OneToOneField(Student,
                                      related_name='praepostor_of_group',
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True)

    def __unicode__(self):
        return self.name_group


