from math import sin, cos, asin, radians, fabs, atan, pi
from typing import List

import config
from utils import avg_p, dist_p, angle, Point


# 计算头部x方向的旋转角度
def x_angle(landmarks: List[Point]):
    y0 = avg_p([landmarks[5], landmarks[195], landmarks[197], landmarks[6]])
    y1 = avg_p(landmarks[72:75]+landmarks[302:305])
    left = avg_p([landmarks[234], landmarks[93], landmarks[132]])
    right = avg_p([landmarks[454], landmarks[323], landmarks[401]])

    opp = dist_p(right, y0)
    adj1 = dist_p(y0, y1)
    adj2 = dist_p(y1, right)
    ang = angle(opp, adj1, adj2)
    perp_right = adj2 * sin(ang)

    opp = dist_p(left, y0)
    adj2 = dist_p(y1, left)
    ang = angle(opp, adj1, adj2)
    perp_left = adj2 * sin(ang)

    x_rad = asin((perp_right - perp_left) / (perp_right + perp_left))
    x_ans = x_rad / (pi / 6)
    if x_ans < -1.0:
        x_ans = -1.0
    if x_ans > 1.0:
        x_ans = 1.0

    return -x_ans


# 计算头部y方向的旋转角度
def y_angle(landmarks: List[Point], x_ang):
    a = dist_p(landmarks[197], landmarks[205])
    b = dist_p(landmarks[197], landmarks[425])
    c = dist_p(landmarks[205], landmarks[425])
    ang = angle(c, a, b)
    corr_ang = ang * (1 + fabs(x_ang) * config.faceYAngleXRotCorrection)

    if corr_ang >= config.faceYAngleZeroValue:
        return -linear_scale(corr_ang,
                                  config.faceYAngleZeroValue,
                                  config.faceYAngleDownThreshold,
                                  False, False)
    else:
        return 1 - linear_scale(corr_ang,
                                 config.faceYAngleUpThreshold,
                                 config.faceYAngleZeroValue,
                                 False, False)


# 计算头部z方向的旋转角度
def z_angle(landmarks: List[Point]):
    eye1, eye2 = eye(landmarks)
    nose1 = landmarks[203]
    nose2 = landmarks[423]
    
    eye_y_diff = eye1.y - eye2.y
    eye_x_diff = eye1.x - eye2.x
    ang1 = atan(eye_y_diff / eye_x_diff)

    nose_y_diff = nose1.y - nose2.y
    nose_x_diff = nose1.x - nose2.x
    ang2 = atan(nose_y_diff / nose_x_diff)

    return (ang1 + ang2) / 2


# 计算嘴部开合状态
def mouth_open(landmarks: List[Point]):
    h_left = dist_p(landmarks[41], landmarks[271])
    h_mid = dist_p(landmarks[78], landmarks[30])
    h_right = dist_p(landmarks[179], landmarks[403])
    h_avg = (h_right + h_mid + h_left) / 3

    width = dist_p(landmarks[11], landmarks[16])

    normalized = h_avg / width
    return linear_scale(normalized,
                          config.mouthClosedThreshold,
                          config.mouthOpenThreshold,
                          True, False)


# 计算眼睛的开闭状态
def eye_open(landmarks: List[Point], left_right, y_ang):
    ratio = eye_ratio([landmarks[33], landmarks[160], landmarks[158],
                       landmarks[133], landmarks[153], landmarks[144]]
                      if left_right else
                      [landmarks[362], landmarks[385], landmarks[387],
                       landmarks[263], landmarks[373], landmarks[380]])

    corr_ratio = ratio / cos(radians(y_ang))

    return 1 - linear_scale(corr_ratio,
                            config.eyeClosedThreshold,
                            config.eyeOpenThreshold)


# 计算瞳孔的旋转情况
def iris_ang(landmarks: List[Point]):
    ref = (dist_p(landmarks[468], landmarks[471]) +
             dist_p(landmarks[473], landmarks[476]))

    eye1, eye2 = eye(landmarks)
    iris1 = avg_p(landmarks[468:473])
    iris2 = avg_p(landmarks[473:478])

    pos_x = ((iris1.x - eye1.x) + (iris2.x - eye2.x)) * 2
    # pos_y = ((iris1.y - eye1.y) + (iris2.y - eye2.y)) * 4

    return pos_x / ref


# 计算眼睛位置
def eye(landmarks: List[Point]):
    eye1 = avg_p([landmarks[33], landmarks[160], landmarks[158],
                  landmarks[133], landmarks[153], landmarks[144]])
    eye2 = avg_p([landmarks[362], landmarks[385], landmarks[387],
                  landmarks[263], landmarks[373], landmarks[380]])
    return eye1, eye2


# 计算眼睛的长宽比例
def eye_ratio(points: List[Point]):
    width = dist_p(points[0], points[3])
    h1 = dist_p(points[1], points[5])
    h2 = dist_p(points[2], points[4])

    return (h1 + h2) / (2 * width)


# 线性比例
def linear_scale(num, mi, ma, clip_mi=True, clip_ma=True):
    if num < mi and clip_mi:
        return 0.0
    if num > ma and clip_ma:
        return 1.0
    return (num - mi) / (ma - mi)
