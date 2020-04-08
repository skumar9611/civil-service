import pymysql

from config import config
from logger import logger as logging


class SQLClient:
    def __init__(self):
        try:
            logging.info("Connecting to MySQL..")
            database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"])
            logging.info("Database connection successful")

            logging.info("Creating cursor for communication..")
            database_cursor = database.cursor()

            logging.debug("Checking and creating 'csm' database..")
            database_cursor.execute("CREATE DATABASE csm")

            logging.info("Connecting to MySQL with csm database..")
            self.csm_database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"], database=config["mysql_database"])
            logging.info("Connection successful")

            logging.info("Creating cursor for communication with csm database..")
            self.cursor = self.csm_database.cursor()
            logging.info("Cursor ready and awaiting commands.....")

        except Exception as exception:
            logging.error(exception)
            raise Exception(exception)

    def get_tables(self):
        print(self.cursor.execute("SHOW TABLES"))


my_sql_client = SQLClient
# def database_connect():
#     # # Open database connection
#     db = pymysql.connect(host="localhost", user="root", database="csm")
#
#     print(db)
#     # prepare a cursor object using cursor() method
#     cursor = db.cursor()
#
#     # execute SQL query using execute() method.
#     cursor.execute("CREATE DATABASE csm")
#     print(cursor)
# #     #
# #     # # Fetch a single row using fetchone() method.
# #     # data = cursor.fetchone()
# #     # print("Database version : %s " % data)
# #     #
# #     # # disconnect from server
# #     # db.close()
# #
# #     # db_connection = mysql.connector.connect(
# #     #     host="localhost",
# #     #     user="root",
# #     #     passwd="root"
# #     # )
# #     # print(db_connection)
