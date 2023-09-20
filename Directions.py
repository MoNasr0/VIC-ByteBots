def global_orientation(from_C, now_C, ultra_reads):
    dic = {0: "U", 1: "R", 2: "L", 3: "D"}
    open_path = []
    direction = "U"

    # determine direction of robot
    x = now_C[0] - from_C[0]
    y = now_C[1] - from_C[1]
    if x == 1 and y == 0: direction = "R"
    elif x == -1 and y == 0: direction = "L"
    elif x == 0 and y == 1: direction = "U"
    elif x == 0 and y == -1: direction = "D"
    # return robot direction and available paths
    if direction == 'U':
        # available paths to go
        for ind in range(3):
            if ultra_reads[ind]: open_path.append(dic[ind])
        return direction, ''.join(open_path) + 'D'
    elif direction == 'R':
        #URL
        # U => R
        # R => D
        # L => U
        dic = {0: "R", 1: "D", 2: "U", 3: "L"}
        for ind in range(3):
            if ultra_reads[ind]: open_path.append(dic[ind])
        return direction, ''.join(open_path) + 'L'
    elif direction == 'L':
        #URL
        # U => L
        # R => U
        # L => D
        dic = {0: "L", 1: "U", 2: "D", 3: "R"}
        for ind in range(3):
            if ultra_reads[ind]: open_path.append(dic[ind])
        return direction, ''.join(open_path) + 'R'
    elif direction == 'D':
        #URL
        # U => D
        # R => L
        # L => R
        dic = {0: "D", 1: "L", 2: "R", 3: "U"}
        for ind in range(3):
            if ultra_reads[ind]: open_path.append(dic[ind])
        return direction, ''.join(open_path) + 'U'


def priority(inp, last, visited):
    if len(inp) == 1:
        return inp
    if 'U' in visited or last == 'D':
        inp = inp.replace('U', '')
    elif 'L' in visited or last == 'R':
        inp = inp.replace('L', '')
    elif 'R' in visited or last == 'L':
        inp = inp.replace('R', '')
    elif 'D' in visited or last == 'U':
        inp = inp.replace('D', '')

    # print(inp, visited, last)
    if len(inp) > 1 and len(visited) > 0:
        if 'U' in inp and 'U' != last:
            return 'U'
        elif 'R' in inp and 'R' != last:
            return 'R'
        elif 'L' in inp and 'L' != last:
            return 'L'
        elif 'D' in inp and 'D' != last:
            return 'D'

    if 'U' in inp:
        return 'U'
    elif 'R' in inp:
        return 'R'
    elif 'L' in inp:
        return 'L'
    elif 'D' in inp:
        return 'D'
    else:
        last

x, y = 4, 4

map = [['' for _ in range(x)] for _ in range(y)]

visited = [['' for _ in range(x)] for _ in range(y)]

pos = [0, 0]
surr = list(input())
for i in range(len(surr)):
    surr[i] = int(surr[i])
print(surr)
ultrasonics = [surr]

# ultrasonics = [[1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 0], [0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0], [0, 0, 1], [1, 0, 0], [0, 1, 1], [1,0, 0], [0, 0, 0]]
old_pos = [0, 0]

path = ''
paths = []
def dfs(ultrasonics):
    global map, path, old_pos, pos
    for ultrasonic in ultrasonics:
        print(path, pos)
        if pos in [[3, 3], [7, 8], [8, 7], [8, 8]]:  #
            print("maze solved")
            return path
        next = global_orientation(old_pos, pos, ultrasonic)
        old_pos = pos[::]
        if len(map[pos[0]][pos[1]]) > 0:
            chr = next[0]
            if chr == 'D':
                chr = 'U'
            elif chr == 'R':
                chr = 'L'
            elif chr == 'L':
                chr = 'R'
            elif chr == 'U':
                chr = 'D'
            map[pos[0]][pos[1]] = map[pos[0]][pos[1]].replace(chr, '')
        else:
            map[pos[0]][pos[1]] = next[1]
        n = priority(next[1], next[0], visited[pos[0]][pos[1]])
        path += n
        visited[old_pos[0]][old_pos[1]] += n
        if n == "U":
            pos[1] += 1
        elif n == "R":
            pos[0] += 1
        elif n == "L":
            pos[0] -= 1
        elif n == "D":
            pos[1] -= 1
        # print(path)
dfs(ultrasonics)
# print(*map)

for _ in range(len(path)):
    x = path
    for i in range(len(path)-1):
        x = x.replace("RL", "")
        x = x.replace("DU", "")
        x = x.replace("UD", "")
        x = x.replace("LR", "")
    path = x

reverse_path = ""
for i in path[::-1]:
    if i == "D":
        reverse_path += "U"
    if i == "L":
        reverse_path += "R"
    if i == "R":
        reverse_path += "L"
    if i == "U":
        reverse_path += "D"
print(path, reverse_path)
