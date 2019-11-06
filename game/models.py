# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class AnswerResponse(models.Model):
	primary_img = models.CharField(max_length=100)
	player_1_answer_img = models.CharField(max_length=100)
	player_2_answer_img = models.CharField(max_length=100)


class Player(models.Model):

	# Player status
	OFFLINE = 'offline'
	IDLE = 'idle'
	READY_TO_PLAY = 'ready_to_play'
	IN_GAME = 'in_game'

	name = models.CharField(max_length=50)
	email_address = models.EmailField(max_length=50)
	password = models.CharField(max_length=10)
	total_no_of_tasks = models.IntegerField(default=0)
	total_score = models.IntegerField(default=0)
	status = models.CharField(max_length=20)


class Task(models.Model):
	no_of_ques = models.IntegerField(default=0)
	score = models.IntegerField(default=0)
	answer_responses = models.ManyToManyField(AnswerResponse) 
	players = models.ManyToManyField(Player)

