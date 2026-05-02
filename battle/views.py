import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Song, TournamentResult


def tournament_home(request):
    return render(request, "battle/tournament.html")


def init_tournament(request):
    kpop_songs = list(Song.objects.filter(genre=Song.Genre.KPOP).values(
        "id", "title", "artist", "genre", "youtube_video_id"
    ))
    qpop_songs = list(Song.objects.filter(genre=Song.Genre.QPOP).values(
        "id", "title", "artist", "genre", "youtube_video_id"
    ))

    if len(kpop_songs) < 8 or len(qpop_songs) < 8:
        return JsonResponse({"error": "Not enough songs in the database."}, status=400)

    selected = random.sample(kpop_songs, 8) + random.sample(qpop_songs, 8)
    random.shuffle(selected)

    bracket = {
        "round": 1,
        "match_index": 0,
        "matches": [
            [selected[i], selected[i + 1]]
            for i in range(0, 16, 2)
        ],
        "winners": [],
    }

    request.session["bracket"] = bracket
    request.session.modified = True

    first_match = bracket["matches"][0]
    return JsonResponse({
        "song_a": first_match[0],
        "song_b": first_match[1],
        "round": bracket["round"],
        "match_number": 1,
        "total_matches": len(bracket["matches"]),
    })


@csrf_exempt
@require_POST
def submit_vote(request):
    bracket = request.session.get("bracket")
    if not bracket:
        return JsonResponse({"error": "No active tournament session."}, status=400)

    try:
        data = json.loads(request.body)
        winner_id = int(data.get("winner_id"))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid winner_id."}, status=400)

    current_match = bracket["matches"][bracket["match_index"]]
    valid_ids = [current_match[0]["id"], current_match[1]["id"]]

    if winner_id not in valid_ids:
        return JsonResponse({"error": "winner_id does not match current match."}, status=400)

    winner = current_match[0] if current_match[0]["id"] == winner_id else current_match[1]
    bracket["winners"].append(winner)
    bracket["match_index"] += 1

    if bracket["match_index"] < len(bracket["matches"]):
        next_match = bracket["matches"][bracket["match_index"]]
        request.session["bracket"] = bracket
        request.session.modified = True
        return JsonResponse({
            "status": "next",
            "song_a": next_match[0],
            "song_b": next_match[1],
            "round": bracket["round"],
            "match_number": bracket["match_index"] + 1,
            "total_matches": len(bracket["matches"]),
        })

    if len(bracket["winners"]) == 1:
        request.session["bracket"] = bracket
        request.session.modified = True
        return JsonResponse({
            "status": "tournament_over",
            "winner": bracket["winners"][0],
        })

    next_round_matches = [
        [bracket["winners"][i], bracket["winners"][i + 1]]
        for i in range(0, len(bracket["winners"]), 2)
    ]

    bracket["round"] += 1
    bracket["match_index"] = 0
    bracket["matches"] = next_round_matches
    bracket["winners"] = []

    request.session["bracket"] = bracket
    request.session.modified = True

    first_match = next_round_matches[0]
    return JsonResponse({
        "status": "next",
        "song_a": first_match[0],
        "song_b": first_match[1],
        "round": bracket["round"],
        "match_number": 1,
        "total_matches": len(next_round_matches),
    })


@csrf_exempt
@require_POST
def record_winner(request):
    bracket = request.session.get("bracket")
    if not bracket:
        return JsonResponse({"error": "No active tournament session."}, status=400)

    try:
        data = json.loads(request.body)
        winner_id = int(data.get("winner_id"))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid winner_id."}, status=400)

    try:
        song = Song.objects.get(id=winner_id)
    except Song.DoesNotExist:
        return JsonResponse({"error": "Song not found."}, status=404)

    TournamentResult.objects.create(
        winner=song,
        session_key=request.session.session_key or "",
    )

    del request.session["bracket"]
    request.session.modified = True

    return JsonResponse({"status": "recorded", "winner": {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": song.genre,
        "youtube_video_id": song.youtube_video_id,
    }})