import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.graphics import Color, Canvas, Rectangle
from kivy.config import Config
import random

Config.set('graphics', 'width', '1000')


class UiDesign(GridLayout):
    def __init__(self, **kwargs):
        super(UiDesign, self).__init__(**kwargs)
        with self.canvas:
            # Color(0, 0, 0, 0)
            self.rect = Rectangle(source="German.JPG", pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

        file = open("GermanWords")
        self.german_new_words = file.readlines()
        file.close()
        self.save = ""
        self.total_time_in_sec = 0
        self.rows = 1
        self.padding = 50

        self.inside = GridLayout(padding=120)
        self.inside.rows = 6
        self.inside.display_label = Label(text="Random New GermanWords", color=[2, 0.1, 0.88, 0.99],
                                          font_size="35sp", markup=True)
        self.inside.add_widget(self.inside.display_label)

        self.inside.add_widget(Label(text="\n" + "[i]ReminderTime (hh:mm:ss)[/i]", color=[2, 0.42, 0.74, 1],
                                     font_size="20sp",
                                     markup=True))
        self.inside.user_input_time = TextInput(text="00:00:00", multiline=False, padding=10)
        self.inside.add_widget(self.inside.user_input_time)

        self.inside.add_widget(Label(text="\n" + "[i]Add New German Word[/i]", color=[2, 0.42, 0.74, 1],
                                     font_size="20sp",
                                     markup=True))
        self.inside.user_input_new_word = TextInput(multiline=False)
        self.inside.add_widget(self.inside.user_input_new_word)

        self.add_button = Button(text="Add New Word", background_normal="Add_New_Word.png", size_hint=(None, None),
                                 size=(150, 50))
        self.add_button.bind(on_press=self.adding_new_word)
        self.add_widget(self.add_button)

        self.add_widget(self.inside)
        self.submit_button = Button(text="Submit", size_hint=(None, None), background_normal="Button_img.png",
                                    background_color=(0.5, 1, 0.5, 2), size=(150, 50))
        self.submit_button.bind(on_press=self.reminder_delay)
        self.add_widget(self.submit_button)

        self.start_button = Button(text="Start / Reset", background_normal="German_BG_1.JPG", background_color=(0.2, 1, 0.5, 2),
                                   size_hint=(None, None), size=(150, 50), pos_hint={"x": 0.5, "y": 0.3})
        self.start_button.bind(on_press=self.start_german_word)
        self.add_widget(self.start_button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def start_german_word(self, instance):
        random.shuffle(self.german_new_words)
        self.save = random.choice(self.german_new_words)
        self.inside.display_label.text = "\n" + self.save

    def reminder_delay(self, instance):
        self.inside.display_label.text = ""
        hrs_in_sec = 0
        min_in_sec = 0
        sec = 0
        list_of_hms = self.inside.user_input_time.text.rsplit(":")
        for idx, delay_time in enumerate(list_of_hms):
            if idx == 0:
                hrs_in_sec = (int(delay_time) * 60 * 60)
            elif idx == 1:
                min_in_sec = (int(delay_time) * 60)
            else:
                sec = int(delay_time)
            self.total_time_in_sec = hrs_in_sec + min_in_sec + sec
            print(self.total_time_in_sec)
        Clock.schedule_once(self.hold_previous_german_word, self.total_time_in_sec)

    def hold_previous_german_word(self, instance):
        popup_layout = GridLayout(cols=1, padding=50)
        popup_layout.add_widget(Label(text=self.save, font_size="25sp", italic=True))
        close_button = Button(text="Close", size_hint=(0.5, 0.5), background_color=(2, 1, 0.5, 2))
        popup_layout.add_widget(close_button)
        popup = Popup(title=" Word to Remember ", content=popup_layout,
                      size_hint=(None, None), size=(250, 250))
        popup.open()
        self.inside.display_label.text = self.save
        close_button.bind(on_press=popup.dismiss)

    def adding_new_word(self, instance):
        if (self.inside.user_input_new_word.text + "\n") not in self.german_new_words:
            self.german_new_words.append(self.inside.user_input_new_word.text)
            file = open("GermanWords", "a")
            file.writelines(self.inside.user_input_new_word.text + "\n")
            file.close()
            self.inside.display_label.text = "New Word Added Successfully"
            self.inside.user_input_new_word.text = ""
        else:
            self.inside.display_label.text = "This word is already available"
            self.inside.user_input_new_word.text = ""


class ReminderApplication(App):
    def build(self):
        return UiDesign()


if __name__ == "__main__":
    ReminderApplication().run()
