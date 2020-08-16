import random
from PySide2.QtWidgets import QMainWindow, QApplication, \
    QAction, QDockWidget, QPushButton, QHBoxLayout,\
    QWidget, QLineEdit, QVBoxLayout, QLabel, QFrame, \
    QSlider, QColorDialog, QScrollArea, QShortcut
from PySide2.QtCore import Slot, QSize, QRect
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtGui import Qt, QColor, QKeySequence
import numpy as np
from settings import *
from styles import *
from model import OpenGLController


class View:
    def __init__(self):
        self.model = None
        self.controller = None
        self.main_window = None
        self.opengl_widget = None
        self.functions_dock = None
        self.timeline_dock = None

    def set_model(self, model: OpenGLController):
        self.model = model
        self.model.set_view(self)

    def init(self, controller):
        self.controller = controller
        self.main_window = MainWindow()
        self.main_window.resize(*main_window_size)
        # ------------ Create Docks ---------------
        self.functions_dock = FunctionsMenuDock(self)
        self.timeline_dock = TimelineDock(self)
        self.main_window.addDockWidget(Qt.RightDockWidgetArea, self.functions_dock)
        self.main_window.addDockWidget(Qt.BottomDockWidgetArea, self.timeline_dock)
        # ----------- Main Widget ----------------
        self.opengl_widget = OpenGLWidget(self)
        self.main_window.set_opengl_widget(self.opengl_widget)

        self.main_window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle(APP_TITLE)
        # ------------- Menu ----------------
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.menu.setStyleSheet(menu_style)
        # --------------- Menu Actions ----------------
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)
        # -------------- Bind Menu Actions ------------
        self.file_menu.addAction(exit_action)
        # --------------- Background color ------------
        self.setAutoFillBackground(True)
        p = self.palette()
        c = QColor.fromRgb(*background_color)
        p.setColor(self.backgroundRole(), c)
        self.setPalette(p)
        # ------------- Main Widget ----------------
        self.widget = None
        # ---------------- Dock Widget -------------

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()

    def set_opengl_widget(self, widget):
        self.widget = widget
        self.setCentralWidget(widget)


class ShortcutsBindings:
    def __init__(self, parent):
        s1 = QShortcut(QKeySequence(Qt.Key_1), parent)
        s1.activated.connect(lambda: parent.keyPressEvent(k='1'))
        s2 = QShortcut(QKeySequence(Qt.Key_2), parent)
        s2.activated.connect(lambda: parent.keyPressEvent(k='2'))
        s4 = QShortcut(QKeySequence(Qt.Key_4), parent)
        s4.activated.connect(lambda: parent.keyPressEvent(k='4'))
        s6 = QShortcut(QKeySequence(Qt.Key_6), parent)
        s6.activated.connect(lambda: parent.keyPressEvent(k='6'))
        s8 = QShortcut(QKeySequence(Qt.Key_8), parent)
        s8.activated.connect(lambda: parent.keyPressEvent(k='8'))
        s9 = QShortcut(QKeySequence(Qt.Key_9), parent)
        s9.activated.connect(lambda: parent.keyPressEvent(k='9'))


class OpenGLWidget(QGLWidget):
    def __init__(self, view):
        self.view = view
        QGLWidget.__init__(self)
        # ---------- Navigate Shortcuts ----------------
        self.shortcuts = ShortcutsBindings(self)

    @property
    def aspect_ratio(self):
        rect = self.geometry()
        if rect.height():
            return rect.width() / rect.height()
        return 4 / 3

    def initializeGL(self):
        self.view.model.init()

    def paintGL(self):
        self.view.model.draw()

    def keyPressEvent(self, event=None, k=None):
        if event or k:
            k = event.text() if event else k
            self.view.controller.key_press_event(k)

    def wheelEvent(self, event):
        self.view.controller.wheel_rotate(event)

    def mouseMoveEvent(self, event):
        self.view.controller.mouse_move(event)

    def mousePressEvent(self, event):
        self.view.controller.set_mouse_pos(event)


class FunctionsMenuDock(QDockWidget):
    def __init__(self, view):
        self.view = view
        QDockWidget.__init__(self)
        self.setMinimumWidth(300)
        # ------- Background Color ---------
        self.setAutoFillBackground(True)
        p = self.palette()
        c = QColor.fromRgb(*widget_background_color)
        p.setColor(self.backgroundRole(), c)
        self.setPalette(p)
        self.setStyleSheet(side_widget_style)
        # ------------ Main Widget ------------
        self.docked_widget = QWidget()
        self.setWidget(self.docked_widget)
        self.layout = CustomVLayout()
        self.docked_widget.setLayout(self.layout)
        self.docked_widget.setStyleSheet(side_dock_docked_widget)
        # ------------- Add Function ---------------
        self.add_f_button = QPushButton("Add Function")
        self.add_f_button.clicked.connect(self.add_function)
        self.layout.addWidget(self.add_f_button)
        # ---------------- Functions List -------------
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_w_layout = QVBoxLayout(self.scroll_area_widget)

        # f1 = ExpressionWidget()
        # self.scroll_area_w_layout.addWidget(f1)
        # f2 = ExpressionWidget()
        # self.scroll_area_w_layout.addWidget(f2)

        # self.scroll_area_w_layout.insertStretch(-1)
        # self.scroll_area.setFixedHeight(500)

        self.scroll_area_widget.setStyleSheet(side_dock_scroll_area)
        self.layout.addWidget(self.scroll_area)
        self.setTitleBarWidget(QWidget(None))

    @Slot()
    def add_function(self, event):
        c = np.array([random.randint(0,256) for x in range(3)]+[255])
        c_normalized = c/255
        func = self.view.model.new_func(color=c_normalized[:3], t_as_time=True)
        f = ExpressionWidget(self, func, color=c)
        self.scroll_area_w_layout.addWidget(f)

    def del_function(self, func):
        self.view.model.functions.remove(func)
        del func


