import pymysql

from config import config
from logger import logger as logging


def database_connect():
    # # Open database connection
    logging.info("Connecting to MySQL..")
    database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"])
    logging.info("Database connection successful")

    logging.info("Creating cursor for communication..")
    database_cursor = database.cursor()

    database_cursor.execute("SHOW DATABASES")

    all_databases = [database_name[0] for (database_name) in database_cursor]

    if "csm" in all_databases:
        logging.info("Connecting to MySQL with csm database..")
        csm_database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"],
                                       database=config["mysql_database"])

    else:
        logging.debug("Creating 'csm' database..")
        database_cursor.execute("CREATE DATABASE csm")

        logging.info("Connecting to MySQL with csm database..")
        csm_database = pymysql.connect(host=config["mysql_host"], user=config["mysql_user"],
                                       database=config["mysql_database"])
        logging.info("Connection successful")

    logging.info("Creating cursor for communication with csm database..")
    csm_cursor = csm_database.cursor()
    logging.info("Cursor ready and awaiting commands.....")

    required_csm_tables = ["public_complaints", "public_suggestions", "officials_data"]

    csm_cursor.execute("SHOW TABLES")
    csm_all_tables = [table_name[0] for (table_name) in csm_cursor]

    for table in required_csm_tables:
        if table in csm_all_tables:
            continue
        else:
            if table == "public_complaints":
                csm_cursor.execute("CREATE TABLE {} (name VARCHAR(25), contact VARCHAR(11),age INT(3), email "
                                   "VARCHAR(30), occupation VARCHAR(20), current_location VARCHAR(25), complaint_type "
                                   "VARCHAR(50), complaint_to VARCHAR(50), complaint_subject VARCHAR(100), "
                                   "complaint_details VARCHAR(500), date DATE, s3_file_link VARCHAR(200), "
                                   "complaint_id VARCHAR(50), submission_type VARCHAR(12))".format(table))

            elif table == "public_suggestions":
                csm_cursor.execute("CREATE TABLE {} (name VARCHAR(25), contact VARCHAR(11), age INT(3), email "
                                   "VARCHAR(30), occupation VARCHAR(20), current_location VARCHAR(25), suggestion_type "
                                   "VARCHAR(50), suggestion_to VARCHAR(50), suggestion_subject VARCHAR(100), "
                                   "suggestion_details VARCHAR(500), date DATE, s3_file_link VARCHAR(200), "
                                   "suggestion_id VARCHAR(50), submission_type VARCHAR(12))".format(table))

            elif table == "officials_data":
                csm_cursor.execute("CREATE TABLE {} (username VARCHAR(25), password VARCHAR(25), "
                                   "designation VARCHAR(25))".format(table))

    database.close()
