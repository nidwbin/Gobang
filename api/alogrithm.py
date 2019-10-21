import os
import copy
import time


class Constant:
    directions = ((1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1))
    score = (1, 10, 100, 1000, 1000, 0, 1, 10, 100, 1000, 0, 0, 0, 0, 1000)
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

    def __init__(self, player=False, mode=-1):
        self.__Player = player
        self.__Mode = mode
        self.__Scores = [[0, 0] for _ in range(60)]
        self.__Map = [[0 for _ in range(15)] for _ in range(15)]
        self.__Neighbors = []
        self.__max_min = [15, 15, -1, -1]
        self.__Turn = False
        self.__History = []
        self.__Top = 0

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
        if x < max_min[0]:
            max_min[0] = x - 1
        if y < max_min[1]:
            max_min[1] = y - 1
        if x > max_min[2]:
            max_min[2] = x + 1
        if y > max_min[3]:
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

    def is_win(self, point, max_min, the_map):
        points = self.__clu_start_point(point=point, max_min=max_min)
        for i in range(4):
            t = self.__is_win(max_min=max_min, the_map=the_map, start_point=points[i],
                              direction=self.directions[i])
            if t is not self.Blank:
                return t
        return 0

    def __scan_map(self, max_min, the_map, start_point, direction):
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
            score = self.__scan_map(max_min=max_min, the_map=the_map, start_point=points[i],
                                    direction=self.directions[i])
            t = x + i * 15
            scores[t][0] += score[0]
            scores[t][1] += score[1]
        return scores

    @staticmethod
    def __get_total_score(scores):
        score = [0, 0]
        for i in scores:
            score[0] += i[0]
            score[1] += i[1]
        return score

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
                score = score[0] - score[1]
            else:
                score = score[1] - score[0]
            return score, (-1, -1)
        point = (-1, -1)
        for i in neighbor:
            t_the_map, t_neighbor, t_max_min, t_scores = self.__put_chess(the_map=copy.deepcopy(the_map),
                                                                          neighbor=copy.deepcopy(neighbor),
                                                                          player=player, point=(i[0], i[1]),
                                                                          max_min=copy.deepcopy(max_min),
                                                                          scores=copy.deepcopy(scores))
            score, point = self.__get_chess(the_map=t_the_map, neighbor=t_neighbor, scores=t_scores,
                                            player=not player, max_min=t_max_min, alpha=alpha,
                                            beta=beta, deep=deep - 1, point=(i[0], i[1]))
            if player is not self.__Player:
                if score > alpha:
                    alpha = score
                    point = (i[0], i[1])
                    if score > beta:
                        break
            else:
                if score < beta:
                    beta = score
                    point = (i[0], i[1])
                    if score < alpha:
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
                file.writelines(str(self.__max_min))
                file.writelines(str(self.__Top) + ' ' + str(self.__Turn) + ' ' + str(self.__Player) + ' ' + str(
                    self.__Mode) + '\n')
                return True
