from os import path
from django.db import models


class Student(models.Model):
    student_name = models.CharField(max_length=50)
    date_birthday = models.DateField()
    tiket_number = models.IntegerField()
    foto = models.ImageField(
    upload_to='img/foto',
        null=True,
        blank=True
    )
    group = models.ForeignKey('Group')

    def __unicode__(self):
        return self.student_name


class Group(models.Model):
    name_group = models.CharField(max_length=50)
    praepostor = models.OneToOneField(Student,
                                      related_name='praepostor_of_group',
                                      null=True)

    def __unicode__(self):
        return self.name_group


