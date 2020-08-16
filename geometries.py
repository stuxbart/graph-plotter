from OpenGL.GL import *
import numpy as np


class Geometries:
    def __init__(self):
        # triangle
        triangle = [
            # vertices           colors
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0
        ]
        self.tv_count = int(len(triangle) / 6)
        triangle = np.array(triangle, dtype=np.float32)

        self.vao_triangle = glGenVertexArrays(1)
        glBindVertexArray(self.vao_triangle)
        vbo_triangle = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_triangle)
        glBufferData(GL_ARRAY_BUFFER, len(triangle) * 4, triangle, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

        triangle_3 = [
            # vertices           colors
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, #1
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, #2
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0, #3
            0.0, 0.0, 1.0, 1.0, 1.0, 1.0,  # 4
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,  # 1
        ]

        triangle_3 = np.array(triangle_3, dtype=np.float32)

        indices = [
            1, 2, 3,
            1, 2, 4,
            2, 3, 4,
            1, 3, 4
        ]

        self.ti_count = len(indices)

        indices = np.array(indices, dtype=np.uint32)

        self.vao_triangle_3 = glGenVertexArrays(1)
        glBindVertexArray(self.vao_triangle_3)
        vbo_triangle_3 = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_triangle_3)
        glBufferData(GL_ARRAY_BUFFER, len(triangle_3) * 4, triangle_3, GL_STATIC_DRAW)

        cube_ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cube_ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices)*4, indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

    def bind_triangle(self):
        glBindVertexArray(self.vao_triangle)

    def bind_triangle_3(self):
        glBindVertexArray(self.vao_triangle_3)


