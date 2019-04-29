import sqlite3 as sql
import Constants, pygame


class Database:
    def __init__(self):
        # Connects to the database file
        self.con = sql.connect(Constants.getPath('res/Database.db'))
        # creates a cursor object for the database
        self.cur = self.con.cursor()

        # Runs a command to fetch data from the database
        # If the database is empty which means it did not
        # previously exist, result will be empty
        self.cur.execute("SELECT * FROM sqlite_master")
        result = self.cur.fetchall()
        if not result:
            self.create_database()

    def create_database(self):
        # Creates empty tables for the database
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Controls (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Label TEXT UNIQUE NOT NULL,
        KEY_UP INTEGER NOT NULL,
        KEY_DOWN INTEGER NOT NULL,
        KEY_LEFT INTEGER NOT NULL,
        KEY_RIGHT INTEGER NOT NULL);
        ''')
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Players (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ControlsID INTEGER NOT NULL,
        UserName TEXT UNIQUE NOT NULL,
        FOREIGN KEY (ControlsID) REFERENCES Controls (ID));
        ''')
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Scores (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PlayerID INTEGER NOT NULL,
        Score INTEGER NOT NULL,
        FOREIGN KEY (PlayerID) REFERENCES Players (ID));
        ''')

        # Fill tables with default data
        self.cur.execute('''
        INSERT INTO Controls (ID, Label, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT) VALUES (0, 'Default', 273, 274, 276, 275);
        ''')
        self.cur.execute('''
        INSERT INTO Players (ID, ControlsID, UserName) VALUES (0, 0, 'Default');
        ''')
        self.con.commit()

    def create_player(self, playerName: str, controls: int = 0):
        '''Creates a new player profile, defaults to default controls'''
        added = False
        # Counter is the number that is added to the end of a duplicate name
        # To ensure names are unique
        counter = 0
        # Input is what the player inputted and will never contain the counter
        input = playerName
        while not added:
            try:
                self.cur.execute('''INSERT INTO Players (ControlsID, UserName) VALUES (?, ?);''', (controls, playerName))
                added = True
            # The error that is raised if the unique condition is broken
            except sql.IntegrityError:
                playerName = input + str(counter)
                counter += 1
        self.con.commit()

    def create_controls(self, controlLabel: str, UP: int, DOWN: int, LEFT: int, RIGHT: int):
        '''Creates a new control binding'''
        added = False
        counter = 0
        input = controlLabel
        while not added:
            try:
                self.cur.execute('''INSERT INTO Controls (Label, KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT) VALUES (?, ?, ?, ?, ?);''',
                                 (controlLabel, UP, DOWN, LEFT, RIGHT))
                added = True
            except sql.IntegrityError:
                controlLabel = input + str(counter)
                counter += 1
        self.con.commit()

    def get_players(self) -> tuple:
        '''Returns a list of all player profile names'''
        self.cur.execute('''
        SELECT UserName FROM Players
        ''')
        return self.cur.fetchall()

    def read_controls_label(self, controlLabel: str) -> tuple:
        '''Returns the controls of a control profile using the control label'''
        self.cur.execute('''SELECT KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT FROM Controls WHERE Label = ?''', (controlLabel,))
        return self.cur.fetchone()

    def read_controls_player(self, playerName: str) -> tuple:
        '''Returns the controls of a given player profile using an Inner Join'''
        self.cur.execute('''
        SELECT KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT FROM Controls 
        INNER JOIN Players on Controls.ID = Players.ControlsID WHERE Players.UserName = ?
        ''', (playerName,))
        return self.cur.fetchone()
