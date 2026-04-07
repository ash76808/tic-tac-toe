from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, emit

# ------------------ INIT ------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

socketio = SocketIO(app, cors_allowed_origins="*")


# ------------------ USER MODEL ------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    rating = db.Column(db.Integer, default=1000)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    draws = db.Column(db.Integer, default=0)
    badges = db.Column(db.String(500), default="")

    friends = db.Column(db.String(500), default="")
    friend_requests = db.Column(db.String(500), default="")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------ HELPERS ------------------

def add_badge(user, badge):
    if badge not in user.badges:
        user.badges += badge + ", "


def add_to_list(field, value):
    items = field.split(",") if field else []
    if value not in items:
        items.append(value)
    return ",".join(items)


def remove_from_list(field, value):
    items = field.split(",") if field else []
    items = [i for i in items if i != value]
    return ",".join(items)


# ------------------ STORAGE ------------------

rooms = {}

tournament = {
    "players": [],
    "matches": [],
    "winners": []
}


# ------------------ GAME LOGIC ------------------

def check_winner(board):
    patterns = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for p in patterns:
        a,b,c = p
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None


# ------------------ ELO ------------------

def calculate_elo(rating_a, rating_b, score_a, k=32):
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    return int(rating_a + k * (score_a - expected_a))


# ------------------ AUTH ------------------

@app.route("/")
@login_required
def home():
    return render_template(
        "index.html",
        user=current_user.username,
        user_badges=current_user.badges
    )


@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "User already exists ❌"

        db.session.add(User(username=username, password=password))
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            login_user(user)
            return redirect(url_for("home"))

        return "Invalid credentials ❌"

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ------------------ FRIEND SYSTEM ------------------

@app.route("/friends")
@login_required
def friends():
    return render_template(
        "friends.html",
        friends=current_user.friends.split(",") if current_user.friends else [],
        requests=current_user.friend_requests.split(",") if current_user.friend_requests else []
    )


# ✅ FIXED ROUTE (IMPORTANT)
@app.route("/send_request", methods=["GET"])
@login_required
def send_request():
    username = request.args.get("username")

    if not username:
        return redirect(url_for("friends"))

    user = User.query.filter_by(username=username).first()

    if user and user.username != current_user.username:
        if current_user.username not in (user.friend_requests or ""):
            user.friend_requests = add_to_list(user.friend_requests, current_user.username)
            db.session.commit()

    return redirect(url_for("friends"))


@app.route("/accept_request/<username>")
@login_required
def accept_request(username):
    user = User.query.filter_by(username=username).first()

    if user:
        current_user.friends = add_to_list(current_user.friends, username)
        user.friends = add_to_list(user.friends, current_user.username)

        current_user.friend_requests = remove_from_list(current_user.friend_requests, username)

        db.session.commit()

    return redirect(url_for("friends"))


# ------------------ LEADERBOARD ------------------

@app.route("/leaderboard")
@login_required
def leaderboard():
    users = User.query.order_by(User.rating.desc()).all()
    return render_template("leaderboard.html", users=users)


# ------------------ TOURNAMENT ------------------

@app.route("/tournament")
@login_required
def tournament_page():
    return render_template("tournament.html", data=tournament)


@app.route("/join_tournament")
@login_required
def join_tournament():
    if current_user.username not in tournament["players"]:
        tournament["players"].append(current_user.username)
    return redirect(url_for("tournament_page"))


@app.route("/start_tournament")
@login_required
def start_tournament():
    players = tournament["players"]
    tournament["matches"] = []

    for i in range(0, len(players), 2):
        if i + 1 < len(players):
            tournament["matches"].append((players[i], players[i+1]))

    return redirect(url_for("tournament_page"))


# ------------------ SOCKET EVENTS ------------------

@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)

    if room not in rooms:
        rooms[room] = {
            "board": [""] * 9,
            "players": {},
            "turn": "X"
        }

    game = rooms[room]

    if "X" not in game["players"]:
        game["players"]["X"] = current_user.username
        role = "X"
    elif "O" not in game["players"]:
        game["players"]["O"] = current_user.username
        role = "O"
    else:
        role = "Viewer"

    emit("player_role", role)
    emit("update", game, room=room)


@socketio.on("move")
def on_move(data):
    room = data["room"]
    pos = data["position"]
    player = data["player"]

    game = rooms.get(room)
    if not game:
        return

    if game["turn"] != player:
        return

    if game["board"][pos] == "":
        game["board"][pos] = player

        winner = check_winner(game["board"])

        if winner:
            update_stats(game, winner)
            emit("game_over", winner, room=room)

            game["board"] = [""] * 9
            game["turn"] = "X"
        else:
            game["turn"] = "O" if player == "X" else "X"

        emit("update", game, room=room)


@socketio.on("send_message")
def handle_message(data):
    room = data["room"]
    message = data["message"]

    if not message.strip():
        return

    emit("receive_message", {
        "user": current_user.username,
        "message": message
    }, room=room)


# ------------------ UPDATE STATS ------------------

def update_stats(game, winner):
    player_X = game["players"].get("X")
    player_O = game["players"].get("O")

    user_X = User.query.filter_by(username=player_X).first()
    user_O = User.query.filter_by(username=player_O).first()

    if not user_X or not user_O:
        return

    rating_X = user_X.rating
    rating_O = user_O.rating

    if winner == "Draw":
        score_X = 0.5
        score_O = 0.5
        user_X.draws += 1
        user_O.draws += 1

    elif winner == "X":
        score_X = 1
        score_O = 0
        user_X.wins += 1
        user_O.losses += 1
        tournament["winners"].append(player_X)

    elif winner == "O":
        score_X = 0
        score_O = 1
        user_O.wins += 1
        user_X.losses += 1
        tournament["winners"].append(player_O)

    user_X.rating = calculate_elo(rating_X, rating_O, score_X)
    user_O.rating = calculate_elo(rating_O, rating_X, score_O)

    for user in [user_X, user_O]:
        if user.wins == 1:
            add_badge(user, "First Win 🥇")
        if user.wins == 10:
            add_badge(user, "10 Wins 🔥")
        if user.rating >= 1200:
            add_badge(user, "Pro Player 🏆")

    db.session.commit()


# ------------------ RUN ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    socketio.run(app, host="0.0.0.0", port=10517, debug=True)