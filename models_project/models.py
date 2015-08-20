import json

from django.db import models
from django.db.models import signals
from sorl.thumbnail.shortcuts import get_thumbnail
from sorl.thumbnail.fields import ImageField


class Student(models.Model):
    student_name = models.CharField(max_length=50)
    date_birthday = models.DateField(null=True)
    ticket_number = models.IntegerField(null=True)
    photo = ImageField(
        upload_to='img/photo',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
    )

    def get_thumbnail_html(self):
        img = self.photo
        html = ''
        if img.name != '':
            img_resize_url = unicode(get_thumbnail(img, '50x50').url)
            html = '<img src="/static/{}" alt="photo"/>'.format(img_resize_url)
        return html

    get_thumbnail_html.allow_tags = True

    def __unicode__(self):
        return self.student_name


class Group(models.Model):
    name_group = models.CharField(max_length=50)
    monitor = models.OneToOneField(Student,
                                      related_name='monitor_of_group',
                                      on_delete=models.SET_NULL,
                                      blank=True,
                                      null=True)

    def __unicode__(self):
        return self.name_group


class History(models.Model):
    model_id = models.CharField(max_length=255,
                                null=True,
                                default=None)
    model_type = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    at = models.DateTimeField(auto_now_add=True)
    model_json = models.TextField()

    def __unicode__(self):
        return '{} - {} - at {}'.format(self.action, self.model_type, self.at)

def _handler_action(sender, instance, action):
    for_json = {}
    for key, value in instance.__dict__.iteritems():
        try:
            json.dumps(value)
            for_json[key] = value
        except TypeError:
            pass
    History.objects.create(
        model_id=instance.id,
        model_type=sender.__name__,
        model_json=json.dumps(for_json),
        action=action
    )


def on_remove(sender, instance, **kwargs):
    _handler_action(sender, instance, 'delete')


def on_save(sender, instance, **kwargs):
    _handler_action(
        sender, instance, 'create' if instance.id is None else 'edit'
    )

signals.pre_delete.connect(on_remove, sender=Group)
signals.pre_save.connect(on_save, sender=Group)
signals.pre_delete.connect(on_remove, sender=Student)
signals.pre_save.connect(on_save, sender=Student)
