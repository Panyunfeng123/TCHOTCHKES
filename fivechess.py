import copy
import math
import random

# 定义棋盘类
class Board:
    def __init__(self, size):
        self.size = size
        self.board = [['-' for i in range(size)] for j in range(size)]
        self.last_move = (-1, -1)
    
    # 落子函数
    def move(self, row, col, chess_type):
        if not self.is_valid_coordinate(row, col) or self.board[row][col] != '-':
            return False
        self.board[row][col] = chess_type
        self.last_move = (row, col)
        return True
    
    # 判断坐标是否合法
    def is_valid_coordinate(self, row, col):
        return row >= 0 and row < self.size and col >= 0 and col < self.size
    
    # 获取指定坐标处的棋子类型
    def get_chess_type(self, row, col):
        return self.board[row][col]
        
    # 打印棋盘
    def print_board(self):
        first_row = "   "
        for i in range(self.size):
            first_row += chr(ord('A') + i) + "  "
        print(first_row)
        for i in range(self.size):
            row_str = "{:2d}".format(i+1)
            for j in range(self.size):
                row_str += " " + self.board[i][j] + " "
            print(row_str)
    
    # 判断游戏是否结束
    def is_game_over(self):
        if self.get_winner() != '-':
            return True
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '-':
                    return False
        return True
    
    # 获取胜者
    def get_winner(self):
        x, y = self.last_move
        chess_type = self.board[x][y]
        if chess_type == '-':
            return '-'
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for row_step, col_step in directions:
            count = 1 + self._count_chess_in_direction(row_step, col_step, x, y, chess_type)
            count += self._count_chess_in_direction(-row_step, -col_step, x, y, chess_type)
            if count >= 5:
                return chess_type
        return '-'
    
    # 检查某个方向上可以相连的棋子数
    def _count_chess_in_direction(self, row_step, col_step, row, col, chess_type):
        count = 0
        for i in range(1, 5):
            new_row = row + i * row_step
            new_col = col + i * col_step
            if not self.is_valid_coordinate(new_row, new_col):
                break
            if self.get_chess_type(new_row, new_col) != chess_type:
                break
            count += 1
        return count

