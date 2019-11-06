# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core.serializers import serialize
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from game.models import *
from game.serializers import *

import json
import logging
import traceback

logger = logging.getLogger('esp-image-tagging')


@api_view(http_method_names=['POST'])
def signup(request):
	try:
		data = request.data
		
		existing_player = Player.objects.filter(email_address=data.get('email_address')).last()
		
		if existing_player:
			logger.info('User already exists')
			return Response(data={
				'message': 'User already signed up',
			}, status=status.HTTP_200_OK)
		
		player = Player(name=data.get('name'), email_address=data.get('email_address'), 
						password=data.get('password'), status=Player.OFFLINE)
		player.save()
		logger.info('User signed up successfully')
		
		return Response(data={
				'message': 'User signed up successfully',
			}, status=status.HTTP_200_OK)
	
	except Exception as err:
		traceback.print_exc()
		logger.error('Error in signing up: %s', err.message)
		
		return Response(data={
				'message': 'Sign up failed',
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=['PATCH'])
def login(request):
	try:
		data = request.data
		
		existing_player = Player.objects.filter(email_address=data.get('email_address')).last()
		
		if existing_player:
			if existing_player.password != data.get('password'):
				return Response(data={
						'message': 'Incorrect Password',
					}, status=status.HTTP_200_OK)
			
			existing_player.status = Player.IDLE
			existing_player.save()
			serializer = PlayerSerializer(existing_player)
			return Response(data={
					'message': 'Login successful',
					'player_data': serializer.data
				}, status=status.HTTP_200_OK)
		
		return Response(data={
				'message': 'Account does not exist, please sign up first',
			}, status=status.HTTP_200_OK)
	
	except Exception as err:
		traceback.print_exc()
		logger.error('Error in login: %s', err.message)
		
		return Response(data={
				'message': 'Internal Server Error',
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=['GET'])
def get_ready_to_player_players(request, player_id):
	try:	
		player_1 = Player.objects.filter(id=player_id).last()
		player_1.status = Player.READY_TO_PLAY
		player_1.save()

		other_players = Player.objects.filter(~Q(id=player_id), status=Player.READY_TO_PLAY)
		ready_to_play_players = serialize('json', other_players)

		return Response(data={
				'data': ready_to_play_players,
			}, status=status.HTTP_200_OK)
	
	except Exception as err:
		traceback.print_exc()
		logger.error('Error starting task: %s', err.message)
		
		return Response(data={
				'message': 'Internal Server Error',
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=['PATCH'])
def start_task(request):
	try:
		data = request.data
		player_id_1 = data.get('player_id_1')
		player_id_2 = data.get('player_id_2')
		
		player_1 = Player.objects.filter(id=player_id_1).last()
		player_1.status = Player.IN_GAME
		player_1.save()
		player_2 = Player.objects.filter(id=player_id_2).last()
		player_2.status = Player.IN_GAME
		player_2.save()

		task = Task()
		task.save()
		task.players.add(player_1)
		task.players.add(player_2)
		task.save()

		return Response(data={
				'message': 'entered task successfully',
				'task_id': task.id
			}, status=status.HTTP_200_OK)
	
	except Exception as err:
		traceback.print_exc()
		logger.error('Error entering task: %s', err.message)
		
		return Response(data={
				'message': 'Internal Server Error',
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=['POST'])
def end_task(request):
	try:
		data = request.data
		task = Task.objects.filter(id=data.get('task_id')).last()
		answer_responses = data.get('answer_responses')
		score = 0
		task.no_of_ques = len(answer_responses)
		for answer_response in answer_responses:
			ar_obj = AnswerResponse(primary_img=answer_response.get('primary_img'),
				player_1_answer_img=answer_response.get('player_1_answer_img'),
				player_2_answer_img=answer_response.get('player_2_answer_img'))
			ar_obj.save()
			task.answer_responses.add(ar_obj)
			if ar_obj.player_1_answer_img == ar_obj.player_2_answer_img:
				score += 1
		task.players.update(status=Player.IDLE)
		task.score = score
		task.save()

		player_1 = task.players.first()
		player_1.total_score += task.score
		player_1.total_no_of_tasks += 1
		player_1.save()
		player_2 = task.players.last()
		player_2.total_score += task.score
		player_2.total_no_of_tasks += 1
		player_2.save()

		return Response(data={
				'message': 'ended task successfully',
				'task_score': task.score
			}, status=status.HTTP_200_OK)
	
	except Exception as err:
		traceback.print_exc()
		logger.error('Error ending task: %s', err.message)
		
		return Response(data={
				'message': 'Internal Server Error',
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(http_method_names=['PATCH'])
def logout(request):
	try:
		data = request.data
		player_id = data.get('player_id')
		
		player = Player.objects.filter(id=player_id).last()
		player.status = Player.OFFLINE
		player.save()

		return Response(data={
				'message': 'logged out successfully',
			}, status=status.HTTP_200_OK)
	
	except Exception as err:
		traceback.print_exc()
		logger.error('Error logging out: %s', err.message)
		
		return Response(data={
				'message': 'Internal Server Error',
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

