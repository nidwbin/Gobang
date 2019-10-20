import os


class Constant:
    directions = ((1, 0), (0, 1), (1, 1), (1, -1), (-1, 0), (0, -1), (-1, -1), (-1, 1))
    score = (1, 10, 100, 1000, 0, 1, 10, 100)
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
    __max_min = [15, 15, -1, -1]
    __Neighbors = []

    def __init__(self, player, mode):
        self.__Player = player
        self.__Mode = mode
        for i in range(15):
            self.__Map.append([])
            for j in range(15):
                self.__Map[i].append(0)

    def __scan_map(self, max_min=None, the_map=None, start_point=(0, 0), direction=(1, 0)):
        if the_map is None:
            the_map = self.__Map
        if max_min is None:
            max_min = self.__max_min
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
                        if total >= 5:
                            return [-1, chess]
                        else:
                            if before is self.Blank:
                                if chess is self.BlackChess:
                                    score[0] += self.score[total + 3]
                                else:
                                    score[1] += self.score[total + 3]
                        total = 1
                        before = chess
                        chess = the_map[x][y]
            else:
                if chess is -2:
                    chess = self.Blank
                elif chess is not self.Blank:
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
                        score[0] += self.score[total + 3]
                    else:
                        score[1] += self.score[total + 3]
            else:
                if before is self.Blank:
                    if chess is self.BlackChess:
                        score[0] += self.score[total + 3]
                    else:
                        score[1] += self.score[total + 3]
        return score

    def __get_score(self, the_map=None, max_min=None):
        if the_map is None:
            the_map = self.__Map
        if max_min is None:
            max_min = self.__max_min
        score = [0, 0]
        inputs = []
        for i in range(max_min[1] + 1, max_min[3]):
            inputs.append([(max_min[0] + 1, i), self.directions[0]])
            inputs.append([(max_min[0] + 1, i), self.directions[2]])
            inputs.append([(max_min[0] + 1, i), self.directions[3]])
        for i in range(max_min[0] + 1, max_min[2]):
            inputs.append([(i, max_min[1] + 1), self.directions[1]])
            inputs.append([(i, max_min[1] + 1), self.directions[2]])
            inputs.append([(i, max_min[3] - 1), self.directions[3]])
        for i in inputs:
            tmp = self.__scan_map(the_map=the_map, start_point=i[0], direction=i[1])
            if tmp[0] is -1:
                return tmp
            else:
                score[0] += tmp[0]
                score[1] += tmp[1]
        return score

    def __get_neighbor_points(self, point=(0, 0), the_map=None, neighbor=None, deep=2):
        if neighbor is None:
            neighbor = self.__Neighbors
        if the_map is None:
            the_map = self.__Map
        for i in self.directions:
            for j in range(1, 1 + deep):
                x = point[0] + i[0] * j
                y = point[1] + i[1] * j
                if 0 <= x <= 14 and 0 <= y <= 14:
                    if the_map[x][y] is self.Blank:
                        if not (x, y, j) in neighbor:
                            neighbor.append((x, y, j))
                    else:
                        if (x, y, j) in neighbor:
                            neighbor.pop(neighbor.index((x, y, j)))
        neighbor.sort()
        return neighbor

    def __put_chess(self, the_map, neighbor, player, point, max_min):
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
        return the_map, neighbor, max_min

    def __get_chess(self, the_map, neighbor, max_min, player, alpha, beta, deep):
        total = -2
        point = [-2, -2]
        for i in neighbor:
            t_map, t_neighbor, t_max_min = self.__put_chess(the_map == the_map, neighbor=neighbor, player=player,
                                                            point=(i[0], i[1]), max_min=max_min)
            if deep > 0:
                ans, point = self.__get_chess(the_map=t_map, neighbor=t_neighbor, max_min=t_max_min, player=not player,
                                              alpha=alpha, beta=beta, deep=deep - 1)
                if ans is -3:
                    alpha = point
                if ans is -4:
                    beta = point
            score = self.__get_score(the_map=t_map, max_min=t_max_min)
            if score[0] is -1:
                return score
            if player is True:
                score = score[1] - score[0]
                beta = max(beta, score)
                if score < alpha:
                    return -3, alpha
            else:
                score = score[0] - score[1]
                alpha = max(alpha, score)
                if score < beta:
                    return -4, beta
            if total < score:
                total = score
                point = (i[0], i[1])
        return total, point

    def put_chess(self, player=False, timeout=False, point=(-1, -1)):
        if self.__Turn is player:
            if not timeout:
                self.__Map, self.__Neighbors, self.__max_min = self.__put_chess(the_map=self.__Map,
                                                                                neighbor=self.__Neighbors,
                                                                                player=player, point=point,
                                                                                max_min=self.__max_min)
                self.__History.append(point)
                self.__Top += 1
            self.__Turn = not self.__Turn
            return True
        else:
            return False

    def get_chess(self, player):
        score = self.__get_score()
        if score[0] is -1:
            return score
        else:
            '''
            i = input()
            i = i.split(' ')
            x = int(i[0])
            y = int(i[1])
            self.put_chess(player=player, x=x, y=y)
            return [x, y]
            '''
            if player is False:
                score = score[0] - score[1]
            else:
                score = score[1] - score[0]
            point = []
            neighbor = self.__Neighbors.copy()
            the_map = self.__Map.copy()

            return point

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
