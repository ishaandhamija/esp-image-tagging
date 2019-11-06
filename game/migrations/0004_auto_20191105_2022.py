# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-05 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_player_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_img', models.CharField(max_length=100)),
                ('player_1_answer_img', models.CharField(max_length=100)),
                ('player_2_answer_img', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='questions',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='task',
            name='answer_responses',
            field=models.ManyToManyField(to='game.AnswerResponse'),
        ),
    ]
