import random
import website


class database_query():
    def __init__(self, table):
        self._select = ['*']
        self._table = table
        self._where = []
        self._is_equal_to = []
        self._order_by = []
        self._db_limit = 5
        self._limit = 5
        self._query = None
        self._results = None

    def select(self, columns):
        self._select = columns
        return self

    def where(self, column):
        if len(column) != 1:
            raise ValueError
        self._where = column
        return self

    def is_equal_to(self, values):
        self._is_equal_to = values
        self._db_limit = min(len(values) * 20, 250)
        return self

    def order_by(self, column):
        if len(column) != 1:
            raise ValueError
        self._order_by = column
        return self

    def limit(self, limit):
        if type(limit) != int or limit < 1:
            raise ValueError
        self._limit = limit
        return self

    def _build_strings(self):
        self._select = ','.join(self._select)
        if self._where:
            self._where = self._where[0]
            self._is_equal_to = ["'" + x + "'" for x in self._is_equal_to]
            self._is_equal_to = ','.join(self._is_equal_to)
        if self._order_by:
            self._order_by = self._order_by[0]
        self._db_limit = str(self._db_limit)


    def _build_query(self):
        self._query = "SELECT"
        self._query += " " + self._select
        self._query += " FROM"
        self._query += " " + self._table
        if self._where:
            self._query += " WHERE"
            self._query += " " + self._where
            self._query += " IN"
            self._query += " (" + self._is_equal_to + ")"
        self._query += " LIMIT"
        self._query += " " + self._db_limit


    def _run_query(self):
        self._results = website.session.execute(self._query).all()

    def _sort_and_truncate(self):
        if self._order_by == 'Popular':
            self._results = sorted(self._results, key=lambda x:x['likes'], reverse=True)
        elif self._order_by == 'Random':
            random.shuffle(self._results)
        elif self._order_by == 'Recent':
            self._results = sorted(self._results, key=lambda x:x['published_at'])
        elif self._order_by == 'Length':
            # Needs to be added to db
            pass
        self._results = self._results[:self._limit]


    def execute(self):
        self._build_strings()
        self._build_query()
        self._run_query()
        self._sort_and_truncate()
        return self._results
