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
        pass

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
            point = []
            if self.gobang.put_chess(self.player, False, x, y):
                point = self.gobang.get_chess(not self.player)
            self.send('chess-' + str(point[0]) + '-' + str(point[1]))
