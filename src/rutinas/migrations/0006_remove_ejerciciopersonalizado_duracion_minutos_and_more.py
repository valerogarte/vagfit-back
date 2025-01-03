# Generated by Django 4.2.16 on 2024-10-23 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutinas', '0005_remove_sesion_ejercicio_personalizado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ejerciciopersonalizado',
            name='duracion_minutos',
        ),
        migrations.RemoveField(
            model_name='ejerciciopersonalizado',
            name='repeticiones',
        ),
        migrations.CreateModel(
            name='SeriePersonalizada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repeticiones', models.IntegerField(default=10)),
                ('duracion_minutos', models.IntegerField(default=5)),
                ('ejercicio_personalizado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rutinas.ejerciciopersonalizado')),
            ],
        ),
    ]
