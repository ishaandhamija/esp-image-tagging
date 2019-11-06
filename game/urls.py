from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup/$', views.signup),
	url(r'^login/$', views.login),
	url(r'^get_ready_to_player_players/(?P<player_id>\d+)/$', views.get_ready_to_player_players),
	url(r'^start_task/$', views.start_task),
	url(r'^end_task/$', views.end_task),
	url(r'^logout/$', views.logout),
]
