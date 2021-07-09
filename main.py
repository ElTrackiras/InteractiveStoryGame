from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from functools import partial

Window.size = (500, 500)
Builder.load_file('Assets/main.kv')

character_created = False
character_first_name = None
character_last_name = None
character_gender = None
scene_sequence = 0


# This will serve as the function to load all the data once into the system.
def data_loader():
    game_data_holder = []
    global character_created
    with open('Assets/game_data.txt', 'r') as f:
        for i in f:
            game_data_holder.append(i.replace('\n', ''))

    if game_data_holder[0] == 'CharacterExist':
        character_created = True

    character_data_holder = []
    if character_created:
        with open('Assets/Character.txt', 'r') as f:
            for i in f:
                character_data_holder.append(i.replace('\n', '').split(':'))
        for i in character_data_holder:
            print(i)
        global character_first_name
        global character_last_name
        global character_gender
        character_first_name = character_data_holder[0][1]
        character_last_name = character_data_holder[1][1]
        character_gender = character_data_holder[2][1]


data_loader()


class HomeMenu(Screen):
    def start(self):
        # Transitions to save file/continuation of the game.
        if character_created:
            self.manager.get_screen('scene_screen').display_scene()
            self.manager.current = 'scene_screen'
        # Transitions to character creation screen
        else:
            self.manager.current = 'character_builder_screen'


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
                f.write('FirstName:' + self.first_name.text + '\n' + 'LastName:' + self.last_name.text + '\n' +
                        'Gender:' + self.gender)

            with open('Assets/game_data.txt', 'w') as f:
                f.write('CharacterExist')
            self.manager.get_screen('scene_screen').display_scene()
            self.manager.current = 'scene_screen'
        else:
            print('Invalid')


class Scenes(Screen):
    scene_body_text = ObjectProperty(None)
    scene_grid = ObjectProperty()
    scene_choices_kv = ObjectProperty()
    current_choice = None

    def display_scene(self):
        print('display_scene function Initialized')
        self.scene_choices_kv.clear_widgets()
        data_loader()
        self.scene_grid.bind(minimum_height=self.scene_grid.setter('height'))
        scene_parsed = []
        scene_choices = []

        with open('Assets/StorySequence#' + str(scene_sequence) +'.txt', 'r') as f:
            x = f.read().replace('\n', '')
            scene_parsed.append(x.split('==choices==')[0])
            scene_choices.append(x.split('==choices==')[1].split('()'))

        body_scene_raw = [scene_parsed[0].split('[]')]
        body_scene_parsed = ''
        for i in body_scene_raw[0]:
            if i == 'fname':
                body_scene_parsed += character_first_name
            elif i == 'gender':
                if character_gender == 'Male':
                    body_scene_parsed += 'he'
                else:
                    body_scene_parsed += 'she'
            elif i == 'br':
                body_scene_parsed += '\n'
            else:
                body_scene_parsed += i
        self.scene_body_text.text = body_scene_parsed
        self.scene_choices_kv.bind(minimum_height=self.scene_choices_kv.setter('height'))
        self.scene_choices_kv.height = 500
        for i in scene_choices[0]:
            if i != '':
                choices_box = GridLayout(cols=2)
                choice_text = Label(text=i.split('[]')[0], size_hint_x=0.9, size_hint_y=1, halign='right')
                choice_text.text_size = Window.width * 0.9, None
                choice_text.size = choice_text.texture_size
                choice_checkbox = CheckBox(width=10, height=10, group='choices', size_hint_x=0.1)
                choice_checkbox.bind(active=partial(self.checkbox_effect, i.split('[]')[1]))
                choices_box.add_widget(choice_text)
                choices_box.add_widget(choice_checkbox)
                self.scene_choices_kv.add_widget(choices_box)

    def checkbox_effect(self, effect, instance, value):
        if value:
            self.current_choice = effect
            print(self.current_choice)

    def next_scene(self):
        global scene_sequence
        scene_sequence += 1
        print(scene_sequence)
        if self.current_choice:
            print(self.current_choice)
            with open('Assets/PlayerChoices.txt', 'a') as f:
                f.write(self.current_choice + '\n')
            self.display_scene()
        else:
            print('No choice selected.')


class InteractiveStory(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(HomeMenu(name='home_menu_screen'))
        sm.add_widget(CharacterBuilder(name='character_builder_screen'))
        sm.add_widget(Scenes(name='scene_screen'))
        return sm


if __name__ == '__main__':
    InteractiveStory().run()
