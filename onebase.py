import sqlite3

class Database():

    def __init__(self):
        self.db = 'onebase'
        self.table = 'Main'
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table} (None)')
        self.connection.commit()
        self.headers = [description[0] for description in self.cursor.execute(f'select * from {self.table}').description]

    def _destroy(self):
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
        tables = self.cursor.fetchall()
        for table in tables:
            table_value = table[0]
            self.cursor.execute(f'DROP TABLE {table_value}')
        del tables
        self.connection.commit()

    def _refactor(self):
        header_value = str(self.headers)[1:-1]
        self.cursor.execute(f'CREATE TABLE temp ({header_value})')
        self.cursor.execute(f'INSERT INTO temp SELECT * FROM {self.table}')
        self.cursor.execute(f'DROP TABLE {self.table}')
        self.cursor.execute(f'CREATE TABLE {self.table} ({header_value})')
        self.cursor.execute(f'INSERT INTO {self.table} SELECT * FROM temp')
        self.cursor.execute('DROP TABLE temp')
        del header_value
        self.connection.commit()

    def _headers(self):
        dataset = self.cursor.execute(f'select * from {self.table}').description
        self.headers = [description[0] for description in dataset]
        del dataset

    def show(self):
        print(self.headers[1:])
        data = self.cursor.execute(f'SELECT * FROM {self.table}')
        for row in data:
            print(row[1:])
        del data

    def add_column(self, header):
        self.cursor.execute(f'ALTER TABLE {self.table} ADD COLUMN {header} TEXT')
        self.connection.commit()
        self._headers()

    def add(self, dataset):
        dataset.insert(0, None)
        marks = []
        for i in dataset:
            marks.append('?')
        values = ','.join(marks)
        self.cursor.execute(f'INSERT INTO {self.table} VALUES ({values})', dataset)
        self.connection.commit()

    def locate(self, searchword):
        locations = []
        for header in self.headers:
            self.cursor.execute(f'SELECT rowid from {self.table} WHERE {header} = {searchword}')
            rowid = self.cursor.fetchall()
            if rowid:
                for row in rowid:
                    locations.append([row[0], header])
        self.connection.commit()
        return locations

    def remove(self, index):
        self.cursor.execute(f'DELETE from {self.table} WHERE rowid = {index}')
        self.connection.commit()
        self._refactor()

    def replace(self, index, dataset):
        dataset.insert(0, None)
        consolidation = zip(self.headers, dataset)
        for header, data in consolidation:
            self.cursor.execute(f'Update {self.table} set {header} = "{data}" where rowid = {index}')
            self.connection.commit()
        del consolidation

    def close(self):
        self.connection.close()