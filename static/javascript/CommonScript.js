let player, turn, lastId, Map, History, Top, Mode, webSocket;
let backTimer, times, timerNumber, timer;
timerNumber = $('#TimerNumber');
timer = $('#Timer');


function InitConstant() {
    player = false;
    turn = false;
    lastId = null;
    History = [];
    times = 30;
    Top = 0;
    Mode = -1;
    Map = [];
    for (let i = 0; i < 15; ++i) {
        Map.push([]);
        for (let j = 0; j < 15; ++j) {
            Map[i][j] = 0;
        }
    }
}

function drawChessBoard() {
    let ChessBoard = $('#ChessBoard');
    for (let i = 0; i < 15; ++i) {
        ChessBoard.append('<div id=row-' + i + ' class="ChessBoardRow"></div>');
    }
    for (let i = 0; i < 15; ++i) {
        let row = $('#row-' + i + '');
        if (i === 0) {
            row.append('<div id="0-0" class="TopLeft ChessBoardBase" onclick="putChess(this.id)"></div>');
            for (let j = 1; j < 14; ++j) {
                row.append('<div id="0-' + j + '" class="Top ChessBoardBase" onclick="putChess(this.id)"></div>');
            }
            row.append('<div id="0-14" class="TopRight ChessBoardBase"  onclick="putChess(this.id)"></div>');
            continue;
        }
        if (i === 14) {
            row.append('<div id="14-0" class="BottomLeft ChessBoardBase"  onclick="putChess(this.id)"></div>');
            for (let j = 1; j < 14; ++j) {
                row.append('<div id="14-' + j + '" class="Bottom ChessBoardBase"  onclick="putChess(this.id)"></div>');
            }
            row.append('<div id="14-14" class="BottomRight ChessBoardBase"  onclick="putChess(this.id)"></div>');
            continue;
        }
        row.append('<div id="' + i + '-0" class="Left ChessBoardBase"  onclick="putChess(this.id)"></div>');
        for (let j = 1; j < 14; ++j) {
            row.append('<div id="' + i + '-' + j + '" class="Cross ChessBoardBase"  onclick="putChess(this.id)"></div>');
        }
        row.append('<div id="' + i + '-14" class="Right ChessBoardBase"  onclick="putChess(this.id)"></div>');
    }
}

function putChess(id) {
    if (Mode === 0) {
        toastr['error']('错误，还未开始游戏，请先开始游戏');
        return;
    }
    if (turn !== player) {
        toastr['error']('错误，当前不是您的回合，请等待对方落子');
        return;
    }
    let address, classes, tId, x, y;
    address = $('#' + id);
    classes = address.attr('class');
    classes = classes.split('-');
    tId = id.split("-");
    x = Number(tId[0]);
    y = Number(tId[1]);
    if (Map[x][y] === 1) {
        toastr['warning']('您不能在此处落子，此处已有白棋');
        return;
    }
    if (Map[x][y] === -1) {
        toastr['warning']('您不能在此处落子，此处已有黑棋');
        return;
    }
    sendMessage('chess-' + id + '-' + player);
    drawChess(address, classes, id, x, y);

}

function getChess(id, x, y) {
    let address, classes;
    address = $('#' + id);
    classes = address.attr('class');
    classes = classes.split('-');
    drawChess(address, classes, id, x, y);
}

function drawChess(address, classes, id, x, y) {
    if (turn) {
        address.attr('class', 'WhiteChess-Checked-' + classes[0]);
        Map[x][y] = 1;
    } else {
        address.attr('class', 'BlackChess-Checked-' + classes[0]);
        Map[x][y] = -1;
    }
    turn = !turn;
    if (lastId !== null) {
        address = $('#' + lastId);
        classes = address.attr('class');
        classes = classes.split('-');
        address.attr('class', classes[0] + '-Unchecked-' + classes[2]);
    }
    lastId = id;
    History[Top++] = id;
    clearInterval(backTimer);
    Timer(30);
}

