import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import random

kivy.require('1.9.0')

class root(BoxLayout):
    def __init__(self):
        super(root, self).__init__()

    def process(self):
        self.text = self.ids.input.text

    def submit(self):
        number_list = []
        for i in self.text:
            number_list.append(i)
        print(number_list)

class Gui(App):

    def build(self):
        return root()

gui = Gui()
gui.run()