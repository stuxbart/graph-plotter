from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer, Qt
import sys
import numpy as np
from settings import *


class Controller:
    def __init__(self):
        self.model = None
        self.view = None
        self.app = None
        self.opengl_widget_loop = None
        self.mouse_pos = (200, 200)

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view
        self.view.set_model(self.model)

    def init(self):
        if self.model and self.view:
            self.app = QApplication(sys.argv)
            self.view.init(self)
            self.model.init()
            self.init_refresh_opengl_widget_timer()
            sys.exit(self.app.exec_())

    def init_refresh_opengl_widget_timer(self):
        self.opengl_widget_loop = QTimer()
        self.opengl_widget_loop.timeout.connect(self.view.opengl_widget.update)
        self.opengl_widget_loop.start(1000/fps)

    def key_press_event(self, k):
        if k in ("1", "2", "4", "6", "8", "9"):
            if k == "4":
                # self.translate(0.0, 0.0, 0.0)
                self.model.set_rotation(np.pi / 2, 0.0, -np.pi / 2)

            elif k == "6":
                # self.translate(0.0, 0.0, 0.0)
                self.model.set_rotation(np.pi / 2, 0.0, np.pi / 2)

            elif k == "8":
                # self.translate(0.0, 0.0, 0.0)
                self.model.set_rotation(0.0, 0.0, 0.0)

            elif k == "2":
                # self.translate(0.0, 0.0, 0.0)
                self.model.set_rotation(-np.pi, 0.0, -np.pi)

            elif k == "1":
                # self.translate(0.0, 0.0, 0.0)
                self.model.set_rotation(np.pi / 2, 0.0, 0.0)

            elif k == "9":
                # self.translate(0.0, 0.0, 0.0)
                self.model.set_rotation(np.pi / 2, 0.0, np.pi)

    def wheel_rotate(self, event):
        modifiers = QApplication.keyboardModifiers()
        if Qt.ShiftModifier == modifiers:
            self.model.change_zoom(event.angleDelta().y() / 300)
        else:
            self.model.change_zoom(event.angleDelta().y() / 60)

    def mouse_move(self, event):
        last = event.localPos()
        x, y = self.mouse_pos[0] - last.x(), self.mouse_pos[1] - last.y()
        self.mouse_pos = (last.x(), last.y())
        x /= -1
        y /= -1
        modifiers = QApplication.keyboardModifiers()
        if event.buttons() == Qt.MiddleButton and Qt.ShiftModifier == modifiers:
            trans_x = (np.cos(self.model.rot_z_angle) * x + np.cos(self.model.rot_x_angle)
                       * np.sin(self.model.rot_z_angle) * y)\
                      * (0.00 + 0.005 * np.power(np.e, -self.model.zoom / 10))
            trans_y = (np.sin(self.model.rot_z_angle) * x - np.cos(self.model.rot_x_angle)
                       * np.cos(self.model.rot_z_angle) * y)\
                      * (0.00 + 0.005 * np.power(np.e, -self.model.zoom / 10))
            trans_z = -np.sin(self.model.rot_x_angle) * y / 120
            self.model.translate(trans_x, trans_y, trans_z)
            # self.translate = matrix44.create_from_translation(Vector3([self.trans_x, self.trans_y, self.trans_z]))
        elif event.buttons() == Qt.MiddleButton:
            # self.use_perspective = True
            # if self.show_3D:
            #     self.rot_x_angle -= y / 120
            # # self.rot_angle_y -= np.cos(x / 180 * np.pi) * np.sin(y / 180 * np.pi)
            # self.rot_z_angle -= x / 120
            self.model.rotate(-y / 120, 0.0, -x / 120)

    def set_mouse_pos(self, event):
        last = event.localPos()
        self.mouse_pos = (last.x(), last.y())
