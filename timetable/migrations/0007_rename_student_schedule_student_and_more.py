# Generated by Django 4.2.13 on 2024-08-06 09:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("timetable", "0006_remove_schedule_thursday_fourth_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="schedule",
            old_name="Student",
            new_name="student",
        ),
        migrations.AddField(
            model_name="student",
            name="last_schedule_invite",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 6, 12, 0, 5, 323229)
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="monday_first",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Monday",
                    "hour": datetime.time(9, 15),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="monday_first_classes",
                to="timetable.class",
                verbose_name="שני 09:15",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="monday_fourth",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Monday",
                    "hour": datetime.time(12, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="monday_fourth_classes",
                to="timetable.class",
                verbose_name="שני 12:45",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="monday_second",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Monday",
                    "hour": datetime.time(10, 7),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="monday_second_classes",
                to="timetable.class",
                verbose_name="שני 10:07",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="monday_third",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Monday",
                    "hour": datetime.time(11, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="monday_third_classes",
                to="timetable.class",
                verbose_name="שני 11:45",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="sunday_first",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Sunday",
                    "hour": datetime.time(9, 15),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sunday_first_classes",
                to="timetable.class",
                verbose_name="ראשון 09:15",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="sunday_fourth",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Sunday",
                    "hour": datetime.time(12, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sunday_fourth_classes",
                to="timetable.class",
                verbose_name="ראשון 12:45",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="sunday_second",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Sunday",
                    "hour": datetime.time(10, 7),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sunday_second_classes",
                to="timetable.class",
                verbose_name="ראשון 10:07",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="sunday_third",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Sunday",
                    "hour": datetime.time(11, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="sunday_third_classes",
                to="timetable.class",
                verbose_name="ראשון 11:45",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="thursday_first",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Thursday",
                    "hour": datetime.time(9, 15),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="thursday_first_classes",
                to="timetable.class",
                verbose_name="חמישי 09:15",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="thursday_second",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Thursday",
                    "hour": datetime.time(10, 7),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="thursday_second_classes",
                to="timetable.class",
                verbose_name="חמישי 10:07",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="tuesday_first",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Tuesday",
                    "hour": datetime.time(9, 15),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tuesday_first_classes",
                to="timetable.class",
                verbose_name="שלישי 09:15",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="tuesday_fourth",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Tuesday",
                    "hour": datetime.time(12, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tuesday_fourth_classes",
                to="timetable.class",
                verbose_name="שלישי 12:45",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="tuesday_second",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Tuesday",
                    "hour": datetime.time(10, 7),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tuesday_second_classes",
                to="timetable.class",
                verbose_name="שלישי 10:07",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="tuesday_third",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Tuesday",
                    "hour": datetime.time(11, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tuesday_third_classes",
                to="timetable.class",
                verbose_name="שלישי 11:45",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="wednesday_first",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Wednesday",
                    "hour": datetime.time(9, 15),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="wednesday_first_classes",
                to="timetable.class",
                verbose_name="רביעי 09:15",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="wednesday_fourth",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Wednesday",
                    "hour": datetime.time(12, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="wednesday_fourth_classes",
                to="timetable.class",
                verbose_name="רביעי 12:45",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="wednesday_second",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Wednesday",
                    "hour": datetime.time(10, 7),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="wednesday_second_classes",
                to="timetable.class",
                verbose_name="רביעי 10:07",
            ),
        ),
        migrations.AlterField(
            model_name="schedule",
            name="wednesday_third",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={
                    "day_of_week": "Wednesday",
                    "hour": datetime.time(11, 45),
                },
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="wednesday_third_classes",
                to="timetable.class",
                verbose_name="רביעי 11:45",
            ),
        ),
    ]
