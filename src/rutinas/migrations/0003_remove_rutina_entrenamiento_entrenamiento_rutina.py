# Generated by Django 4.2.16 on 2024-10-23 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rutinas', '0002_remove_ejerciciopersonalizado_entrenamiento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rutina',
            name='entrenamiento',
        ),
        migrations.AddField(
            model_name='entrenamiento',
            name='rutina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entrenamientos', to='rutinas.rutina'),
        ),
    ]
