addr = '127.0.0.1'
port = 11573

size_of_float = 4

# 可信度阈值
min_detection_confidence = 0.75
min_tracking_confidence = 0.75

num_params = 42

# 指定单人id
faceId = 0
# 关键点数目
nPoints = 68
# udp包大小
packetFrameSize = 8 + 4 + 2 * 4 + 2 * 4 + 1 + 4 + 3 * 4 + 3 * 4 + 4 * 4 + 4 * 68\
                  + 4 * 2 * 68 + 4 * 3 * 70 + 4 * 14
# 关键点坐标在udp包中的起始位置
landmarksOffset = 8 + 4 + 2 * 4 + 2 * 4 + 1 + 4 + 3 * 4 + 3 * 4 + 4 * 4 + 4 * 68

# 是否支持眨眼
enable_winking = 1

# 嘴部阈值
mouthNormalThreshold = 0.75
mouthSmileThreshold = 0.9
mouthClosedThreshold = 0.1
mouthOpenThreshold = 0.45
mouthOpenLaughCorrection = 0.2

# 面部阈值
faceYAngleXRotCorrection = 0.15
faceYAngleZeroValue = 1.8
faceYAngleDownThreshold = 2.3
faceYAngleUpThreshold = 1.6

# 眼部阈值
eyeClosedThreshold = 0.18
eyeOpenThreshold = 0.21

# 不同参数缓存的帧数
# faceXAngleNumTaps = 7
# faceYAngleNumTaps = 7
# faceZAngleNumTaps = 7
# mouthFormNumTaps = 3
# mouthOpenNumTaps = 3
# leftEyeOpenNumTaps = 3
# rightEyeOpenNumTaps = 3