# 定义 AI 类
class AI:
    def __init__(self, chess_type, board):
        self.chess_type = chess_type
        self.board = board
        
    # 极大极小值算法
    def minimax(self, depth, alpha, beta, is_max_turn):
        if depth == 0 or self.board.is_game_over():
            return self._evaluation(), (-1, -1)
        best_move = (-1, -1)
        if is_max_turn:
            value = -math.inf
            for move in self._generate_moves():
                new_board = copy.deepcopy(self.board)
                new_board.move(move[0], move[1], self.chess_type)
                new_value, _ = self.minimax(depth-1, alpha, beta, not is_max_turn)
                if new_value > value:
                    value = new_value
                    best_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
        else:
            value = math.inf
            for move in self._generate_moves():
                new_board = copy.deepcopy(self.board)
                new_board.move(move[0], move[1], self._get_opponent_chess_type())
                new_value, _ = self.minimax(depth-1, alpha, beta, not is_max_turn)
                if new_value < value:
                    value = new_value
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break
        return value, best_move
    
    # 评估函数
    # 评估函数
    def _get_chess_type(self, row: int, col: int, row_step: int, col_step: int, chess_type: str) -> str:
        count = self.board._count_chess_in_direction(row_step, col_step, row, col, chess_type)
        if not self.board.is_valid_coordinate(row-row_step, col-col_step) or \
                not self.board.is_valid_coordinate(row+2*row_step, col+2*col_step) or \
                self.board.get_chess_type(row-row_step, col-col_step) != '-' or \
                self.board.get_chess_type(row+2*row_step, col+2*col_step) != '-':
            count -= 1
        if count == 4:
            return 'win_four'
        elif count == 3:
            if not self.board.is_valid_coordinate(row-row_step, col-col_step) or \
                    not self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) or \
                    self.board.get_chess_type(row-row_step, col-col_step) != '-' or \
                    self.board.get_chess_type(row+3*row_step, col+3*col_step) != '-':
                return 'sleep_three'
            else:
                return 'live_three'
        elif count == 2:
            if not self.board.is_valid_coordinate(row-row_step, col-col_step) or \
                    not self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) or \
                    self.board.get_chess_type(row-row_step, col-col_step) != '-' or \
                    self.board.get_chess_type(row+3*row_step, col+3*col_step) != '-':
                if not self.board.is_valid_coordinate(row-row_step, col-col_step) or \
                        not self.board.is_valid_coordinate(row+4*row_step, col+4*col_step) or \
                        self.board.get_chess_type(row-row_step, col-col_step) != '-' or \
                        self.board.get_chess_type(row+4*row_step, col+4*col_step) != '-':
                    return 'sleep_two'
                else:
                    return 'live_two'
            else:
                if not self.board.is_valid_coordinate(row+2*row_step, col+2*col_step) or \
                        not self.board.is_valid_coordinate(row+4*row_step, col+4*col_step) or \
                        self.board.get_chess_type(row+2*row_step, col+2*col_step) != '-' or \
                        self.board.get_chess_type(row+4*row_step, col+4*col_step) != '-':
                    return 'sleep_two'
                else:
                    return 'live_two'
        else:
            return 'others'


    def _evaluation(self):
        # part 1: initialization
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        # part 2: traverse the board and calculate the score
        for row in range(self.board.size):
            for col in range(self.board.size):
                chess_type = self.board.get_chess_type(row, col)
                if chess_type == '-':
                    continue
                for row_step, col_step in directions:
                    count = 1 + self.board._count_chess_in_direction(row_step, col_step, row, col, chess_type)
                    count += self.board._count_chess_in_direction(-row_step, -col_step, row, col, chess_type)

                    # part 3: calculate the score of different chess types
                    if count >= 5:
                        if chess_type == self.chess_type:
                            return math.inf
                        else:
                            return -math.inf
                    elif count == 4:  
                        if chess_type == self.chess_type:
                            score += 100000
                        else:
                            score -= 100000
                    elif count == 3:  
                        if chess_type == self.chess_type:
                            score += 1000
                            if self.board.is_valid_coordinate(row-row_step, col-col_step) and \
                                    self.board.is_valid_coordinate(row+2*row_step, col+2*col_step) and \
                                    self.board.get_chess_type(row-row_step, col-col_step) == '-' and \
                                    self.board.get_chess_type(row+2*row_step, col+2*col_step) == '-':
                                score += 3000
                            elif self.board.is_valid_coordinate(row+row_step, col+col_step) and \
                                    self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) and \
                                    self.board.get_chess_type(row+row_step, col+col_step) == '-' and \
                                    self.board.get_chess_type(row+3*row_step, col+3*col_step) == '-':
                                score += 3000
                        else:
                            score -= 1000
                            if self.board.is_valid_coordinate(row-row_step, col-col_step) and \
                                    not self.board.is_valid_coordinate(row+2*row_step, col+2*col_step) and \
                                    self.board.get_chess_type(row-row_step, col-col_step) == '-' or \
                                    self.board.get_chess_type(row+2*row_step, col+2*col_step) == self._get_opponent_chess_type():
                                score -= 2500
                            elif self.board.is_valid_coordinate(row+row_step, col+col_step) and \
                                    not self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) and \
                                    self.board.get_chess_type(row+row_step, col+col_step) == '-' or \
                                    self.board.get_chess_type(row+3*row_step, col+3*col_step) == self._get_opponent_chess_type():
                                score -= 2500

                    # part 4: calculate the score of live two and sleep two
                    elif count == 2:  
                        if chess_type == self.chess_type:
                            score += 100
                            if self.board.is_valid_coordinate(row-row_step, col-col_step) and \
                                    self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) and \
                                    self.board.get_chess_type(row-row_step, col-col_step) == '-' and \
                                    self.board.get_chess_type(row+3*row_step, col+3*col_step) == '-':
                                score += 400
                            elif self.board.is_valid_coordinate(row+2*row_step, col+2*col_step) and \
                                    self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) and \
                                    self.board.get_chess_type(row+2*row_step, col+2*col_step) == '-' and \
                                    self.board.get_chess_type(row+3*row_step, col+3*col_step) == '-':
                                score += 400
                        else:
                            score -= 100
                            if self.board.is_valid_coordinate(row-row_step, col-col_step) and \
                                    not self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) and \
                                    self.board.get_chess_type(row-row_step, col-col_step) == '-' or \
                                    self.board.get_chess_type(row+3*row_step, col+3*col_step) == self._get_opponent_chess_type():
                                score -= 250
                            elif self.board.is_valid_coordinate(row+2*row_step, col+2*col_step) and \
                                    not self.board.is_valid_coordinate(row+3*row_step, col+3*col_step) and \
                                    self.board.get_chess_type(row+2*row_step, col+2*col_step) == '-' or self.board.get_chess_type(row+3*row_step, col+3*col_step) == self._get_opponent_chess_type():
                                    score -= 250

                # part 5: calculate the score of sleep three
                            elif count == 1 and self._get_chess_type(row, col, row_step, col_step, chess_type) == 'sleep_three':
                                if chess_type == self.chess_type:
                                    score += 10
                                else:
                                    score -= 10

            return score
    
    # 获取分数
    def _get_score(self, count, chess_type):
        if count >= 3:
            if chess_type == self.chess_type:
                return 20
            else:
                return -20
        elif count == 2:
            if chess_type == self.chess_type:
                return 6
            else:
                return -6
        elif count == 1:
            if chess_type == self.chess_type:
                return 2
            else:
                return -2
        else:
            return 0
        
    # 获取对手的棋子类型
    def _get_opponent_chess_type(self):
        if self.chess_type == 'X':
            return 'O'
        else:
            return 'X'
    
    # 产生下一步可能的走法
    def _generate_moves(self):
        moves = []
        for i in range(self.board.size):
            for j in range(self.board.size):
                if self.board.get_chess_type(i, j) != '-':
                    for row in range(max(0, i-2), min(self.board.size, i+2)):
                        for col in range(max(0, j-2), min(self.board.size, j+2)):
                            if self.board.get_chess_type(row, col) == '-':
                                moves.append((row, col))
        if not moves:
            moves.append((self.board.size//2, self.board.size//2)) # 如果候选点为空，则将第一个落子点设置为棋盘中心点
        random.shuffle(moves)
        return moves

    
# 主程序
def main():
    size = 15
    depth = 5
    print("请先选择先后手：")
    while True:
        player_first = input("玩家先手请输入 H，AI 先手请输入 C：").upper()
        if player_first == 'H' or player_first == 'C':
            break
        else:
            print("输入有误，请重新输入！")
    board = Board(size)
    ai = AI('O', board)
    if player_first == 'C':
        ai_move = ai.minimax(depth, -math.inf, math.inf, True)[1]
        board.move(ai_move[0], ai_move[1], 'O')
        print("AI 已落子：", chr(ord('A')+ai_move[1]), ai_move[0]+1)
    while not board.is_game_over():
        board.print_board()
        while True:
            move_str = input("请输入您的落子坐标（例如 A1）：").upper()
            if len(move_str) != 2 or not move_str[0].isalpha() or not move_str[1].isdigit():
                print("坐标格式不正确，请重新输入！")
                continue
            col = ord(move_str[0]) - ord('A')
            row = int(move_str[1]) - 1
            if not board.is_valid_coordinate(row, col) or board.get_chess_type(row, col) != '-':
                print("该位置无法落子，请重新输入！")
                continue
            board.move(row, col, 'X')
            break
        if board.is_game_over():
            break
        ai_move = ai.minimax(depth, -math.inf, math.inf, True)[1]
        board.move(ai_move[0], ai_move[1], 'O')
        print("AI 已落子：", chr(ord('A')+ai_move[1]), ai_move[0]+1)
    board.print_board()
    winner = board.get_winner()
    if winner == 'X':
        print("恭喜您获胜！")
    elif winner == 'O':
        print("很遗憾，您输给了 AI。")
    else:
        print("游戏结束，平局。")

if __name__ == '__main__':
    main()
