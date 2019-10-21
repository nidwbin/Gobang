from channels.generic.websocket import WebsocketConsumer
from api import alogrithm


class index(WebsocketConsumer):
    mode = 0
    player = False
    history = []
    top = 0
    length = 0
    gobang = alogrithm.Gobang

    def connect(self):
        self.accept()

    def disconnect(self, code):
        self.mode = 0
        self.player = False
        self.history = []
        self.top = 0
        self.length = 0
        self.gobang.__init__()

    def receive(self, text_data=None, bytes_data=None):
        messages = text_data.split('-')
        if messages[0] == 'start':
            self.top = 0
            self.mode = int(messages[1])
            tmp = messages[2]
            if tmp == 'false':
                self.player = False
            else:
                self.player = True
            self.send('linked')
            self.gobang = alogrithm.Gobang(player=self.player, mode=self.mode)
            return
        if messages[0] == 'chess':
            x = int(messages[1])
            y = int(messages[2])
            tmp = self.gobang.put_chess(player=self.player, timeout=False, point=(x, y))
            if tmp is 0:
                tmp, point = self.gobang.get_chess(not self.player)
                if tmp is 0:
                    self.send('chess-' + str(point[0]) + '-' + str(point[1]))
                elif tmp is -1:
                    self.send('win-BlackChess')
                else:
                    self.send('win-WhiteChess')
            elif tmp is -1:
                self.send('win-BlackChess')
            else:
                self.send('win-WhiteChess')
        if messages[0] == 'timeout':
            self.gobang.put_chess(player=self.player, timeout=True)
            point = self.gobang.get_chess(not self.player)
            self.send('chess-' + str(point[0]) + '-' + str(point[1]))
