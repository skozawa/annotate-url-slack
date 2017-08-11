import MySQLdb
import MySQLdb.cursors

from annotate.config import config


class DB(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            db=config.DB_CONFIG['db'],
            host=config.DB_CONFIG['host'],
            user=config.DB_CONFIG['user'],
            password=config.DB_CONFIG['password'],
            cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8',
        )

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
