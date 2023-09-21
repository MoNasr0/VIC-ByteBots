# if  flag again and no new dir: go back
# back remapping til you find new path
# adding encoders to improve move among cells and adding them in path
import time


# m1, m2 ==> left motor, right motor
def stopwatch(sec):
    st = time.time()
    elapsed = 0
    while elapsed <= sec:
        elapsed = time.time() - st
        time.sleep(1)


def stop(m1, m2):
    m1, m2 = 0, 0
    return m1, m2


def right(angle):
    angle = (abs(angle - 90) + 360) % 360
    m1, m2 = 1, 0
    # time.sleep(1)  # in sec
    return m1, m2


def left(angle):
    angle = (angle + 90) % 360
    m1, m2 = 0, 1
    # time.sleep(1)  # in sec
    return m1, m2


def forward():
    m1, m2 = 1, 1
    # time.sleep(5)  # in sec
    return m1, m2


def back():
    right(angle)
    right(angle)
    return 0

global r, c
def mapping_maze(r, c):
    if not angle and motor1 and motor2:
        c += 1
    elif angle == 180 and motor1 and motor2:
        c -= 1
    elif angle == 90 and motor1 and motor2:
        r += 1
    elif angle == 270 and motor1 and motor2:
        r -= 1
    if [r, c] not in mapping: mapping.append([r, c])
    return r, c


# s1, s2, s3 ==> left_ultrasonic, middle_ultrasonic, right_ultrasonic
def short(s1, s2, s3):
    if s1 and not (s2 + s3):
        left(angle)
        forward()
        mapping_maze(r, c)
    elif s2 and not (s1 + s3):
        forward()
        mapping_maze(r, c)
    elif s3 and not (s1 + s2):
        right(angle)
        forward()
        mapping_maze(r, c)
    elif s1 and s2 and not s3:
        forward()
        mapping_maze(r, c)
    elif s1 and s3 and not s2:
        right(angle)
        mapping_maze(r, c)
    elif s2 and s3 and not s1:
        forward()
        mapping_maze(r, c)
    elif s1 and s2 and s3:
        forward()
    else:
        back()
        forward()
        mapping_maze(r, c)


def find(mapping):
    for el in mapping:
        if el in dic:
            dic[el] += 1
        else:
            dic[el] = 1
    p = 0
    for el in mapping:
        p += 1
        if dic[el] == 2:
            ind_1 = mapping.index(el)
            mapping.remove(mapping[ind_1:p])
    print("find", mapping)


if __name__ == '__main__':
    motor1, motor2 = 0, 0
    start = 0, 0
    end = [[7, 7], [7, 8], [8, 7], [8, 8]]
    mapping = [[start[0], start[1]]]
    shortest = [(0, 0)]
    dic = {}
    # angle = 90  # by default
    sign = 0  # sign at end point
    while 1:
        r, c = mapping[-1]
        s1, s2, s3, angle = map(int, input().split())
        short(s1, s2, s3)
        # time.sleep(1)
        if mapping[-1] in end:
            stop(motor1, motor2)
            break
        print(mapping)
    print(find(mapping))
"""
0 1 0 90
0 0 1 0
1 0 0 90
0 0 1 0
1 1 0 0
1 0 0 90
1 0 0 180
1 0 0 270
0 1 0 270
0 1 0 270
0 1 0 270
0 1 0 270
0 1 0 270
0 1 0 270
0 1 0 270
"""
