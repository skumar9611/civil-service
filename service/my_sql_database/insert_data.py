import pymysql

from config import config
from logger import logger as logging


def insert_data_to_database(table_name, consumer_data):
    csm_database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"],
                                   database=config["mysql_database"])

    logging.info("Creating cursor for communication with csm database..")
    csm_cursor = csm_database.cursor()
    logging.info("Cursor ready and awaiting commands.....")

    csm_cursor.execute("INSERT INTO {} VALUES {}".format(table_name, consumer_data))

    csm_database.commit()

    csm_database.close()
