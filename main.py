from view import View
from controler import Controller
from model import OpenGLController

if __name__ == "__main__":
    opengl = OpenGLController()
    v = View()
    c = Controller()
    c.set_model(opengl)
    c.set_view(v)
    c.init()
