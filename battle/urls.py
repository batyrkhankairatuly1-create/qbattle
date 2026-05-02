from django.urls import path
from . import views

app_name = "battle"

urlpatterns = [
    path("", views.tournament_home, name="home"),
    path("api/init/", views.init_tournament, name="init_tournament"),
    path("api/vote/", views.submit_vote, name="submit_vote"),
    path("api/winner/", views.record_winner, name="record_winner"),
]