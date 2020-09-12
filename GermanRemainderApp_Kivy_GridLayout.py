import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
import random


class UiDesign(GridLayout):
    def __init__(self, **kwargs):
        super(UiDesign, self).__init__(**kwargs)
        self.delay_possible_dict = {"5Sec": 5, "10Sec": 10, "15Sec": 15}
        file = open("GermanWords")
        self.german_new_words = file.readlines()
        file.close()
        self.save = ""
        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2
        self.inside.display_label = Label(text="Random New GermanWords")
        self.inside.add_widget(self.inside.display_label)

        self.inside.start_button = Button(text="Start")
        self.inside.start_button.bind(on_press=self.start_german_word)
        self.inside.add_widget(self.inside.start_button)

        self.inside.add_widget(Label(text="Enter Remainder Time in Sec"))
        self.inside.user_input_time = TextInput(multiline=False)
        self.inside.add_widget(self.inside.user_input_time)

        self.inside.add_widget(Label(text="Add New German Word"))
        self.inside.user_input_new_word = TextInput(multiline=False)
        self.inside.add_widget(self.inside.user_input_new_word)

        self.add_widget(self.inside)
        self.submit_button = Button(text="Submit")
        self.submit_button.bind(on_press=self.remainder_delay)
        self.add_widget(self.submit_button)

        self.add_button = Button(text="Add New Word")
        self.add_button.bind(on_press=self.adding_new_word)
        self.add_widget(self.add_button)

    def start_german_word(self, instance):
        random.shuffle(self.german_new_words)
        self.save = random.choice(self.german_new_words)
        self.inside.display_label.text = self.save

    def remainder_delay(self, instance):
        self.inside.display_label.text = ""
        for delay_time in self.delay_possible_dict:
            if delay_time == self.inside.user_input_time.text:
                Clock.schedule_once(self.hold_previous_german_word, self.delay_possible_dict[delay_time])

    def hold_previous_german_word(self, instance):
        self.inside.display_label.text = self.save

    def adding_new_word(self, instance):
        if self.inside.user_input_new_word.text not in self.german_new_words:
            self.german_new_words.append(self.inside.user_input_new_word.text)
            file = open("GermanWords", "a")
            file.writelines(self.inside.user_input_new_word.text+"\n")
            file.close()


class RemainderApplication(App):
    def build(self):
        return UiDesign()


if __name__ == "__main__":
    RemainderApplication().run()
