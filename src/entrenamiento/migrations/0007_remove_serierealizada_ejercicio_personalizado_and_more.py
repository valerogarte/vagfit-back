# Generated by Django 4.2.16 on 2024-10-27 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entrenamiento', '0006_alter_serierealizada_options_serierealizada_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serierealizada',
            name='ejercicio_personalizado',
        ),
        migrations.AddField(
            model_name='serierealizada',
            name='ejercicio_realizado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='series', to='entrenamiento.ejerciciorealizado'),
        ),
    ]