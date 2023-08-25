import time
# import ReadData
# s1, s2, s3 ==> left, mid, right
# m1, m2 ==> left motor, right motor

def stopwatch(sec):
    st = time.time()
    elapsed = 0
    while elapsed <= sec:
        elapsed = time.time() - st
        time.sleep(1)


def stop():
    m1, m2 = 0, 0
    return m1, m2


def right(ang):
    ang = (abs(ang - 90) + 360) % 360
    m1, m2 = 1, 0
    # time.sleep(1)  # in sec
    return m1, m2


def left(ang):
    ang = (ang + 90) % 360
    m1, m2 = 0, 1
    # time.sleep(1)  # in sec
    return m1, m2


def forward():
    m1, m2 = 1, 1
    # time.sleep(5)  # in sec
    return m1, m2


def back():
    right(ang); right(ang)
    return 0


def mapping_maze(r, c):
    # print(ang, "ang")
    if not ang: c += 1
    elif ang == 180: c -= 1
    elif ang == 90: r += 1
    elif ang == 270: r -= 1
    if [r, c] in mapping and [r, c] in flag \
            or [r, c] not in mapping: mapping.append([r, c])
    return r, c


def short(s1, s2, s3):
    if s1 and not (s2 + s3): left(ang); forward(); mapping_maze(r, c)
    elif s2 and not (s1 + s3): forward(); mapping_maze(r, c)
    elif s3 and not (s1 + s2): right(ang); forward(); mapping_maze(r, c)
    elif s1 and s2 and not s3: flag.append([r, c]); forward(); mapping_maze(r, c)
    elif s1 and s3 and not s2: flag.append([r, c]); forward(); mapping_maze(r, c)
    elif s2 and s3 and not s1: flag.append([r, c]); forward(); mapping_maze(r, c)
    elif s1 and s2 and s3: flag.append([r, c]); forward(); short(s1, s2, s3)
    else: back(); forward(); mapping_maze(r, c)



if __name__ == '__main__':
    m1, m2 = 0, 0
    flag = []
    start = 1, 1
    end = [2, 3]
    mapping = [[start[0], start[1]]]
    shortest = [(1, 1)]
    # ang = 90  # by default
    sign = 0  # sign at end point
    # s1, s2, s3 = ReadData.message
    while 1:
        r, c = mapping[-1]
        s1, s2, s3, ang = map(int, input().split())
        short(s1, s2, s3)
        # time.sleep(1)
        if mapping[-1] == end: stop(); break
    print(mapping)