function setLayout() {
    let width, height;
    width = window.innerWidth;
    height = window.innerHeight;
    width = width < height ? width : height;
    if (width > 600) {
        $('head').append('<link rel="stylesheet" type="text/css" href="/static/stylesheet/LayoutForLarge.css">');
    }
}

function reset() {
    let ChessBoard = $('#ChessBoard');
    ChessBoard.html('');
    drawChessBoard();
    InitConstant();
    checkWebsocket();
    setButtons();
    webSocket.close();
}

function repent() {

}

function startPlay() {
    let chessSelect = $('#ChessSelect').val();
    player = chessSelect !== 'BlackChess';
    Mode = 1;
    setButtons();
    startWebSocket();
    Timer(30);
}

function setButtons() {
    let chessSelect, start, reset, repent, save, load;
    chessSelect = $('#ChessSelect');
    start = $('#start');
    reset = $('#reset');
    repent = $('#repent');
    save = $('#save');
    load = $('#load');
    switch (Mode) {
        case -1: {
            chessSelect.attr('disabled', true);
            start.attr('disabled', true);
            reset.attr('disabled', true);
            repent.attr('disabled', true);
            save.attr('disabled', true);
            load.attr('disabled', true);
            break;
        }
        case 0: {
            chessSelect.attr('disabled', false);
            start.attr('disabled', false);
            reset.attr('disabled', true);
            repent.attr('disabled', true);
            save.attr('disabled', true);
            load.attr('disabled', false);
            break;
        }
        case 1: {
            chessSelect.attr('disabled', true);
            start.attr('disabled', true);
            reset.attr('disabled', false);
            repent.attr('disabled', false);
            save.attr('disabled', false);
            load.attr('disabled', false);
            break;
        }
        case 2: {
            chessSelect.attr('disabled', true);
            start.attr('disabled', true);
            reset.attr('disabled', false);
            reset.innerText = '认输';
            repent.attr('disabled', true);
            save.attr('disabled', true);
            load.attr('disabled', true);
            break;
        }
    }
}

function sendMessage(message) {
    switch (webSocket.readyState) {
        case 0: {
            window.setTimeout(sendMessage, 100);
            break;
        }
        case 1: {
            webSocket.send(message);
            break;
        }
        case 2: {
            break;
        }
        case 3: {
            break;
        }
    }
}

function webSocketError(e) {

}

function webSocketMessage(message) {
    if (message.data === 'linked') {
        return true;
    } else {
        let data = message.data.split('-');
        if (data[0] === 'chess') {
            getChess(data[1] + '-' + data[2], data[1], data[2]);
        }
    }
}

function startWebSocket() {
    webSocket = new WebSocket('ws://' + window.location.host + window.location.pathname);
    webSocket.onmessage = webSocketMessage;
    webSocket.onerror = webSocketError;
    webSocket.onopen = function () {
        sendMessage('start-' + Mode + '-' + player);
    }
}

function checkWebsocket() {
    if ('WebSocket' in window) {
        Mode = 0;
    } else {
        toastr['error']('错误，您的浏览器不支持本页面');
    }
}

function Timer(Time) {
    times = Time;
    backTimer = setInterval(setTimer, 1000);
}

function setTimer() {
    console.log(times);
    if (times <= -1) {
        clearInterval(backTimer);
        TimeOut();
        return;
    }
    if (times <= 5) {
        timer.css('background', '#dc3545')
    } else {
        timer.css('background', '#7abaff')
    }
    if (turn) {
        timerNumber.attr('class', 'text-white');
    } else {
        timerNumber.attr('class', 'text-dark');
    }
    let number = times.toString();
    if (times < 10) {
        number = '0' + number;
    }
    timerNumber.html(number);
    times -= 1;
}

function TimeOut() {
    if (turn === player) {
        turn = !turn;
        sendMessage('timeout');
    } else {
        toastr['warning']('您的网络好像出现了问题');
    }
}