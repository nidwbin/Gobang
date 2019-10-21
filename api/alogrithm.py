import os
import copy
import random


class Constant:
    directions = ((1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1))
    score = (1, 10, 1000, 10000, 100000, 0, 1, 100, 1000, 100000, 0, 0, 0, 0, 100000)
    BlackChess = -1
    WhiteChess = 1
    Blank = 0
    Inf = 0x3f3f3f3f


class Gobang(Constant):
    __Map = []
    __History = []
    __Top = 0
    __Turn = False
    __Player = False
    __Mode = -1
    __max_min = [15, 15, -1, -1]
    __Neighbors = []
    __Scores = []
    __rate = 1.5

    def __init__(self, player=False, mode=-1, rate=1.5):
        self.__Player = player
        self.__Mode = mode
        self.__Scores = [[0, 0] for _ in range(60)]
        self.__Map = [[0 for _ in range(15)] for _ in range(15)]
        self.__Neighbors = []
        self.__max_min = [15, 15, -1, -1]
        self.__Turn = False
        self.__History = []
        self.__Top = 0
        self.__rate = rate

    @staticmethod
    def __get_total_score(scores):
        score = [0, 0]
        for i in scores:
            score[0] += i[0]
            score[1] += i[1]
        return score

    def __get_neighbor_points(self, point=(0, 0), the_map=None, neighbor=None):
        if neighbor is None:
            neighbor = self.__Neighbors
        if the_map is None:
            the_map = self.__Map
        for i in self.directions:
            x = point[0] + i[0]
            y = point[1] + i[1]
            if 0 <= x <= 14 and 0 <= y <= 14:
                if the_map[x][y] is self.Blank:
                    if not (x, y) in neighbor:
                        neighbor.append((x, y))
                else:
                    if (x, y) in neighbor:
                        neighbor.pop(neighbor.index((x, y)))
        if point in neighbor:
            neighbor.pop(neighbor.index(point))
        return neighbor

    def __put_chess(self, the_map, neighbor, player, point, max_min, scores):
        x = point[0]
        y = point[1]
        if player:
            the_map[x][y] = self.WhiteChess
        else:
            the_map[x][y] = self.BlackChess
        if x <= max_min[0]:
            max_min[0] = x - 1
        if y <= max_min[1]:
            max_min[1] = y - 1
        if x >= max_min[2]:
            max_min[2] = x + 1
        if y >= max_min[3]:
            max_min[3] = y + 1
        if neighbor is not None:
            neighbor = self.__get_neighbor_points(point=point, the_map=the_map, neighbor=neighbor)
        scores = self.__get_scores(point=point, the_map=the_map, max_min=max_min, scores=scores)
        return the_map, neighbor, max_min, scores

    def __is_win(self, max_min, the_map, start_point, direction):
        x = start_point[0]
        y = start_point[1]
        min_x = max(max_min[0] + 1, 0)
        min_y = max(max_min[1] + 1, 0)
        max_x = min(max_min[2] - 1, 14)
        max_y = min(max_min[3] - 1, 14)
        total = 0
        chess = 0
        while min_x <= x <= max_x and min_y <= y <= max_y and total < 5:
            if the_map[x][y] is self.Blank:
                chess = 0
                total = 0
            else:
                if chess is 0:
                    chess = the_map[x][y]
                    total = 1
                else:
                    if the_map[x][y] is chess:
                        total += 1
                    else:
                        chess = the_map[x][y]
                        total = 1
            x += direction[0]
            y += direction[1]
        if total >= 5:
            return chess
        else:
            return 0

    def __scan_row(self, max_min, the_map, start_point, direction):
        x = start_point[0]
        y = start_point[1]
        min_x = max(max_min[0] + 1, 0)
        min_y = max(max_min[1] + 1, 0)
        max_x = min(max_min[2] - 1, 14)
        max_y = min(max_min[3] - 1, 14)
        before = -2
        total = 0
        score = [0, 0]
        chess = -2
        if x is not 0 and y is not 0:
            before = self.Blank
        while min_x <= x <= max_x and min_y <= y <= max_y:
            if the_map[x][y] is not self.Blank:
                if chess is -2:
                    chess = the_map[x][y]
                    total = 1
                elif chess is self.Blank:
                    before = chess
                    chess = the_map[x][y]
                    total = 1
                else:
                    if the_map[x][y] is chess:
                        total += 1
                    else:
                        if before is self.Blank:
                            if chess is self.BlackChess:
                                score[0] += self.score[total + 4]
                            else:
                                score[1] += self.score[total + 4]
                        else:
                            if chess is self.BlackChess:
                                score[0] += self.score[total + 9]
                            else:
                                score[1] += self.score[total + 9]
                        total = 1
                        before = chess
                        chess = the_map[x][y]
            else:
                if chess is -2:
                    chess = self.Blank
                elif chess is not self.Blank:
                    if before is self.Blank:
                        if chess is self.BlackChess:
                            score[0] += self.score[total - 1]
                        else:
                            score[1] += self.score[total - 1]
                    else:
                        if chess is self.BlackChess:
                            score[0] += self.score[total + 4]
                        else:
                            score[1] += self.score[total + 4]
                    total = 0
                    chess = self.Blank
            x += direction[0]
            y += direction[1]
        if total is not 0:
            if x < 14 and y < 14:
                if before is self.Blank:
                    if chess is self.BlackChess:
                        score[0] += self.score[total - 1]
                    else:
                        score[1] += self.score[total - 1]
                else:
                    if chess is self.BlackChess:
                        score[0] += self.score[total + 4]
                    else:
                        score[1] += self.score[total + 4]
            else:
                if before is self.Blank:
                    if chess is self.BlackChess:
                        score[0] += self.score[total + 4]
                    else:
                        score[1] += self.score[total + 4]
                else:
                    if chess is self.BlackChess:
                        score[0] += self.score[total + 9]
                    else:
                        score[1] += self.score[total + 9]
        return score

    def __get_scores(self, point, the_map, max_min, scores):
        x = point[0]
        points = self.__clu_start_point(point=point, max_min=max_min)
        for i in range(4):
            score = self.__scan_row(max_min=max_min, the_map=the_map, start_point=points[i],
                                    direction=self.directions[i])
            t = x + i * 15
            scores[t][0] += score[0]
            scores[t][1] += score[1]
        return scores

    def __clu_start_point(self, point, max_min):
        x = point[0]
        y = point[1]
        min_x = max(max_min[0] + 1, 0)
        min_y = max(max_min[1] + 1, 0)
        points = [(min_x, y), (x, min_y)]
        for i in range(2, 4):
            x = point[0]
            y = point[1]
            while max_min[0] < x < max_min[2] and max_min[1] < y < max_min[3]:
                x -= self.directions[i][0]
                y -= self.directions[i][1]
            points.append((x + self.directions[i][0], y + self.directions[i][1]))
        return points

    def __get_chess(self, the_map, neighbor, scores, player, max_min, alpha, beta, deep, point=None):
        t = self.Blank
        if point is not None:
            t = self.is_win(point=point, max_min=max_min, the_map=the_map)
        if deep <= 0 or t is not self.Blank:
            score = self.__get_total_score(scores=scores)
            if self.__Player is True:
                score = score[0] - int(score[1] * self.__rate)
            else:
                score = score[1] - int(score[0] * self.__rate)
            return score, (-1, -1)
        point = (-1, -1)
        for i in neighbor:
            t_the_map, t_neighbor, t_max_min, t_scores = self.__put_chess(the_map=copy.deepcopy(the_map),
                                                                          neighbor=copy.deepcopy(neighbor),
                                                                          player=player, point=(i[0], i[1]),
                                                                          max_min=copy.deepcopy(max_min),
                                                                          scores=copy.deepcopy(scores))
            score, t_point = self.__get_chess(the_map=t_the_map, neighbor=t_neighbor, scores=t_scores,
                                              player=not player, max_min=t_max_min, alpha=alpha,
                                              beta=beta, deep=deep - 1, point=(i[0], i[1]))
            if player is not self.__Player:
                if score > alpha:
                    alpha = score
                    point = (i[0], i[1])
                    if score >= beta:
                        break
            else:
                if score < beta:
                    beta = score
                    point = (i[0], i[1])
                    if score <= alpha:
                        break
        if player is not self.__Player:
            return alpha, point
        else:
            return beta, point

    def put_chess(self, player=False, timeout=False, point=(-1, -1)):
        if not timeout:
            self.__Map, self.__Neighbors, self.__max_min, self.__Scores = self.__put_chess(the_map=self.__Map,
                                                                                           neighbor=self.__Neighbors,
                                                                                           player=player,
                                                                                           point=point,
                                                                                           max_min=self.__max_min,
                                                                                           scores=self.__Scores)
            self.__History.append(point)
            self.__Top += 1
        self.__Turn = not self.__Turn
        return self.is_win(point=point, max_min=self.__max_min, the_map=self.__Map)

    def get_chess(self, player):
        score, point = self.__get_chess(the_map=self.__Map, neighbor=self.__Neighbors,
                                        scores=self.__Scores, player=player, max_min=self.__max_min, alpha=-self.Inf,
                                        beta=self.Inf, deep=3)
        return self.put_chess(player=player, timeout=False, point=point), point

    def is_win(self, point, max_min, the_map):
        points = self.__clu_start_point(point=point, max_min=max_min)
        for i in range(4):
            t = self.__is_win(max_min=max_min, the_map=the_map, start_point=points[i],
                              direction=self.directions[i])
            if t is not self.Blank:
                return t
        return 0

    def save_map(self, path, name):
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            file = open(path + name, 'w')
            file.write(str(self.__Top) + '\n')
            file.write(str(self.__Turn) + '\n')
            file.write(str(self.__Player) + '\n')
            file.write(str(self.__Mode) + '\n')
            file.write(str(self.__rate) + '\n')
            for i in self.__max_min:
                file.write(str(i) + ' ')
            file.write('\n')
            for i in range(self.__Top):
                file.write(str(self.__History[i][0]) + ',' + str(self.__History[i][1]))
                if i is not self.__Top - 1:
                    file.write(' ')
            file.write('\n')
            cnt = 0
            for i in self.__Map:
                for j in i:
                    file.write(str(j))
                    if cnt is not 224:
                        file.write(' ')
                    cnt += 1
            file.write('\n')
            l_s = len(self.__Scores)
            for i in self.__Scores:
                file.write(str(i[0]) + ',' + str(i[1]))
                l_s -= 1
                if l_s is not 0:
                    file.write(' ')
            file.write('\n')
            l_s = len(self.__Neighbors)
            for i in self.__Neighbors:
                file.write(str(i[0]) + ',' + str(i[1]))
                l_s -= 1
                if l_s is not 0:
                    file.write(' ')
            file.write('\n')
            file.close()
            return True
        except IOError as e:
            print(e)
            return False

    def repent(self):
        point = [0, 0]
        for i in range(2):
            self.__Top -= 1
            point[i] = self.__History[self.__Top]
            self.__History.pop(self.__Top)
            self.__Map[point[i][0]][point[i][1]] = 0
            self.__Scores = self.__get_scores(point=point[i], the_map=self.__Map, max_min=self.__max_min,
                                              scores=self.__Scores)
        return point

    def load_map(self, path, name):
        self.__init__()
        total = ''
        if not os.path.exists(path + name):
            return False, ''
        else:
            file = open(path + name, 'r')
            cnt = 0
            for i in file.readlines():
                i = i.split('\n')[0]
                if cnt is 0:
                    total += i + '-'
                    self.__Top = int(i)
                elif cnt is 1:
                    if i == 'False':
                        self.__Turn = False
                    else:
                        self.__Turn = True
                elif cnt is 2:
                    total += i + '-'
                    if i == 'False':
                        self.__Player = False
                    else:
                        self.__Player = True
                elif cnt is 3:
                    total += i + '-'
                    self.__Mode = int(i)
                elif cnt is 4:
                    self.__rate = float(i)
                elif cnt is 5:
                    i = i.split(' ')
                    for j in range(4):
                        self.__max_min[j] = int(i[j])
                elif cnt is 6:
                    total += i + '-'
                    i = i.split(' ')
                    for j in i:
                        if j == '':
                            continue
                        j = j.split(',')
                        self.__History.append((int(j[0]), int(j[1])))
                elif cnt is 7:
                    i = i.split(' ')
                    for j in range(15):
                        for k in range(15):
                            if i[k + 15 * j] == '':
                                continue
                            self.__Map[j][k] = int(i[k + 15 * j])
                elif cnt is 8:
                    i = i.split(' ')
                    for j in range(60):
                        k = i[j].split(',')
                        self.__Scores[j][0] = int(k[0])
                        self.__Scores[j][1] = int(k[1])
                elif cnt is 9:
                    i = i.split(' ')
                    for j in i:
                        if j == '':
                            continue
                        j = j.split(',')
                        self.__Neighbors.append((int(j[0]), int(j[1])))
                cnt += 1
            return True, total

    def first_hand(self, the_map=None):
        if the_map is None:
            the_map = self.__Map
        x = random.randint(5, 11)
        y = random.randint(5, 11)
        point = (x, y)
        the_map[x][y] = self.BlackChess
        return point
