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
from kivymd.app import MDApp
from kivy.metrics import dp, sp

sm = ScreenManager()
kivy.require('1.9.0')
class root(BoxLayout):
    def __init__(self):
        super(root, self).__init__()

class CustomGrid(FloatLayout):
    pass

class CustomGrid(FloatLayout):
    def add_child_to_specific(self, row, col, widget):
        self.ids[row].ids[col].add_widget(widget)

class MenuScreen(Screen):
    number_list = []
    def process(self):
        self.text = self.ids.input.text
        if self.text == "":
            self.disable_submit()
        else:
            self.enable_submit()
    pass

    def submit(self):
        global number_list
        global initial_length
        number_list = []
        for i in self.text:
            number_list.append(int(i))
        self.ids.input.text = ''
        initial_length = len(number_list)

    def disable_submit(self):
        self.ids.submit.disabled = True
    def enable_submit(self):
        self.ids.submit.disabled = False

class GuessScreen(Screen):
    def guess(self, number):
        if number == number_list[0]:
            number_list.pop(0)
            if number_list == []:
                self.disable_buttons()
                self.ids.guess_text.text = 'All numbers are correct'
                Clock.schedule_once(self.change_screen_menu, 3)

        elif number != number_list[0]:
            self.disable_buttons()
            self.ids.guess_text.text = f'Incorrect, you guessed {initial_length - len(number_list)} / {initial_length}'
            Clock.schedule_once(self.change_screen_menu, 3)


    def change_screen_menu(self, obj):
        self.manager.current = 'menu'
        Clock.schedule_once(self.reset_text, 2)
        self.enable_buttons()
    pass
    def reset_text(self, obj):
        self.ids.guess_text.text = 'Guess the number?'
    def disable_buttons(self):
        self.ids.one.disabled = True
        self.ids.two.disabled = True
        self.ids.three.disabled = True
        self.ids.four.disabled = True
        self.ids.five.disabled = True
        self.ids.six.disabled = True
        self.ids.seven.disabled = True
        self.ids.eight.disabled = True
        self.ids.nine.disabled = True
        self.ids.zero.disabled = True
    def enable_buttons(self):
        self.ids.one.disabled = False
        self.ids.two.disabled = False
        self.ids.three.disabled = False
        self.ids.four.disabled = False
        self.ids.five.disabled = False
        self.ids.six.disabled = False
        self.ids.seven.disabled = False
        self.ids.eight.disabled = False
        self.ids.nine.disabled = False
        self.ids.zero.disabled = False

class DBScreen(Screen):
    def save_number(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        name = self.ids.save_name.text
        number = self.ids.save_number.text

        name = name.replace("(","").replace(")","").replace(",","").replace("'","")
        number = number.replace("(", "").replace(")", "").replace(",", "").replace("'", "")

        number = int(number)

        c.execute("INSERT INTO database VALUES (?,?)", (name, number))

        c.execute("SELECT * FROM database WHERE name=:name", {'name': name})

        conn.commit()
        conn.close()
    pass

    def save_process(self):
        self.s_name = self.ids.save_name.text
        self.s_number = self.ids.save_number.text
        if self.s_number == "" and self.s_name == "":
            self.disable_save()
        elif self.s_number != "" and self.s_name != "":
            self.enable_save()
    pass

    def disable_save(self):
        self.ids.save_button.disabled = True
    def enable_save(self):
        self.ids.save_button.disabled = False

    def load_number(self):
        global number_list
        global initial_length
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        name = self.ids.load_name.text

        if self.ids.load_name.text == "":
            self.disable_load()
        else:
            self.enable_load()


        c.execute("SELECT * FROM database WHERE name=:name", {'name': name})

        try:
            tot = c.fetchone()
            name, number = tot
            conn.commit()
            conn.close()

            number_list = []
            for i in number:
                number_list.append(int(i))
            initial_length = len(number_list)
            self.manager.current = 'guess'
            self.ids.load_name.text == ""
            print("hjej")
        except:
            self.ids.load_name.text = "Not a saved record"


    def load_process(self):
        self.load_text = self.ids.load_name.text
        print(self.load_text)
        if self.load_text == "":
            self.disable_load()
        else:
            self.enable_load()

    def disable_load(self):
        self.ids.load_button.disabled = True
    def enable_load(self):
        self.ids.load_button.disabled = False

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
                    number integer
                    )""")

        conn.commit()
        conn.close()

        self.icon = 'icon.png'
        self.title = 'RTN'
        return sm

if __name__ == '__main__' :
    gui = Gui()
    gui.run()