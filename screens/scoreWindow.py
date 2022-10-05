import kivy

import defaults
import utils

kivy.require('2.1.0')

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

from collections import defaultdict


class ScoreWindow(Screen):
    TITLE_TXT = StringProperty("טבלת ניקוד"[::-1])
    NUMBER_TXT = StringProperty("מספר"[::-1])
    DATE_TXT = StringProperty("תאריך"[::-1])
    NAME_TXT = StringProperty("שם"[::-1])
    SCORE_TXT = StringProperty("ניקוד"[::-1])

    def __init__(self, name):
        super().__init__()
        self.name = name

    def on_pre_enter(self, *args):
        # Configure the master scroll view, will hold the grid of tables.
        master_scroll_view = self.ids.master_scroll_view
        master_scroll_view.height = Window.size[1] - self.ids.score_title.height

        # Configure the grid of tables.
        tables_grid = self.ids.master_grid
        tables_grid.rows = 0
        tables_grid.height = 0
        tables_grid.clear_widgets()

        # Build local scores.
        self.build_local_score_tables()

        # Build global scores.
        utils.get_scores_from_server(self.build_global_score_tables)

    def build_local_score_tables(self):
        """
        Building the score tables for the local player scores.
        """
        scores = utils.get_scores()
        for game_mode in range(len(defaults.GameModes)):
            table_name = utils.fix_string(defaults.GameModes.get_name(game_mode))
            self.build_table(table_name, scores[str(game_mode)])

    def build_global_score_tables(self, req, *args):
        """
        Building the score tables for the global scores.
        """
        scores = defaultdict(list, req.result)
        for game_mode in range(len(defaults.GameModes)):
            table_name = utils.fix_string(defaults.GameModes.get_name(game_mode) + ' שיתופי')
            self.build_table(table_name, scores[str(game_mode)])

    def build_table(self, table_name, scores):
        # Builds a table with the given names and scores and adds it to the window.
        row_height = self.ids.score_title.texture_size[1]
        tables_grid = self.ids.master_grid
        tables_grid.rows += 1

        # Each table will have a row for the name and a row for the table grid.
        head_grid = GridLayout(cols=1, rows=2, size_hint_y=None)

        # Add table name
        table_name_label = Label(text=table_name,
                                 height=row_height,
                                 size_hint_y=None)

        head_grid.add_widget(table_name_label)

        # Create and fill the table grid.
        # tmp_scores = scores_by_mode[game_mode]
        # tmp_scores = scores[game_mode]
        table = GridLayout(size_hint_y=None, cols=4, rows=len(scores) + 2)  # +1 for headers +1 for line

        # space label
        table.height = table.rows * row_height
        head_grid.add_widget(table)
        head_grid.height = table.height + row_height  # for table name
        tables_grid.height += head_grid.height

        # Add headers to the table.
        headers = [Label(text=self.SCORE_TXT, height=row_height, size_hint_y=None),
                   Label(text=self.DATE_TXT, height=row_height, size_hint_y=None),
                   Label(text=self.NAME_TXT, height=row_height, size_hint_y=None),
                   Label(text=self.NUMBER_TXT, height=row_height, size_hint_y=None)]

        for header in headers:
            table.add_widget(header)

        # Add scores to the table.
        tmp_scores = [(a['score'], a['date'], utils.fix_string(a['name']), i) for i, a in enumerate(scores)]
        for score_row in tmp_scores:
            for j in range(len(headers)):
                l = Label(text=str(score_row[j]))
                table.add_widget(l)

        # Line space
        table.add_widget(Label(text='', height=row_height, size_hint_y=None))

        tables_grid.add_widget(head_grid)
