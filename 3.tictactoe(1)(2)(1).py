import math
import random
from collections import defaultdict

size = 4

# 方形组成四点的可能性
box_shape_groups = []

# 直线组成四格的可能性（横4个，竖4个，斜2个，原本 straight_line_groups 应该也是要根据落子动态加载的）
straight_line_groups = [
    ('00', '10', '20', '30'),
    ('01', '11', '21', '31'),
    ('02', '12', '22', '32'),
    ('03', '13', '23', '33'),
    ('00', '11', '22', '33'),
    ('00', '01', '02', '03'),
    ('10', '11', '12', '13'),
    ('20', '21', '22', '23'),
    ('30', '31', '32', '33'),
    ('30', '21', '12', '03')
]

# 我的历史下子坐标
my_points = []

# 机器人历史下子坐标
robot_points = []

# 4*4中间四个点是组成四个点涉及组合最多的点，占7组，其他点每个点4组，所以这四点优先级比较高
priority_points = ['11', '21', '12', '22']

points_set = [str(i)+str(j) for i in range(4) for j in range(4)]


def move():
    # 我不能让对面赢
    # 在现有的能连成四点的所有可能的组合里, 根据历史所有机器人坐标点，筛选出还剩2个子就连成了的组合。
    # 对遍历出的2个子的坐标统计，有唯一最大的坐标就返回，这类是比较危机的坐标，优先级比较高。
    # 如果min_remain_points有两组以上坐标点数>2的 其实也就是拦不住了
    min_remain_group_maps = defaultdict(int)
    min_remain_points = []
    for i in box_shape_groups + straight_line_groups:
        cnt = 0
        for j in robot_points:
            if j in i:
                cnt += 1

        if cnt >= 2:
            for n in set(i) - set(robot_points):
                min_remain_group_maps[n] += 1

        # 如果有只剩一个子就连成的组合，优先返回，这是最危机的坐标，优先级最高
        if cnt >= 3:
            a = set(i) - set(robot_points)
            return a.pop()

    if min_remain_group_maps:
        min_remain_group_count = sorted(min_remain_group_maps.items(), key=lambda item: item[1], reverse=True)
        max_remain_count = max([i[1] for i in min_remain_group_count if i[0] not in my_points + robot_points])
        min_remain_points = [i[0] for i in min_remain_group_count if i[0] not in my_points + robot_points and i[1] >= max_remain_count]

    if len(min_remain_points) == 1:
        return min_remain_points[0]

    # 我不想对面赢
    # 在现有的能连成四点的所有可能的组合里，出现在组合里最多次数的未被落子坐标点
    point_win_group_count_maps = defaultdict(int)
    for i in box_shape_groups + straight_line_groups:
        for n in i:
            point_win_group_count_maps[n] += 1

    # 1 根据出现的次数倒序排列一下
    point_win_group_count = sorted(point_win_group_count_maps.items(), key=lambda item: item[1], reverse=True)
    # print("point_win_group_count: ",point_win_group_count)
    # 2 取出次数的最大值
    max_group_count = max([i[1] for i in point_win_group_count if i[0] not in my_points + robot_points] + [-1])
    # print("max_group_count: ",max_group_count)
    # 3 取出次数最大值对应的坐标点，可能有多个
    max_win_points = [i[0] for i in point_win_group_count if i[0] not in my_points + robot_points and i[1] >= max_group_count] + [-1]
    # print("max_win_points: ",max_win_points)
    #: 上面三步只是为了取最大次数的坐标点组

    # 如果有多个坐标点比重一样就选上面说的优先级比较高的坐标点
    for i in max_win_points:
        if i in priority_points:
            return i

    remain_point_set = set(points_set) - set(my_points) - set(robot_points)
    # print("remain_point_set: ",remain_point_set)
    # print("max_win_points[0]:",max_win_points[0] if max_win_points[0] != -1 else remain_point_set.pop())
    return max_win_points[0] if max_win_points[0] != -1 else remain_point_set.pop()


def rm_group(point):
    """
    删除不可能再出现的组合， 因为被我的子占了
    :param point:
    :return:
    """
    global straight_line_groups, box_shape_groups
    straight_line_groups = [i for i in straight_line_groups if point not in i]
    box_shape_groups = [i for i in box_shape_groups if point not in i]


