import kivy

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.core.window import Window

class ScoreWindow(Screen):
    def __init__(self, name):
        super().__init__()
        self.name = name
        # TODO this calculation is off, need to take other things into account???
        # self.ids.table_scrollview.height = Window.size[1] - 3 * self.ids.score_title.texture_size[1]
        self.ids.table_scrollview.height = Window.size[0] - self.ids.score_title.height - self.ids.g1.height

    def on_pre_enter(self, *args):
        table = self.ids.table_grid
        self.ids.table_grid.rows=20
        self.ids.table_grid.height=self.ids.score_title.texture_size[1]*20

        for i in range(20):
            for j in range(3):
                l = Label(text='asdf')
                table.add_widget(l)


