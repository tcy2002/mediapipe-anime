import mediapipe as mp
import numpy as np
import cv2
import torch
import pyvirtualcam as pv
import os


from tha2.poser.modes import mode_20
from tha2.util import resize_PIL_image, \
    extract_PIL_image_from_filelike, \
    extract_pytorch_image_from_PIL_image, \
    convert_output_image_from_torch_to_numpy

from utils import Point
import calc
import config


class Translator:
    def __init__(self, poser, cuda):
        self.poser = poser
        self.cuda = cuda

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            False, 1, True,
            config.min_detection_confidence,
            config.min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

        pil_img = resize_PIL_image(extract_PIL_image_from_filelike('./data/illust/9e.png'))
        self.source_img = extract_pytorch_image_from_PIL_image(pil_img).to(self.cuda)

        self.cam = cv2.VideoCapture(0)
        self.webcam = pv.Camera(width=256, height=256, fps=20, device='VirtualCamera')
        self.install_webcam()

    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()
        print('tracking terminated')

    # 启动本机摄像头，读取图像
    def run(self):
        while self.cam.isOpened():
            try:
                success, img = self.cam.read()
                if not success:
                    print('Ignoring empty frame...')
                    continue

                landmarks = self.process_img(img)
                img = self.send_to_anime(landmarks)
                self.webcam.send(img)
                self.webcam.sleep_until_next_frame()

                cv2.getWindowProperty('anime', 0)

            except (KeyboardInterrupt, cv2.error):
                break

    # 翻译数据并发至amine
    def send_to_anime(self, landmarks):
        if len(landmarks) == 0:
            return

        params = [0.0 for i in range(config.num_params)]
        params[40] = calc.x_angle(landmarks)
        params[39] = calc.y_angle(landmarks, params[40])
        params[41] = calc.z_angle(landmarks)
        params[14] = calc.eye_open(landmarks, True, params[41])
        params[13] = calc.eye_open(landmarks, False, params[41])
        params[26] = calc.mouth_open(landmarks)
        params[38] = calc.iris_ang(landmarks)

        pose = torch.tensor(params, device=self.cuda)
        output_img = self.poser.pose(self.source_img, pose, 0)[0].detach().cpu()
        numpy_img = np.uint8(np.rint(convert_output_image_from_torch_to_numpy(output_img) * 255.0))[:, :, :3]
        # numpy_img = cv2.cvtColor(cv2.flip(numpy_img, 1), cv2.COLOR_BGR2RGB)

        cv2.imshow('anime', numpy_img)
        cv2.waitKey(1)

        return numpy_img

    # 解析面部数据点
    def process_img(self, img):
        landmarks = []
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        h, w, c = img.shape
        results = self.face_mesh.process(img)

        if results.multi_face_landmarks:
            total_landmarks = results.multi_face_landmarks[0]
            for idx, landmark in enumerate(total_landmarks.landmark):
                x, y = landmark.x * w, landmark.y * h
                # cv2.circle(img, (int(x), int(y)), 1, (0, 255, 255), -1)
                # cv2.putText(img, str(idx), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0, 255, 255), 1)
                landmarks.append(Point(x, y))

        # cv2.imshow('face', img)
        # cv2.waitKey(1)

        return landmarks

    # 创建/获取虚拟摄像头
    def install_webcam(self):
        webcam = self.get_webcam_id()
        if webcam == -1:
            cmd = '.\\vc\\Install.bat'
            os.system(cmd)
            webcam = self.get_webcam_id()

        if webcam == -1:
            raise RuntimeError('Fail to install webcam!')

    # 获取虚拟摄像头id
    def get_webcam_id(self):
        detector = '.\\vc\\ReadCameraInfo.exe'
        rs = os.popen(detector)
        a = rs.read()
        sa = a.split('\n')

        for line in sa:
            if len(line) >= 7:
                camera = line[7:].split(":")
                if camera[1] == 'VirtualCamera':
                    return camera[0]

        return -1


if __name__ == '__main__':
    cuda = torch.device('cuda')
    poser = mode_20.create_poser(cuda)

    translator = Translator(poser, cuda)
    translator.run()