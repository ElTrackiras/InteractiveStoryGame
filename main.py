from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty

Window.size = (500, 500)
Builder.load_file('Assets/main.kv')

character_created = False
character_first_name = None
character_last_name = None
character_gender = None


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
            self.manager.current = 'prologue_screen'
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

            self.manager.current = 'prologue_screen'
        else:
            print('Invalid')


class PrologueCreation(Screen):
    pass


class InteractiveStory(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(HomeMenu(name='home_menu_screen'))
        sm.add_widget(CharacterBuilder(name='character_builder_screen'))
        sm.add_widget(PrologueCreation(name='prologue_screen'))

        return sm


if __name__ == '__main__':
    InteractiveStory().run()
