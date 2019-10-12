function makeChessBoardLineStyle() {
    let head = $('head');
    let basePath = '/static/picture/style/normal/';
    let chessNames = ['BlackChess', 'WhiteChess'];
    let type = ['Unchecked', 'Checked'];
    let names = ['TopLeft', 'Top', 'TopRight', 'Left', 'Cross', 'Right', 'BottomLeft', 'Bottom', 'BottomRight'];
    head.append('<style id="ChessBoardBackgroundStyle"></style>');
    let style = $('#ChessBoardBackgroundStyle');
    style.html('');
    style.append('.ChessBoardBackground{background-image: url("' + basePath + 'ChessBoard/Background/ChessBoardBackground.png");}');
    head.append('<style id="ChessBoardLineStyle"></style>');
    style = $('#ChessBoardLineStyle');
    style.html('');
    for (let i = 0; i < 9; ++i) {
        style.append('.' + names[i] + '{background-image: url("' + basePath + 'ChessBoard/' + type[0] + '/' + names[i] + '.png");}');
        style.append('.' + names[i] + ':hover {background-image: url("' + basePath + 'ChessBoard/' + type[1] + '/' + names[i] + '.png");}');
    }
    for (let k = 0; k < 2; ++k) {
        for (let j = 0; j < 2; ++j) {
            for (let i = 0; i < 9; ++i) {
                style.append('.' + chessNames[j] + '-' + type[k] + '-' + names[i] + '{background-image: url("' + basePath + chessNames[j] + '/' + type[k] + '/' + names[i] + '.png");}');
            }
        }
    }
    for (let j = 0; j < 2; ++j) {
        for (let i = 0; i < 9; ++i) {
            style.append('.' + chessNames[j] + '-' + type[0] + '-' + names[i] + ':hover {background-image: url("' + basePath + chessNames[j] + '/' + type[1] + '/' + names[i] + '.png");}');
        }
    }
}
