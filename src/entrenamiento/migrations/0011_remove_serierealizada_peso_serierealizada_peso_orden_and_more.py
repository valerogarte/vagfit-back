# Generated by Django 4.2.16 on 2024-10-31 14:02

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamiento', '0010_alter_serierealizada_ejercicio_realizado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serierealizada',
            name='peso',
        ),
        migrations.AddField(
            model_name='serierealizada',
            name='peso_orden',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='entrenamiento',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='serierealizada',
            name='descanso',
            field=models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='serierealizada',
            name='inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='serierealizada',
            name='repeticiones',
            field=models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='serierealizada',
            name='rer',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='serierealizada',
            name='velocidad_repeticion',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
