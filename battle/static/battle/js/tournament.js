let playerA = null;
let playerB = null;
let playerWinner = null;
let ytReady = false;
let pendingMatch = null;
let currentSongA = null;
let currentSongB = null;
let kpopWins = 0;
let qpopWins = 0;

function showScreen(id) {
    document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

function buildPips(total, current) {
    const track = document.getElementById("pip-track");
    track.innerHTML = "";
    for (let i = 0; i < total; i++) {
        const pip = document.createElement("div");
        pip.className = "pip" + (i < current - 1 ? " done" : i === current - 1 ? " active" : "");
        track.appendChild(pip);
    }
}

function getCsrfToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");
    for (const c of cookies) {
        const trimmed = c.trim();
        if (trimmed.startsWith(name + "=")) {
            return decodeURIComponent(trimmed.slice(name.length + 1));
        }
    }
    return "";
}

function resetPlayerDiv(id) {
    const el = document.getElementById(id);
    el.innerHTML = "";
    const newDiv = document.createElement("div");
    newDiv.id = id;
    el.parentNode.replaceChild(newDiv, el);
}

function loadPlayers(vidA, vidB) {
    if (playerA) { try { playerA.destroy(); } catch(e) {} playerA = null; }
    if (playerB) { try { playerB.destroy(); } catch(e) {} playerB = null; }

    resetPlayerDiv("player-a");
    resetPlayerDiv("player-b");

    playerA = new YT.Player("player-a", {
        videoId: vidA,
        host: "https://www.youtube-nocookie.com",
        playerVars: { rel: 0, modestbranding: 1 },
    });

    playerB = new YT.Player("player-b", {
        videoId: vidB,
        host: "https://www.youtube-nocookie.com",
        playerVars: { rel: 0, modestbranding: 1 },
    });
}

async function initTournament() {
    document.getElementById("btn-start").disabled = true;
    kpopWins = 0;
    qpopWins = 0;

    const res = await fetch(INIT_URL);
    const data = await res.json();

    if (data.error) {
        alert(data.error);
        document.getElementById("btn-start").disabled = false;
        return;
    }

    showScreen("screen-battle");
    loadMatch(data);
}

function loadMatch(data) {
    currentSongA = data.song_a;
    currentSongB = data.song_b;

    document.getElementById("round-label").textContent = "Round " + data.round;
    document.getElementById("match-counter").textContent = "Match " + data.match_number + " / " + data.total_matches;
    buildPips(data.total_matches, data.match_number);

    document.getElementById("artist-a").textContent = currentSongA.artist;
    document.getElementById("title-a").textContent = currentSongA.title;
    document.getElementById("tag-a").textContent = currentSongA.genre === "kpop" ? "K-POP" : "Q-POP";

    document.getElementById("artist-b").textContent = currentSongB.artist;
    document.getElementById("title-b").textContent = currentSongB.title;
    document.getElementById("tag-b").textContent = currentSongB.genre === "kpop" ? "K-POP" : "Q-POP";

    document.getElementById("vote-a").disabled = false;
    document.getElementById("vote-b").disabled = false;

    if (ytReady) {
        loadPlayers(currentSongA.youtube_video_id, currentSongB.youtube_video_id);
    } else {
        pendingMatch = data;
    }
}

async function castVote(winnerId) {
    document.getElementById("vote-a").disabled = true;
    document.getElementById("vote-b").disabled = true;

    if (playerA) { try { playerA.pauseVideo(); } catch(e) {} }
    if (playerB) { try { playerB.pauseVideo(); } catch(e) {} }

    const loser = winnerId === currentSongA.id ? currentSongB : currentSongA;
    if (loser.genre === "kpop") kpopWins--;
    else qpopWins--;

    const winner = winnerId === currentSongA.id ? currentSongA : currentSongB;
    if (winner.genre === "kpop") kpopWins++;
    else qpopWins++;

    const res = await fetch(VOTE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify({ winner_id: winnerId }),
    });

    const data = await res.json();

    if (data.status === "next") {
        loadMatch(data);
    } else if (data.status === "tournament_over") {
        await recordWinner(data.winner);
    }
}

async function recordWinner(winner) {
    await fetch(WINNER_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify({ winner_id: winner.id }),
    });

    showWinnerScreen(winner);
}

function showWinnerScreen(winner) {
    document.getElementById("winner-artist").textContent = winner.artist;
    document.getElementById("winner-title").textContent = winner.title;

    const badge = document.getElementById("winner-genre");
    badge.textContent = winner.genre === "kpop" ? "K-POP" : "Q-POP";
    badge.className = "winner-badge " + winner.genre;

    const totalMatches = kpopWins + qpopWins;
    const kpopPct = totalMatches ? Math.round((kpopWins / totalMatches) * 100) : 0;
    const qpopPct = 100 - kpopPct;

    document.getElementById("analytics-block").innerHTML = `
        <div class="analytics-bar-wrap">
            <span class="analytics-genre-label" style="color:var(--accent-k)">K-POP</span>
            <span class="analytics-number" style="color:var(--accent-k)">${kpopPct}%</span>
            <span class="analytics-desc">${kpopWins} match wins</span>
        </div>
        <div class="analytics-bar-wrap">
            <span class="analytics-genre-label" style="color:var(--accent-q)">Q-POP</span>
            <span class="analytics-number" style="color:var(--accent-q)">${qpopPct}%</span>
            <span class="analytics-desc">${qpopWins} match wins</span>
        </div>
    `;

    showScreen("screen-winner");

    if (playerWinner) { try { playerWinner.destroy(); } catch(e) {} playerWinner = null; }
    resetPlayerDiv("player-winner");

    playerWinner = new YT.Player("player-winner", {
        videoId: winner.youtube_video_id,
        host: "https://www.youtube-nocookie.com",
        playerVars: { rel: 0, modestbranding: 1, autoplay: 1 },
    });
}

window.onYouTubeIframeAPIReady = function () {
    ytReady = true;
    if (pendingMatch) {
        loadPlayers(pendingMatch.song_a.youtube_video_id, pendingMatch.song_b.youtube_video_id);
        pendingMatch = null;
    }
};

document.getElementById("btn-start").addEventListener("click", initTournament);
document.getElementById("vote-a").addEventListener("click", () => castVote(currentSongA.id));
document.getElementById("vote-b").addEventListener("click", () => castVote(currentSongB.id));

document.getElementById("btn-restart").addEventListener("click", () => {
    showScreen("screen-start");
    document.getElementById("btn-start").disabled = false;
    if (playerA) { try { playerA.destroy(); } catch(e) {} playerA = null; }
    if (playerB) { try { playerB.destroy(); } catch(e) {} playerB = null; }
    if (playerWinner) { try { playerWinner.destroy(); } catch(e) {} playerWinner = null; }
});