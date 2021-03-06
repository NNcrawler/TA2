# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 02:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=38)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=38)),
                ('waktu', models.FloatField(blank=True, null=True)),
                ('alternative', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alter', to='AdaptiveLearningPath.Course')),
                ('prerequisit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prereq', to='AdaptiveLearningPath.Course')),
            ],
        ),
        migrations.CreateModel(
            name='EdgeConcept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dari', to='AdaptiveLearningPath.Concept')),
                ('ke', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ke', to='AdaptiveLearningPath.Concept')),
            ],
        ),
        migrations.CreateModel(
            name='LearningStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=38)),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdaptiveLearningPath.Course')),
                ('knowledge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdaptiveLearningPath.Concept')),
                ('learningStyle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdaptiveLearningPath.LearningStyle')),
            ],
        ),
    ]
