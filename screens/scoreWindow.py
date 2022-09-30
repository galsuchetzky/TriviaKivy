import kivy

import defaults
import utils

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class ScoreWindow(Screen):
    TITLE_TXT = StringProperty("טבלת ניקוד"[::-1])
    NUMBER_TXT = StringProperty("מספר"[::-1])
    DATE_TXT = StringProperty("תאריך"[::-1])
    SCORE_TXT = StringProperty("ניקוד"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name

    def on_pre_enter(self, *args):
        row_height = self.ids.score_title.texture_size[1]

        # Configure the master scroll view, will hold the grid of tables.
        master_scroll_view = self.ids.master_scroll_view
        master_scroll_view.height = Window.size[1] - self.ids.score_title.height

        # Configure the grid of tables.
        tables_grid = self.ids.master_grid
        tables_grid.rows = len(defaults.GameModes)
        tables_grid.height = 0
        tables_grid.clear_widgets()

        # Devide scores into modes.
        scores_by_mode = [[] for _ in range(len(defaults.GameModes))]
        scores = utils.get_scores()
        for score_dict in scores.values():
            scores_by_mode[score_dict['game_mode']].append(score_dict)

        # Build tables.

        for game_mode in range(len(defaults.GameModes)):
            # Each table will have a row for the name and a row for the table grid.
            head_grid = GridLayout(cols=1, rows=2, size_hint_y=None)

            # Add table name
            table_name_label = Label(text=defaults.GameModes.get_name(game_mode),
                                     height=row_height,
                                     size_hint_y=None)

            head_grid.add_widget(table_name_label)

            # Create and fill the table grid.
            tmp_scores = scores_by_mode[game_mode]
            table = GridLayout(size_hint_y=None, cols=3, rows=len(tmp_scores) + 2)  # +1 for headers +1 for line
            # space label

            table.height = table.rows * row_height
            head_grid.add_widget(table)
            head_grid.height = table.height + row_height  # for table name
            tables_grid.height += head_grid.height

            # Add headers to the table.
            headers = [Label(text=self.SCORE_TXT, height=row_height, size_hint_y=None),
                       Label(text=self.DATE_TXT, height=row_height, size_hint_y=None),
                       Label(text=self.NUMBER_TXT, height=row_height, size_hint_y=None)]

            for header in headers:
                table.add_widget(header)

            # Add scores to the table.
            tmp_scores = [(a['score'], a['date'], a['id']) for a in tmp_scores]
            for score_row in tmp_scores:
                for j in range(len(headers)):
                    l = Label(text=str(score_row[j]))
                    table.add_widget(l)

            # Line space
            table.add_widget(Label(text='', height=row_height, size_hint_y=None))

            tables_grid.add_widget(head_grid)

        print(tables_grid.height)


    def build_table(self, table_name, scores):
        scroll_view = ScrollView(size_hint_y=None, do_scroll_x=False)
        table = GridLayout(size_hint_y=None)

        scroll_view.add_widget(table)

        row_height = self.ids.score_title.texture_size[1]
        table.rows = len(scores)
        table.height = table.rows * row_height

        scores = [(a['score'], a['date'], a['id']) for a in scores.values()]
        for score_row in scores:
            for j in range(3):
                l = Label(text=str(score_row[j]))
                table.add_widget(l)
