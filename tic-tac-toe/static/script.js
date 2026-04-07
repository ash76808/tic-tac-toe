const socket = io();

let room = "";
let player = "";
let board = ["","","","","","","","",""];

const boardDiv = document.getElementById("board");

// ------------------ BOARD ------------------

function createBoard() {
    boardDiv.innerHTML = "";

    board.forEach((cell, index) => {
        const div = document.createElement("div");
        div.classList.add("cell");
        div.innerText = cell;

        div.onclick = () => makeMove(index);

        boardDiv.appendChild(div);
    });
}

// ------------------ JOIN ROOM ------------------

function joinRoom() {
    room = document.getElementById("room").value;

    if (!room) {
        alert("Enter room id");
        return;
    }

    socket.emit("join", { room: room });
}

// ------------------ SOCKET EVENTS ------------------

socket.on("player_role", (role) => {
    player = role;
    document.getElementById("playerRole").innerText = "You are: " + role;
});

socket.on("update", (game) => {
    board = game.board;
    createBoard();

    // ✅ NEW: show turn
    document.getElementById("status").innerText =
        "Turn: " + game.turn;
});

socket.on("game_over", (winner) => {
    if (winner === "Draw") {
        alert("Game Draw 🤝");
    } else {
        alert("Winner: " + winner + " 🎉");
    }

    document.getElementById("status").innerText = "";
});

// ------------------ MOVE ------------------

function makeMove(index) {
    if (!room) {
        alert("Join a room first");
        return;
    }

    if (player === "Viewer") {
        alert("You are a viewer");
        return;
    }

    socket.emit("move", {
        room: room,
        position: index,
        player: player
    });
}

// ================== CHAT SYSTEM ==================

function sendMessage() {
    const msg = document.getElementById("chatInput").value;

    if (!room) {
        alert("Join room first");
        return;
    }

    if (!msg.trim()) {
        return;
    }

    socket.emit("send_message", {
        room: room,
        message: msg
    });

    document.getElementById("chatInput").value = "";
}

socket.on("receive_message", (data) => {
    const chatBox = document.getElementById("chatBox");

    const msgDiv = document.createElement("div");
    msgDiv.innerText = data.user + ": " + data.message;

    chatBox.appendChild(msgDiv);

    // auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
});