class TimelineDock(QDockWidget):
    def __init__(self, view):
        self.view = view
        QDockWidget.__init__(self)
        self.docked_widget = QWidget()
        self.setWidget(self.docked_widget)
        self.layout = QVBoxLayout()
        self.buttons = QHBoxLayout()

        self.b0 = QPushButton("Reset T")
        self.b1 = QPushButton("<")
        self.b2 = QPushButton("■")
        self.b3 = QPushButton("►")
        self.b4 = QPushButton(">")
        self.b5 = QPushButton("0.5")
        self.b6 = QPushButton("0.75")
        self.b7 = QPushButton("1")
        self.b8 = QPushButton("1.25")
        self.b9 = QPushButton("1.5")

        self.buttons.addWidget(self.b0)
        self.buttons.addWidget(self.b1)
        self.buttons.addWidget(self.b2)
        self.buttons.addWidget(self.b3)
        self.buttons.addWidget(self.b4)
        self.buttons.addWidget(self.b5)
        self.buttons.addWidget(self.b6)
        self.buttons.addWidget(self.b7)
        self.buttons.addWidget(self.b8)
        self.buttons.addWidget(self.b9)

        self.time_counter = QLabel("")
        self.buttons.addWidget(self.time_counter)

        self.b0.clicked.connect(self.reset_time)
        self.b1.clicked.connect(lambda e: self.change_time(e, -5))
        self.b2.clicked.connect(self.stop_time)
        self.b3.clicked.connect(self.start_time)
        self.b4.clicked.connect(lambda e: self.change_time(e, 5))
        self.b5.clicked.connect(lambda e: self.set_clock_speed(e, 0.5))
        self.b6.clicked.connect(lambda e: self.set_clock_speed(e, 0.75))
        self.b7.clicked.connect(lambda e: self.set_clock_speed(e, 1.0))
        self.b8.clicked.connect(lambda e: self.set_clock_speed(e, 1.25))
        self.b9.clicked.connect(lambda e: self.set_clock_speed(e, 1.5))

        self.layout.addLayout(self.buttons)

        self.slider = QSlider(Qt.Horizontal)
        self.layout.addWidget(self.slider)

        self.docked_widget.setLayout(self.layout)

        self.setStyleSheet(slider_style)
        self.setTitleBarWidget(QWidget(None))

        self.clock = self.view.model.clock
        self.clock.bind_widget(self.time_counter)

    @Slot()
    def set_clock_speed(self, event, s):
        self.clock.set_speed(s)

    @Slot()
    def reset_time(self, event):
        self.clock.reset_time()

    @Slot()
    def stop_time(self, event):
        self.clock.stop()

    @Slot()
    def start_time(self, event):
        self.clock.start()

    @Slot()
    def change_time(self, event, dt=None):
        t = self.clock.time
        self.clock.set_time(t + dt)


class CustomVLayout(QVBoxLayout):
    def geometry(self):
        return QRect(0, 0, 350, 0)

    def maximumSize(self):
        return QSize(400, 0)


class ExpressionWidget(QWidget):
    def __init__(self, parent, func, color):
        self.parent = parent
        self.func = func
        QWidget.__init__(self)
        self.setMaximumHeight(200)
        self.setAutoFillBackground(True)

        self.label = QLabel("Function 1")
        self.color_label = QPushButton()
        self.color_label.setFixedHeight(20)
        self.color_label.setFixedWidth(50)
        self.color_label.setObjectName("color_layout")
        self.color_label.clicked.connect(self.select_color)

        self.del_button = QPushButton("X")
        self.del_button.clicked.connect(self.delete_function)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.label)
        self.h_layout.addWidget(self.color_label)
        self.h_layout.addWidget(self.del_button)

        c = ",".join([str(x) for x in color])
        self.color_label.setStyleSheet('background-color: rgba(' + c + ')')

        self.input = QLineEdit()
        self.input.editingFinished.connect(self.change_expression)

        self.show_button = QPushButton("E")

        self.layout = QVBoxLayout()
        self.layout.setMargin(10)
        self.setLayout(self.layout)
        self.layout.addLayout(self.h_layout)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.show_button)

        s = QFrame()
        s.setFixedHeight(1)
        s.setFrameShape(QFrame.HLine)
        s.setStyleSheet("QFrame { background-color: rgb(115, 115, 115); }")
        self.layout.addWidget(s)
        # ------------ Parameters ---------------
        self.parameters_layout = QVBoxLayout()

        # ---------------- Separator -------------
        s = QFrame()
        s.setFixedHeight(2)
        s.setFrameShape(QFrame.HLine)
        s.setStyleSheet("QFrame { background-color: rgb(115, 115, 115); }")
        self.layout.addWidget(s)

    @Slot()
    def change_expression(self):
        self.func.change_expression(self.input.text())


    @Slot()
    def select_color(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            col = np.array(color.getRgb())/255
            self.func.set_color(col[:3])
            c = ",".join([str(x) for x in color.getRgb()])
            self.color_label.setStyleSheet('background-color: rgba(' + c + ')')

    @Slot()
    def delete_function(self, event):
        self.parent.del_function(self.func)
        self.close()
