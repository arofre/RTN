import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

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
        correct = True
        for i in number_list:
            if correct == True:
                guess = input("Input")
                if guess == i:
                    print("Correct, next number")
                    correct = True
                else:
                    print("Wrong")
                    correct = False
        if correct == True:
            print("Every number was correct")




class Gui(App):

    def build(self):
        return root()

gui = Gui()
gui.run()