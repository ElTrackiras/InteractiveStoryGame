from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty

Window.size = (500, 500)
Builder.load_file('Assets/main.kv')


class CharacterBuilder(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    gender = ''

    def gender_set(self, instance, value, gender):
        if value:
            self.gender = gender

    def done(self):
        if self.first_name.text != '' and self.last_name.text != '' and self.gender != '':
            with open('Assets/Character.txt', 'w') as f:
                f.write(self.first_name.text + '\n' + self.last_name.text + '\n' + self.gender)
            self.manager.current = 'prologue_screen'
        else:
            print('Invalid')


class PrologueCreation(Screen):
    pass


class InteractiveStory(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(CharacterBuilder(name='character_builder_screen'))
        sm.add_widget(PrologueCreation(name = 'prologue_screen'))
        return sm


if __name__ == '__main__':
    InteractiveStory().run()
