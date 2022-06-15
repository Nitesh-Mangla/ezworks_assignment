from core import app
import pymysql

class Connection:

    __mysql = None

    @staticmethod
    def getDbInstance():
        if Connection.__mysql is None:
            Connection.__mysql = Connection.connector()

        return Connection.__mysql

    @staticmethod
    def connector():
        try:
            Connection.__mysql = pymysql.connect(
                host=app.config['DB_HOST'],
                user=app.config['DB_USERNAME'],
                password=app.config['DB_PASSWORD'],
                database=app.config['DB_NAME'],
                port=app.config['DB_PORT']
            )

            return Connection.__mysql
        except Exception as e:
            print('Error: Mysql connection not established {}'.format(e))
            exit()