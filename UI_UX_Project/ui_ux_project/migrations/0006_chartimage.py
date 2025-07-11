# Generated by Django 3.2.16 on 2025-01-11 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui_ux_project', '0005_rename_skill_count_topskills_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChartImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chart_type', models.CharField(max_length=50, unique=True, verbose_name='Тип графика')),
                ('image', models.ImageField(upload_to='charts/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'График',
                'verbose_name_plural': 'Графики',
            },
        ),
    ]