class Coordinate:
    def __init__(self):
        self.nx = 20
        self.ny = 20
        self.nz = 20
        self.density = 0.5
        self.x_range = [-self.nx // 2, self.nx // 2]
        self.y_range = [-self.ny // 2, self.ny // 2]
        self.z_range = [-self.nz // 2, self.nz // 2]
        self.xs = np.arange(self.x_range[0], self.x_range[1] + self.density, self.density)
        self.ys = np.arange(self.y_range[0], self.y_range[1] + self.density, self.density)
        self.zs = np.arange(self.z_range[0], self.z_range[1] + self.density, self.density)
        self.x_lines = [((x, 0, self.ys[0]), (x, 0, self.ys[-1])) for x in self.xs]
        self.y_lines = [((y, 0, self.xs[0]), (y, 0, self.xs[-1])) for y in self.ys]
        # self.z_lines = [((self.xs[0], 0, z), (self.xs[-1], 0, z)) for z in self.ys]
        self.x_color = (168 / 255, 50 / 255, 50 / 255)
        self.y_color = (50 / 255, 168 / 255, 82 / 255)
        self.z_color = (50 / 255, 93 / 255, 168 / 255)
        self.neutral_color = (0.3, 0.3, 0.3)

        def colors(coords):
            if coords[0] == 0:
                return self.y_color
            if coords[1] == 0:
                return self.x_color
            return self.neutral_color

        vertices = [((x, self.ys[0], 0), colors((x, self.ys[0], 0)), (x, self.ys[-1], 0), colors((x, self.ys[-1], 0))) for x in self.xs]\
                 + [((self.xs[0], y, 0), colors((self.xs[0], y, 0)), (self.xs[-1], y, 0), colors((self.xs[-1], y, 0))) for y in self.xs]\
                 + [((0, 0, self.zs[0]), self.z_color, (0, 0, self.zs[-1]), self.z_color)]
        vertices = np.array(vertices, dtype=np.float32).reshape(12*len(vertices))
        self.cv_count = int(len(vertices) / 6)

        self.vao_coordinate = glGenVertexArrays(1)
        glBindVertexArray(self.vao_coordinate)
        vbo_coordinate = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_coordinate)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)

    def bind_coordinate(self):
        glBindVertexArray(self.vao_coordinate)


# class F:
#     def __init__(self):
#         self.color = (1.0, 1.0, 1.0)
#         self.speed = 1
#         self.n = 20
#         self.density = 0.1
#         self.xs = np.arange(-self.n//2, self.n//2, self.density, dtype=np.float32)
#         self.ys = np.arange(-self.n//2, self.n//2, self.density, dtype=np.float32)
#         self.xx, self.yy = np.meshgrid(self.xs, self.ys)
#         self.z = np.sin(self.xx**2 + self.yy**2)
#         self.stacked = np.column_stack((self.xx.flat, self.yy.flat, self.z.flat))
#         self.vertices = np.column_stack((self.stacked, np.ones_like(self.stacked)))
#         self.vertices = np.array(self.vertices, dtype=np.float32).reshape(len(self.vertices)*6)
#         self.fv_count = int(len(self.vertices)/6)
#
#         self.vao_f = glGenVertexArrays(1)
#         glBindVertexArray(self.vao_f)
#         self.vbo_f = glGenBuffers(1)
#         glBindBuffer(GL_ARRAY_BUFFER, self.vbo_f)
#         glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, self.vertices, GL_STATIC_DRAW)
#
#         glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
#         glEnableVertexAttribArray(0)
#
#         glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
#         glEnableVertexAttribArray(1)
#         glBindVertexArray(0)
#
#     def __call__(self, t, *args, **kwargs):
#         ct = t * self.speed
#         z = (self.xx**2 + self.yy**2)/50 * np.power(np.e,np.sin(self.xx+self.yy * ct)*np.cos(self.yy+self.xx * ct))+ np.sin(self.yy/self.xx + ct)
#         stacked = np.column_stack((self.xx.flat, self.yy.flat, z.flat))
#         vertices = np.column_stack((stacked, np.ones_like(stacked)))
#         vertices = vertices.reshape(len(vertices) * 6)
#         self.fv_count = int(len(vertices) / 6)
#
#         glBindVertexArray(self.vao_f)
#         glBindBuffer(GL_ARRAY_BUFFER, self.vbo_f)
#         glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices, GL_STATIC_DRAW)
#
#         glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
#         glEnableVertexAttribArray(0)
#
#         glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
#         glEnableVertexAttribArray(1)
#         glBindVertexArray(0)
#         del vertices, z, stacked,
#
#     def bind_f(self):
#         glBindVertexArray(self.vao_f)


class Function:
    def __init__(self, init=True, three_dim=True, t_as_time=True, color=(0, 1.0, 1.0), density=0.1):
        self.exp = 'sin(x * t)'
        self.functions_dict = {'sin': np.sin, 'cos': np.cos, 'e': np.e, 'pow': np.power}
        self.color = np.array(color)
        self.color_arr = None
        self.three_dimensions = three_dim
        self.t_as_time = t_as_time
        self.density = density
        self.domain_x = [-10, 10]
        self.domain_y = [-10, 10]
        self.domain_z = [-10.0, 10.0]
        self.xs = None
        self.ys = None
        self.xx = None
        self.yy = None
        self.zz = None
        self.xxyy = None
        self.stacked = None
        self.vertices = None
        self.fv_count = None
        self.vao_f = glGenVertexArrays(1)
        glBindVertexArray(self.vao_f)
        self.vbo_f = glGenBuffers(1)
        glBindVertexArray(0)
        self.parameters = {}

        if init:
            self.make_grid()
            self.eval(0.0)

    def make_grid(self):
        if self.three_dimensions:
            self.xs = np.arange(self.domain_x[0], self.domain_x[1], self.density, dtype=np.float32)
            self.ys = np.arange(self.domain_y[0], self.domain_y[1], self.density, dtype=np.float32)
            self.xx, self.yy = np.meshgrid(self.xs, self.ys)
            self.xxyy = np.column_stack((self.xx.flat, self.yy.flat))
        else:
            self.xx = np.arange(self.domain_x[0], self.domain_x[1], self.density, dtype=np.float32)

        self.fv_count = int(len(self.xx.flat))
        self.set_color(self.color)

    def eval(self, t=None):
        if self.three_dimensions:
            try:
                self.zz = eval(self.exp, self.functions_dict, {'t': t, 'x': self.xx, 'y': self.yy})
            except:
                self.zz = np.zeros_like(self.xx)
        else:
            self.yy = np.sin(self.xx + t)
            self.zz = np.zeros_like(self.xx)

        stacked = np.column_stack((self.xxyy, self.zz.flat))

        vertices = np.column_stack((stacked, self.color_arr))
        vertices = np.array(vertices, dtype=np.float32).reshape(len(vertices) * 6)

        glBindVertexArray(self.vao_f)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_f)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBindVertexArray(0)
        del vertices, stacked, self.zz

    def draw(self, t=None):
        if self.t_as_time:
            self.eval(t)
        glBindVertexArray(self.vao_f)
        glDrawArrays(GL_LINES, 0, self.fv_count)

    def set_color(self, c):
        self.color = c
        self.color_arr = np.full((len(self.xx.flat), 3), self.color)

    def change_expression(self, e):
        self.exp = e

x = """
# self.vertices = np.array([((x, y, z), self.color) for x, y, z in zip(self.xs, self.ys, self.zs)], dtype=np.float32)
        self.vertices = np.array([[((x, y, np.sin(x)*np.sin(y)), self.color) for y, z in zip(self.ys, self.zs)] for x in self.xs], dtype=np.float32)
        self.vertices = self.vertices.reshape(len(self.vertices)*len(self.ys)*6)
        self.fv_count = int(len(self.vertices)/6)
        print(self.fv_count)
        self.vao_f = glGenVertexArrays(1)

    def __call__(self, *args, **kwargs):
        ct = time.perf_counter() * self.speed
        self.zs = np.power(np.e, self.xs) + np.sin(self.xs * self.w * ct)*np.sin(self.ys * self.w * ct)
        self.vertices = np.array([[((x, y, np.sin(x + ct)*np.sin(y + ct)), self.color) for y, z in zip(self.ys, self.zs)] for x in self.xs], dtype=np.float32)
        self.vertices = self.vertices.reshape(len(self.vertices)*len(self.ys)*6)

        self.fv_count = int(len(self.vertices) / 6)
"""