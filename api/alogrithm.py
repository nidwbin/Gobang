import os


class Constant:
    directions = ((1, 0), (0, 1), (1, 1), (1, -1))
    score = (1, 10, 100, 1000, 1, 10, 100)
    BlackChess = -1
    WhiteChess = 1
    Blank = 0


class Gobang(Constant):
    __Map = []
    __History = []
    __Top = 0
    __Turn = False
    __Player = False
    __Mode = -1
    __MAX_MIN = [15, 15, -1, -1]

    def __init__(self, player, mode):
        self.__Player = player
        self.__Mode = mode
        for i in range(15):
            self.__Map.append([])
            for j in range(15):
                self.__Map[i].append(0)

    def __scan_map(self, start_point=(0, 0), direction=(1, 0)):
        x = start_point[0]
        y = start_point[1]
        min_x = self.__MAX_MIN[0] + 1
        min_y = self.__MAX_MIN[1] + 1
        max_x = self.__MAX_MIN[2] - 1
        max_y = self.__MAX_MIN[3] - 1
        before = -2
        total = 0
        score = [0, 0]
        chess = self.Blank
        if x is not 0 and y is not 0:
            before = self.Blank
        while min_x <= x <= max_x and min_y <= y <= max_y:
            if self.__Map[x][y] is not self.Blank:
                if chess is self.Blank:
                    before = chess
                    chess = self.__Map[x][y]
                    total = 1
                else:
                    if self.__Map[x][y] is chess:
                        total += 1
                    else:
                        if total >= 5:
                            return [-1, chess]
                        else:
                            if before is self.Blank:
                                if chess is self.BlackChess:
                                    score[0] += self.score[total + 2]
                                else:
                                    score[1] += self.score[total + 2]
                        total = 1
                        before = chess
                        chess = self.__Map[x][y]
            else:
                if chess is not self.Blank:
                    if total >= 5:
                        return [-1, chess]
                    else:
                        if before is self.Blank:
                            if chess is self.BlackChess:
                                score[0] += self.score[total - 1]
                            else:
                                score[1] += self.score[total - 1]
                    total = 0
                    chess = self.Blank
            x += direction[0]
            y += direction[1]
        if total is not 0:
            if total >= 5:
                return [-1, chess]
            if x < 14 and y < 14:
                if before is self.Blank:
                    if chess is self.BlackChess:
                        score[0] += self.score[total - 1]
                    else:
                        score[1] += self.score[total - 1]
                else:
                    if chess is self.BlackChess:
                        score[0] += self.score[total + 2]
                    else:
                        score[1] += self.score[total + 2]
            else:
                if before is self.Blank:
                    if chess is self.BlackChess:
                        score[0] += self.score[total + 2]
                    else:
                        score[1] += self.score[total + 2]
        return score

    def __get_score(self):
        score = [0, 0]
        inputs = []
        for i in range(self.__MAX_MIN[1]+1,self.__MAX_MIN[3]):
            inputs.append([(self.__MAX_MIN[0] + 1, i), self.directions[0]])
            inputs.append([(self.__MAX_MIN[0] + 1, i), self.directions[2]])
            inputs.append([(self.__MAX_MIN[0] + 1, i), self.directions[3]])
        for i in range(self.__MAX_MIN[0]+1, self.__MAX_MIN[2]):
            inputs.append([(i, self.__MAX_MIN[1] + 1), self.directions[1]])
            inputs.append([(i, self.__MAX_MIN[1] + 1), self.directions[2]])
            inputs.append([(i, self.__MAX_MIN[3] - 1), self.directions[3]])
        for i in inputs:
            tmp = self.__scan_map(i[0], i[1])
            if tmp[0] is -1:
                return tmp
            else:
                score[0] += tmp[0]
                score[1] += tmp[1]
        return score

    def put_chess(self, player=False, timeout=False, x=-1, y=-1):
        if self.__Turn is player:
            if not timeout:
                if player:
                    self.__Map[x][y] = self.WhiteChess
                else:
                    self.__Map[x][y] = self.BlackChess
                self.__History.append([x, y])
                self.__Top += 1
                if x <= self.__MAX_MIN[0]:
                    self.__MAX_MIN[0] = x - 1
                if y <= self.__MAX_MIN[1]:
                    self.__MAX_MIN[1] = y - 1
                if x >= self.__MAX_MIN[2]:
                    self.__MAX_MIN[2] = x + 1
                if y >= self.__MAX_MIN[3]:
                    self.__MAX_MIN[3] = y + 1
            self.__Turn = not self.__Turn
            return True
        else:
            return False

    def get_chess(self, player):
        score = self.__get_score()
        i = input()
        i = i.split(' ')
        x = int(i[0])
        y = int(i[1])
        self.put_chess(player=player, x=x, y=y)
        return [x, y]

    def save(self, path, name):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            if os.path.exists(path + name):
                return False
            else:
                file = open(path + name, 'w')
                file.writelines(str(self.__Map) + '\n')
                file.writelines(str(self.__History) + '\n')
                file.writelines(str(self.__MAX_MIN))
                file.writelines(str(self.__Top) + ' ' + str(self.__Turn) + ' ' + str(self.__Player) + ' ' + str(
                    self.__Mode) + '\n')
                return True
