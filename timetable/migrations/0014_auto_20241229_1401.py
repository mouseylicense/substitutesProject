# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def make_many_teachers(apps, schema_editor):
    """
        Adds the Author object in Book.author to the
        many-to-many relationship in Book.authors
    """
    Class = apps.get_model('timetable', 'Class')

    for c in Class.objects.all():
        c.teachers.add(c.teacher)


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0013_class_teachers'),
    ]

    operations = [
        migrations.RunPython(make_many_teachers),
    ]