def myTicTacToe(grille, monSymbole, pcx, pcy):

    robot_x_input = pcy
    robot_y_input = pcx
    robot_input_point = str(robot_x_input) + str(robot_y_input)

    # 验证下输入数字是否 0-3 且不再历史输入数字内
    if -1 < robot_x_input < 4 and -1 < robot_y_input < 4 \
            and robot_input_point not in my_points + robot_points:
        print('机器人输入有效，下子坐标为：', robot_input_point)
        robot_points.append(robot_input_point)

    # 和本次对手下的子相关的方形四点组合可能性
    if 0 < robot_x_input < 4 and 0 < robot_y_input < 4:
        if str(robot_x_input - 1) + str(robot_y_input - 1) not in my_points \
                and str(robot_x_input) + str(robot_y_input - 1) not in my_points \
                and str(robot_x_input - 1) + str(robot_y_input) not in my_points:
            box_shape_groups.append(
                (
                    str(robot_x_input - 1) + str(robot_y_input - 1),
                    str(robot_x_input) + str(robot_y_input - 1),
                    str(robot_x_input - 1) + str(robot_y_input),
                    str(robot_x_input) + str(robot_y_input)
                )
            )

    if -1 < robot_x_input < 3 and -1 < robot_y_input < 3:
        if str(robot_x_input + 1) + str(robot_y_input + 1) not in my_points \
                and str(robot_x_input) + str(robot_y_input + 1) not in my_points \
                and str(robot_x_input + 1) + str(robot_y_input) not in my_points:
            box_shape_groups.append(
                (
                    str(robot_x_input + 1) + str(robot_y_input + 1),
                    str(robot_x_input) + str(robot_y_input + 1),
                    str(robot_x_input + 1) + str(robot_y_input),
                    str(robot_x_input) + str(robot_y_input)
                )
            )

    if -1 < robot_x_input < 3 and 0 < robot_y_input < 4:
        if str(robot_x_input + 1) + str(robot_y_input) not in my_points \
                and str(robot_x_input) + str(robot_y_input - 1) not in my_points \
                and str(robot_x_input + 1) + str(robot_y_input - 1) not in my_points:
            box_shape_groups.append(
                (
                    str(robot_x_input + 1) + str(robot_y_input),
                    str(robot_x_input + 1) + str(robot_y_input - 1),
                    str(robot_x_input) + str(robot_y_input - 1),
                    str(robot_x_input) + str(robot_y_input)
                )
            )

    if 0 < robot_x_input < 4 and -1 < robot_y_input < 3:
        if str(robot_x_input - 1) + str(robot_y_input) not in my_points \
                and str(robot_x_input) + str(robot_y_input + 1) not in my_points \
                and str(robot_x_input - 1) + str(robot_y_input + 1) not in my_points:
            box_shape_groups.append(
                (
                    str(robot_x_input - 1) + str(robot_y_input),
                    str(robot_x_input) + str(robot_y_input + 1),
                    str(robot_x_input - 1) + str(robot_y_input + 1),
                    str(robot_x_input) + str(robot_y_input)
                )
            )

    my_input_point = move()
    my_points.append(my_input_point)
    rm_group(my_input_point)

    return (int(my_input_point[1]), int(my_input_point[0]))




def check(tab):
    sum = 0
    motif = 0

    global finished
    finished = False
    global winner
    winner = -1

    # check lines
    for i in range(0, 4):
        sum = 0
        for j in range(0, 4):
            sum = sum + tab[i][j]
        # print("lines" + str(sum))
        if math.fabs(sum) == 4:
            motif = sum

    # check columns
    for i in range(0, 4):
        sum = 0
        for j in range(0, 4):
            sum = sum + tab[j][i]
        # print("columns" + str(sum))
        if math.fabs(sum) == 4:
            motif = sum

    # check diags
    sum = 0
    for j in range(0, 4):
        sum = sum + tab[j][j]
    if math.fabs(sum) == 4:
        motif = sum

    sum = 0
    for j in range(0, 4):
        sum = sum + tab[j][3 - j]
    if math.fabs(sum) == 4:
        motif = sum

    # check squares
    for i in range(0, 3):
        for j in range(0, 3):
            sum = tab[i][j] + tab[i + 1][j] + tab[i][j + 1] + tab[i + 1][j + 1]
            if math.fabs(sum) == 4:
                motif = sum

    if motif == 4:
        finished = True
        winner = 1
    elif motif == -4:
        finished = True
        winner = -1
    else:
        finished = True
        winner = 0
        for i in range(0, 4):
            if tab[i][j] == 0:
                finished = False

    print(str(winner) + " " + str(finished))
    return (winner, finished)


def tictactoeRandom(grille, monSymbole):
    x = random.randint(0, (size - 1))
    y = random.randint(0, (size - 1))

    # print(grille[x][y])

    while grille[x][y] == monSymbole or (grille[x][y] + monSymbole) == 0:
        x = random.randint(0, (size - 1))
        y = random.randint(0, (size - 1))

    return (x, y)


def affecterSymbole(grille, monSymbole, x, y):
    # print(grille)
    # print(x, y)
    grille[x][y] = monSymbole
    # print(grille)


def affichage(grille):
    for i in range(0, size):
        ch = ""
        for j in range(0, size):
            ch += str(grille[i][j]) + " "
        print(ch)
    print()


grille = [0] * size

for i in range(size):

    grille[i] = [0] * size



winner = 0
finished = False

while winner == 0 or finished is False:
    monSymbole = -1
    (pcx, pcy) = tictactoeRandom(grille, monSymbole)

    affecterSymbole(grille, monSymbole, pcx, pcy)

    print("Dummy player")
    affichage(grille)
    (winner, finished) = check(grille)

    if winner == 0 or finished is False:
        monSymbole = 1
        (x, y) = myTicTacToe(grille, monSymbole, pcx, pcy)
        affecterSymbole(grille, monSymbole, x, y)
        (winner, finished) = check(grille)

        print("Student player")
        affichage(grille)
