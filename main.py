import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import sqlite3

sm = ScreenManager()
kivy.require('1.9.0')
Window.size = (360, 760)
class root(BoxLayout):
    def __init__(self):
        super(root, self).__init__()

class MenuScreen(Screen):
    number_list = []
    def process(self):
        self.text = self.ids.input.text
        print(self.text)
    pass

    def submit(self):
        global number_list
        global initial_length
        number_list = []
        for i in self.text:
            number_list.append(int(i))
        self.ids.input.text = ''
        initial_length = len(number_list)

class GuessScreen(Screen):
    def guess(self, number):
        if number == number_list[0]:
            number_list.pop(0)
            if number_list == []:
                self.ids.guess_text.text = 'All numbers are correct'
                Clock.schedule_once(self.change_screen_menu, 3)

        elif number != number_list[0]:
            self.ids.guess_text.text = f'Incorrect, you guessed {initial_length - len(number_list)} / {initial_length}'
            Clock.schedule_once(self.change_screen_menu, 3)

    def change_screen_menu(self, obj):
        self.manager.current = 'menu'
        Clock.schedule_once(self.reset_text, 2)
    pass
    def reset_text(self, obj):
        self.ids.guess_text.text = 'Guess the number?'

class DBScreen(Screen):
    def save_number(self):

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        name =  self.ids.save_name.text,
        number = self.ids.save_number.text,
        name = str(name)
        number = str(number)

        print(number)
        print(name)

        c.execute("INSERT INTO database VALUES (?,?)", (name, number))

        c.execute("SELECT * FROM database WHERE name=:name", {'name': name})

        print(c.fetchone())

        conn.commit()
        conn.close()

    pass

class Gui(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GuessScreen(name='guess'))
        sm.add_widget(DBScreen(name='database'))
        sm.current = 'menu'

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE if not exists database(
                    name text,
                    number text
                    )""")

        conn.commit()
        conn.close()

        return sm

if __name__ == '__main__' :
    gui = Gui()
    gui.run()