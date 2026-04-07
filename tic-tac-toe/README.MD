# 🎯 Project Milestones – Real-Time Multiplayer Tic-Tac-Toe

---

## 🟢 Milestone 1: Basic Game Logic

**Goal:** Create core Tic-Tac-Toe functionality

**What I implemented:**

* 3x3 board UI using HTML/CSS
* Click-based moves using JavaScript
* Win/draw detection using pattern matching logic

**Tech:** JS + DOM manipulation

---

## 🟢 Milestone 2: Player vs AI

**Goal:** Enable single-player mode

**What I implemented:**

* Simple AI using random move selection
* Automatic move after user turn
* Game reset functionality

**Tech:** JavaScript logic

---

## 🟢 Milestone 3: Authentication System

**Goal:** Add user login system

**What I implemented:**

* Signup & Login using Flask
* Session management with Flask-Login
* SQLite database for storing users

**Tech:** Flask, SQLAlchemy

---

## 🟢 Milestone 4: Multiplayer (Real-Time)

**Goal:** Enable real-time gameplay

**What I implemented:**

* WebSocket communication using Flask-SocketIO
* Room-based gameplay (join via Room ID)
* Player roles (X / O / Viewer)

**Tech:** Socket.IO

---

## 🟢 Milestone 5: Leaderboard System

**Goal:** Track player performance

**What I implemented:**

* Stored wins, losses, draws in DB
* Displayed leaderboard sorted by rating
* Created leaderboard UI page

**Tech:** SQLAlchemy

---

## 🟢 Milestone 6: ELO Rating System

**Goal:** Add fair ranking system

**What I implemented:**

* ELO formula for rating calculation
* Dynamic rating updates based on opponent strength
* Integrated into game result logic

**Tech:** Python math logic

---

## 🟢 Milestone 7: Tournament System

**Goal:** Simulate competition

**What I implemented:**

* Players join tournament
* Automatic match pairing
* Winner tracking system

**Tech:** Backend data structure

---

## 🟢 Milestone 8: Achievements (Badges)

**Goal:** Add gamification

**What I implemented:**

* Badges like:

  * First Win 🥇
  * 10 Wins 🔥
  * Pro Player 🏆
* Triggered based on performance

**Tech:** Conditional logic in backend

---

## 🟢 Milestone 9: Friend System + Chat

**Goal:** Add social interaction

**What I implemented:**

* Friend request & accept system
* Stored relationships in DB
* Real-time chat using Socket.IO

**Tech:** Flask + WebSockets

---

# 🏆 FINAL OUTCOME

Built a **full-stack real-time multiplayer gaming platform** with:

* Authentication
* Real-time communication
* Ranking system
* Social features
* Tournament simulation

---

# 💡 KEY LEARNING

* Real-time systems (WebSockets)
* Backend architecture (Flask)
* Database design (SQLAlchemy)
* State management for multiplayer
* Building scalable feature-based systems


## ▶️ How to Run & Play the Game

### ⚙️ Run Locally

1. Clone the repository

```
git clone <your-repo-url>
cd tic-tac-toe
```

2. Create virtual environment

```
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run the application

```
python app.py
```

5. Open in browser

```
http://localhost:10517
```

---

### 🎮 How to Play

#### 🔐 Step 1: Signup & Login

* Create an account
* Login to access the game

---

#### 👥 Step 2: Multiplayer Game

* Open **two browsers** (or Incognito mode)
* Login with **two different users**
* Enter the same **Room ID**
* Click **Join Room**

---

#### ⚡ Step 3: Start Playing

* One player becomes **X**, other becomes **O**
* Take turns clicking cells
* Game ends with **Winner or Draw**

---

#### 💬 Step 4: Chat

* Use chat box to send messages in real-time

---

#### 🏆 Step 5: Leaderboard

* Check rankings based on ELO rating

---

#### 👥 Step 6: Friend System

* Send friend requests using username
* Accept requests and manage friends

---

#### 🏁 Step 7: Tournament

* Join tournament
* Play matches and track winners

---

### ⚠️ Notes

* Use **different browsers or Incognito mode** to simulate multiple users
* Database resets if `instance/` folder is deleted
* Default port: **10517**

---

### ✅ Example

* User1 → Chrome
* User2 → Incognito

Both join:

```
room1
```

Start playing 🎮



# THANK YOU 💡💡