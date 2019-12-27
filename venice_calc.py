#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtCore import QCoreApplication, Qt
from ui_loader import load_ui
import time

sensor_modes = {
    "6K 3:2": [6048, 4032, 690, 460],
    "6K 2.39:1": [6048, 2534, 690, 288],
    "6K 17:9": [6054, 3192, 690, 364],
    "6K 1.85:1": [6054, 3272, 690, 374],
    "6K 1.66:1": [6054, 3632, 690, 416],
    "5.7K 16:9": [5674, 3192, 690, 388],
    "4K 4:3": [4096, 3024, 613, 460],
    "4K 2.39:1": [4096, 1716, 690, 288],
    "4K 17:9": [4096, 2160, 690, 364],
    "3.8K 16:9": [3840, 2160, 690, 388]
}

user_max_w = 479
user_max_h = 269

class VeniceCalc(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        load_ui('venice_calc.ui', self)
        self.cbSensor.currentIndexChanged.connect(lambda: draw_sensor(self))
        self.cbSqueeze.currentIndexChanged.connect(lambda: draw_sensor(self))
        self.leScale.textEdited.connect(lambda: VeniceCalc.get_results(self))
        self.leUserRatioW.textEdited.connect(lambda: VeniceCalc.get_results(self))

        self.leUserRatioH.textEdited.connect(lambda: VeniceCalc.get_results(self))

    def get_results(self):
        time.sleep(.25)
        sensor = self.cbSensor.currentText()
        self.lSensorW.setText(str(sensor_modes[sensor][0]))
        self.lSensorH.setText(str(sensor_modes[sensor][1]))

        if self.leUserRatioW.text() == "" or self.leUserRatioH.text() == "":
            self.lFrameUser.hide()
        else:
            sensor_w = sensor_modes[sensor][0]
            sensor_h = sensor_modes[sensor][1]
            _scale = self.leScale.text()
            lens_factor = float(self.cbSqueeze.currentText())
            sensor_ratio = (sensor_w / sensor_h) / lens_factor
            user_ratio = (float(self.leUserRatioW.text()) / float(self.leUserRatioH.text())) / lens_factor
            user_frame_w = user_max_h * ((user_max_w / sensor_ratio) * (user_ratio / user_max_h))
            user_frame_h = user_max_w / ((user_ratio / sensor_ratio) * (user_max_w / user_max_h))
            user_pixels_w = sensor_h * user_ratio
            user_pixels_h = sensor_w / user_ratio
            print(lens_factor)
            if _scale in ("100", "100.0", ""):
                scale = 0
                print('100% scale')
            else:
                if int(self.leScale.text()) > 100:
                    self.leScale.setText("100")
                    scale = 0
                else:
                    scale = 100 - int(self.leScale.text())

            if user_ratio < sensor_ratio:  # fit height
                self.lUserWidth.setText(f"{round(user_frame_w - (user_frame_w * scale / 100))}")
                self.lUserHeight.setText(f"{round(user_max_h - (user_max_h * scale / 100))}")
                self.lUserPixelsW.setText(f"{round(user_pixels_w - (user_pixels_w * scale / 100))}")
                self.lUserPixelsH.setText(f"{round(sensor_h - (sensor_h * scale / 100))}")

            elif user_ratio > sensor_ratio:  # fit width
                self.lUserWidth.setText(f"{round(user_max_w - (user_max_w * scale / 100))}")
                self.lUserHeight.setText(f"{round(user_frame_h - (user_frame_h * scale / 100))}")
                self.lUserPixelsW.setText(f"{round(sensor_w - (sensor_w * scale / 100))}")
                self.lUserPixelsH.setText(f"{round(user_pixels_h - (user_pixels_h * scale / 100))}")

            elif user_ratio == sensor_ratio:
                self.lUserWidth.setText(f"{round(user_max_w - (user_max_w * scale / 100))}")
                self.lUserHeight.setText(f"{round(user_max_h - (user_max_h * scale / 100))}")
                self.lUserPixelsW.setText(f"{round(sensor_w - (sensor_w * scale / 100))}")
                self.lUserPixelsH.setText(f"{round(sensor_h - (sensor_h * scale / 100))}")
            draw_frame(self)


# def scale(self, value):
#     _scale = self.leScale.text()
#     if _scale == "" or _scale == "100.0" or _scale == "100":
#         scale = 0
#     else:
#         scale = 100 - int(self.leScale.text())
#     return int(value) - ((scale * int(value)) / 100)


def draw_sensor(self):
    _scale = self.leScale.text()

    if _scale in ("100", "100.0", ""):
        scale = 0
        print('100% scale')

    else:
        if int(self.leScale.text()) > 100:
            self.leScale.setText("100")
            scale = 0

        else:
            scale = 100 - int(self.leScale.text())

    sensor_index = self.cbSensor.currentIndex()
    sensor_text = self.cbSensor.currentText()
    draw_sensor_w = sensor_modes[sensor_text][2]
    draw_sensor_h = sensor_modes[sensor_text][3]

    if sensor_index == 0:  # 3:2
        self.lFrameSensor.resize(draw_sensor_w, draw_sensor_h)
        self.lFrameSensor.move(0, 0)

    elif sensor_index == 1 or sensor_index == 7:  # 2.39:1
        self.lFrameSensor.resize(draw_sensor_w, draw_sensor_h)
        self.lFrameSensor.move(0, 86)

    elif sensor_index == 2 or sensor_index == 8:  # 17:9
        self.lFrameSensor.resize(draw_sensor_w, draw_sensor_h)
        self.lFrameSensor.move(0, 48)

    elif sensor_index == 3:  # 1.85
        self.lFrameSensor.resize(draw_sensor_w, draw_sensor_h)
        self.lFrameSensor.move(0, 43)

    elif sensor_index == 4:  # 1.66
        self.lFrameSensor.resize(draw_sensor_w, draw_sensor_h)
        self.lFrameSensor.move(0, 22)

    elif sensor_index == 5 or sensor_index == 9:  # 1.78
        self.lFrameSensor.resize(draw_sensor_w, draw_sensor_h)
        self.lFrameSensor.move(0, 36)

    elif sensor_index == 6:  # 4:3
        self.lFrameSensor.resize(draw_sensor_w, draw_sensor_h)
        self.lFrameSensor.move(38, 0)
    VeniceCalc.get_results(self)


def draw_frame(self):
    _scale = self.leScale.text()
    if _scale in ("100", "100.0", ""):
        scale = 100
        print('100% scale')
    else:
        scale = 100 - int(self.leScale.text())

    sensor_ratio = int(self.lSensorW.text()) / int(self.lSensorH.text())
    user_ratio = float(self.leUserRatioW.text()) / float(self.leUserRatioH.text())
    self.lFrameUser.show()
    sensor_cb = self.cbSensor.currentText()
    _user_max_w = 479
    user_max_w = _user_max_w - ((scale * _user_max_w) / 100)
    _user_max_h = 269
    user_max_h = _user_max_h - ((scale * _user_max_h) / 100)
    draw_sensor_frame_w = sensor_modes[sensor_cb][2]
    draw_sensor_frame_h = sensor_modes[sensor_cb][3]
    new_w = round(draw_sensor_frame_h * user_ratio)
    new_h = round(draw_sensor_frame_w / user_ratio)
    new_x = (draw_sensor_frame_w - new_w) // 2
    new_y = (draw_sensor_frame_h - new_h) // 2
    max_x = round((user_max_w - (((100 - scale) * user_max_w) / 100) - draw_sensor_frame_w) // 2)
    max_y = round((user_max_h - (((100 - scale) * user_max_h) / 100) - draw_sensor_frame_h) // 2)
    # print(f"draw_sensor_frame_w{draw_sensor_frame_w}")
    # print(f"draw_sensor_frame_h{draw_sensor_frame_h}")
    # print(f"new_w{new_w}")
    # print(f"new_h{new_h}")
    # print(f"new_x{new_x}")
    # print(f"new_y{new_y}")
    # print(f"max_x{max_x}")
    # print(f"max_y{max_y}")

    if user_ratio == sensor_ratio:
        if sensor_cb == "6K 3:2":
            self.lFrameUser.resize(draw_sensor_frame_w, draw_sensor_frame_h)
            self.lFrameUser.move(0, 0)

        elif sensor_cb == "4K 4:3":
            self.lFrameUser.resize(draw_sensor_frame_w, draw_sensor_frame_h)
            self.lFrameUser.move(new_x, 0)

        else:
            self.lFrameUser.resize(draw_sensor_frame_w, new_h)
            self.lFrameUser.move(0, new_y)

    elif sensor_ratio < 1.5:  # 4:3 sensor
        if sensor_ratio == user_ratio:
            self.lFrameUser.resize(draw_sensor_frame_w, draw_sensor_frame_h)
            self.lFrameUser.move(max_x, 0)

        elif user_ratio > sensor_ratio:  # fit width
            self.lFrameUser.resize(draw_sensor_frame_w, new_h)
            self.lFrameUser.move(max_x, new_y)
            print(f"4:3 sensor {max_x}, {new_y}")

        elif user_ratio < sensor_ratio:  # fit height
            self.lFrameUser.resize(new_w, draw_sensor_frame_h)
            self.lFrameUser.move(max_x + new_x, 0)

    elif sensor_ratio > 1.5:  # wider than 3:2 sensor
        if sensor_ratio == user_ratio:
            self.lFrameUser.resize(draw_sensor_frame_w, draw_sensor_frame_h)
            self.lFrameUser.move(0, max_y)

        elif user_ratio > sensor_ratio:  # fit width
            self.lFrameUser.resize(draw_sensor_frame_w, new_h)
            self.lFrameUser.move(max_x, max_y + new_y)
            print("wider than 3:2, fit width", draw_sensor_frame_w, new_h, max_y + new_y)

        elif user_ratio < sensor_ratio:  # fit height
            self.lFrameUser.resize(new_w, draw_sensor_frame_h)
            self.lFrameUser.move(max_x + new_x, max_y)
            print("wider than 3:2, fit height")
            print(f"{max_x + new_x},{max_y}")

    elif sensor_ratio == 1.5:
        if user_ratio > sensor_ratio:  # fit width
            self.lFrameUser.resize(draw_sensor_frame_w, new_h)
            self.lFrameUser.move(0, new_y)

        elif user_ratio < sensor_ratio:  # fit height
            self.lFrameUser.resize(new_w, draw_sensor_frame_h)
            self.lFrameUser.move(new_x, 0)


if __name__ == '__main__':
    import sys

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    w = VeniceCalc()
    w.show()
    w.get_results()
    sys.exit(app.exec_())
