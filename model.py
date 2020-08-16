import time
from OpenGL.GL import *
from OpenGL.GL import shaders
from pyrr import Matrix44, matrix44, Vector3
import numpy as np

from geometries import Coordinate, Function


vertex_shader = """
# version 330
in layout(location=0) vec3 position;
in layout(location=1) vec3 colors;

out vec3 newColor;
uniform mat4 rotation;
uniform mat4 vp;
uniform mat4 translation;
    
void main(){
    gl_Position = vp * rotation * translation * vec4(position, 1.0);
    newColor = colors;
}
"""

fragment_shader = """
# version 330

in vec3 newColor;
out vec4 outColor;

void main(){
    outColor = vec4(newColor, 1.0);
}
"""


class OpenGLController:
    def __init__(self):
        self.view = None
        self.refresh_loop = None
        self.clock = Clock()
        self.initialized = False
        # -------- OpenGL vars loc ---------
        self.vp_loc = None
        self.rot_loc = None
        self.trans_loc = None
        # ------------- Rotation -----------
        self.rot_x_angle = 0.0
        self.rot_y_angle = 0.0
        self.rot_z_angle = 0.0
        self.rot_x = Matrix44.identity()
        self.rot_y = Matrix44.identity()
        self.rot_z = Matrix44.identity()
        # ------------ Translation ---------
        self.trans_x = 0.0
        self.trans_y = 0.0
        self.trans_z = 0.0
        # ----------- Perspective ----------
        self.use_perspective = True
        self.zoom = -5.0
        self.view_angle = 30.0
        self.min_clipping = 0.1
        self.max_clipping = 200
        # --------- Render Items -----------
        self.c = None
        self.functions = []

    def set_view(self, view):
        self.view = view

    def init(self):
        if not self.initialized:
            shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                                      OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))
            glClearColor(0.2, 0.2, 0.2, 1)
            glUseProgram(shader)
            glEnable(GL_DEPTH_TEST)
            self.rot_loc = glGetUniformLocation(shader, "rotation")
            self.vp_loc = glGetUniformLocation(shader, "vp")
            self.trans_loc = glGetUniformLocation(shader, "translation")
            self.set_perspective()
            self.initialize_objects()
            self.initialized = True

    @property
    def aspect_ratio(self):
        return self.view.opengl_widget.aspect_ratio

    def initialize_objects(self):
        self.c = Coordinate()
        # self.functions.append(Function(t_as_time=True))

    def set_perspective(self):
        if self.use_perspective:
            view = matrix44.create_from_translation(Vector3([0.0, 0.0, self.zoom]))
            projection = matrix44.create_perspective_projection_matrix(self.view_angle, self.aspect_ratio,
                                                                       self.min_clipping, self.max_clipping)
            vp = matrix44.multiply(view, projection)
        else:
            vp = np.diag([1, self.aspect_ratio, 0, -self.zoom / 2])
        glUniformMatrix4fv(self.vp_loc, 1, GL_FALSE, vp)

    def draw(self):
        self.clock.tick()
        self.clock.update_widget_time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        gl_widget_size = self.view.opengl_widget.geometry()
        self.resize_gl(gl_widget_size.width(), gl_widget_size.height())
        self.set_perspective()
        self.calculate_rotation()
        self.calculate_translation()
        if self.c:
            self.c.bind_coordinate()
            glDrawArrays(GL_LINES, 0, self.c.cv_count)
        # if self.mesh:
        #     self.mesh.bind_triangle_3()
        #     glDrawElements(GL_TRIANGLE_STRIP, self.mesh.ti_count, GL_UNSIGNED_INT, None)

        for f in self.functions:
            f.draw(self.clock.time)
            # f(self.clock.time)
            # f.bind_f()
            # glDrawArrays(GL_POINTS, 0, f.fv_count)

    def calculate_rotation(self):
        self.rot_x = Matrix44.from_x_rotation(self.rot_x_angle)
        self.rot_y = Matrix44.from_y_rotation(self.rot_y_angle)
        self.rot_z = Matrix44.from_z_rotation(self.rot_z_angle)
        rotation_matrix = matrix44.multiply(self.rot_z, matrix44.multiply(self.rot_x, self.rot_y))
        glUniformMatrix4fv(self.rot_loc, 1, GL_FALSE, rotation_matrix)

    def calculate_translation(self):
        translation_matrix = matrix44.create_from_translation(Vector3([self.trans_x, self.trans_y, self.trans_z]))
        glUniformMatrix4fv(self.trans_loc, 1, GL_FALSE, translation_matrix)

    def resize_gl(self, w, h):
        glViewport(0, 0, w, h)

    def set_rotation(self, rot_x_angle, rot_y_angle, rot_z_angle):
        self.rot_x_angle = rot_x_angle
        self.rot_y_angle = rot_y_angle
        self.rot_z_angle = rot_z_angle
        self.calculate_rotation()

    def rotate(self, rot_x_angle, rot_y_angle, rot_z_angle):
        self.rot_x_angle += rot_x_angle
        self.rot_y_angle += rot_y_angle
        self.rot_z_angle += rot_z_angle
        self.calculate_rotation()

    def translate(self, trans_x, trans_y, trans_z):
        self.trans_x += trans_x
        self.trans_y += trans_y
        self.trans_z += trans_z
        self.calculate_translation()

    def change_zoom(self, delta_zoom):
        self.zoom += delta_zoom
        self.set_perspective()

    def new_func(self, *args, **kwargs):
        f = Function(*args, **kwargs)
        self.functions.append(f)
        return f


class Clock:
    def __init__(self, init=False):
        self._system_time = time.perf_counter
        self._system_time_last = self._system_time()
        self._time = 0.0
        self._running = False
        self._initialized = False
        self._widget = None
        self._speed = 1.0
        if init:
            self.start()

    @property
    def time(self):
        return self._time

    def start(self):
        self._running = True
        if not self._initialized:
            self._system_time_last = self._system_time()
            self._initialized = True

    def stop(self):
        self._running = False

    def change_time(self, dt):
        self._time += dt

    def set_time(self, t):
        self._time = t

    def reset_time(self):
        self.set_time(0.0)

    def bind_widget(self, w):
        self._widget = w

    def update_widget_time(self):
        if self._widget:
            self._widget.setText(f"T: {self.time:.2f}s")

    def tick(self):
        if self._running:
            dt = self._system_time() - self._system_time_last
            self._time += dt * self._speed
        self._system_time_last = self._system_time()

    def set_speed(self, s):
        self._speed = s
