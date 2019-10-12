let player, lastId, Map, History, Top, Mode;

function InitConstant(mode) {
    player = false;
    lastId = null;
    history = [];
    Top = 0;
    Mode = mode;
    Map = [];
    for (let i = 0; i < 15; ++i) {
        Map.push([]);
        for (let j = 0; j < 15; ++j) {
            Map[i][j] = 0;
        }
    }
}

function drawChessBoard(mode) {
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
    InitConstant(mode);
}

function putChess(id) {
    let address, classes, tId, x, y;
    address = $('#' + id);
    classes = address.attr('class');
    classes = classes.split('-');
    tId = id.split("-");
    x = Number(tId[0]);
    y = Number(tId[1]);
    if (Map[x][y] === 1) {
        return;
    }
    if (Map[x][y] === -1) {
        return;
    }
    if (player) {
        address.attr('class', 'WhiteChess-Checked-' + classes[0]);
        Map[x][y] = 1;
    } else {
        address.attr('class', 'BlackChess-Checked-' + classes[0]);
        Map[x][y] = -1;
    }
    player = !player;
    if (lastId !== null) {
        address = $('#' + lastId);
        classes = address.attr('class');
        classes = classes.split('-');
        address.attr('class', classes[0] + '-Unchecked-' + classes[2]);
    }
    lastId = id;
    History[Top++] = id;
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

function reset(mode) {

    InitConstant(mode);
}

function repent() {

}