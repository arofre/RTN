import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout


# Create the manager
sm = ScreenManager()
kivy.require('1.9.0')

Window.size = (360, 760)

class root(BoxLayout):
    def __init__(self):
        super(root, self).__init__()

class MenuScreen(Screen):
    def process(self):
        self.text = self.ids.input.text
        print(self.text)
    pass

    def submit(self):
        number_list = []
        for i in self.text:
            number_list.append(int(i))

class GuessScreen(Screen):
    def guess(self, number):
        for i in MenuScreen.number_list:
            if correct == True:
                if number == i:
                    print("Correct, next number")
                    correct = True
                else:
                    print("Wrong")
                    correct = False
    pass

class SettingsScreen(Screen):
    pass

class Gui(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GuessScreen(name='guess'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'menu'
        return sm

gui = Gui()
gui.run()